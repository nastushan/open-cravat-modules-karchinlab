import os
import sqlite3
import random
import cravat
import json

class Mapper(cravat.BaseMapper):
    """
    Map genomic positions to transcripts from knowngene
    """
    
    def _define_additional_cmd_args(self):
        """
        Setup cmd arg parsing in addition to that in BaseMapper.
        """
        self.cmd_parser.add_argument('--include-sources',
                                     nargs = '+',
                                     default = [],
                                     help='Gene sources to include. '\
                                          +'Default all.')
        self.cmd_parser.add_argument('--exclude-sources',
                                     nargs = '+',
                                     default = [],
                                     help='Gene sources to exclude. '\
                                     +'Default KnownGene.')
        self.cmd_parser.add_argument('--primary-source',
                                     nargs='?',
                                     default='EnsemblT',
                                     help='Specify a preffered gene source '\
                                          +'to be reported in the transcript '\
                                          +'column.')
    
    def setup(self):
        """
        Setup attributes will be used by this mapper
        """
        db_path = os.path.join(self.mapper_dir, 'data', 'hg38.sqlite')
        if not(os.path.exists(db_path)):
            raise Exception('No database at %s' %db_path)
        self.logger.info('Using database at: %s' %db_path)
        self.db = sqlite3.connect(db_path)
        self.c = self.db.cursor()
        q = 'select distinct source from transcript;'
        self.c.execute(q)
        all_sources = set([x[0] for x in self.c.fetchall()])
        include_sources = set(self.cmd_args.include_sources)
        exclude_sources = set(self.cmd_args.exclude_sources)
        if include_sources - all_sources:
            err_msg = 'Include source(s) %s are not available in the database'\
                %', '.join(list(include_sources - all_sources))
            raise Exception(err_msg)
        if exclude_sources - all_sources:
            err_msg = 'Exclude source(s) %s are not available in the database'\
                %', '.join(list(exclude_sources - all_sources))
            raise Exception(err_msg)
        if include_sources:
            self.gene_sources = list(include_sources - exclude_sources)
        else:
            self.gene_sources = list(all_sources - exclude_sources)
        if len(self.gene_sources) == 1:
            self.primary_gene_source = self.gene_sources[0]
        else:
            if self.cmd_args.primary_source not in self.gene_sources:
                err_msg = 'Primary source (%s) not in selected gene sources (%s)'\
                    %(self.cmd_args.primary_source, ', '.join(self.gene_sources))
                raise Exception(err_msg)
            self.primary_gene_source = self.cmd_args.primary_source
        self.logger.info('Gene source(s): %s' %', '.join(self.gene_sources))
        self.logger.info('Primary gene source: %s' %self.primary_gene_source)
        
    def map(self, crv_data):
        """
        Takes a dict with crv fields and return a dict with crx fields
        """
        all_hits = []
        self.hit_tr = {}
        all_hits += self._get_coding_hits(crv_data)
        all_hits += self._get_splice_site_hits(crv_data)
        all_hits += self._get_non_coding_hits(crv_data)
        # If no coding/neargene hits are found, variant is intergenic
        if not(all_hits):
            hit = IntergenicHit()
            hit.load_crv(crv_data)
            all_hits.append(hit)
        crx_data, alt_transcripts = self._combine_to_crx_data(crv_data, all_hits)
        return crx_data, alt_transcripts
        
    def _get_non_coding_hits(self, crv_data):
        """
        Query noncoding table for hit start position in noncoding range.
            
        Creates NonCodingHit object and fills with relevant information
        """
        hit_list = []
        chrom = crv_data['chrom']
        pos = crv_data['pos']
        bins = cravat.get_ucsc_bins(pos)
        pos = str(pos)
        for gbin in bins:
            query = 'select tid, desc from noncoding ' +\
                'where binno=' + str(gbin) + ' and ' +\
                'chrom="' + chrom + '" and ' +\
                'start<=' + pos + ' and end>=' + pos
            self.c.execute(query) 
            ncd_results = self.c.fetchall()
            for result in ncd_results:
                try:
                    hit = NoncodingHit()
                    hit.load_crv(crv_data)
                    hit.gbin = gbin
                    hit.tid = result[0]
                    if hit.tid in self.hit_tr:
                        continue
                    self._fill_transcript_info(hit)
                    hit.so = result[1]
                    hit_list.append(hit)
                    self.hit_tr[hit.tid] = True
                except DiscardHit:
                    continue
        return hit_list
    
    def _get_splice_site_hits(self, crv_data):
        """
        Query splice table for hit start position on splice site.
        
        Creates CodingHit object and fills with relevant information
        """
        hit_list = []
        gbin = cravat.get_ucsc_bins(crv_data['pos'])[0]
        q = 'select * from splice where chrom="%s" and binno=%d and gpos=%d;' \
            %(crv_data['chrom'], gbin, crv_data['pos'])
        self.c.execute(q)
        splice_query_results = self.c.fetchall()
        splice_query_headers = [x[0] for x in self.c.description]
        for splice_row in splice_query_results:
            try:
                splice_dict = dict(zip(splice_query_headers, splice_row))
                hit = CodingHit()
                hit.load_crv(crv_data)
                hit.gbin = splice_dict['binno']
                hit.tid = splice_dict['tid']
                if hit.tid in self.hit_tr:
                    continue
                self._fill_transcript_info(hit)
                hit.so = 'SPL'
                hit.apos_start = splice_dict['apos']
                hit_list.append(hit)
                self.hit_tr[hit.tid] = True
            except DiscardHit:
                continue
            
        return hit_list
    
    def _get_coding_hits(self, crv_data):
        """
        Query coding table for affected transcripts and determine sequence
        changes within those transcripts.
        
        Check both genomic start and end position of variant since
        transcripts can occur on both strands. Swap start and end in the
        case of a minus strand transcript.
        """
        coding_hits = []
        chrom = crv_data['chrom']
        start_gpos = crv_data['pos']
        end_gpos = start_gpos + len(crv_data['ref_base']) - 1
        gstart_tdata = self._coding_query(chrom=chrom, gpos=start_gpos)
        gend_tdata = self._coding_query(chrom=chrom, gpos=end_gpos)
        all_tids = set(list(gstart_tdata.keys()) + list(gend_tdata.keys()))
        for tid in all_tids:
            try:
                hit = CodingHit()
                hit.load_crv(crv_data)
                hit.tid = tid
                if hit.tid in self.hit_tr:
                    continue
                self._fill_transcript_info(hit)
                # Both start and end position must be in the coding region
                # of the transcript to determine sequence ontology
                if tid in gstart_tdata and tid in gend_tdata:
                    # Fill in ref base if needed
                    if hit.gref == '':
                        hit.gref = gstart_tdata[tid]['base']
                    # Map plus strand genomic start/end to transcript direction
                    if hit.transcript.strand == '+':
                        hit.cref = hit.gref
                        hit.calt = hit.galt
                        tstart_info = gstart_tdata[tid]
                        tend_info = gend_tdata[tid]
                    else:
                        hit.cref = cravat.reverse_complement(hit.gref)
                        hit.calt = cravat.reverse_complement(hit.galt)
                        # Adjust the position for inserts on minus strand transcript
                        if hit.cref == '-': 
                            adj_tpos = gstart_tdata[tid]['tpos'] + 1
                            adj_tstart_tdata = self._coding_query(tid=tid, tpos=adj_tpos)
                            tstart_info = adj_tstart_tdata[tid]
                            tend_info = tstart_info
                        else:
                            tstart_info = gend_tdata[tid]
                            tend_info = gstart_tdata[tid]
                    # Add the start/end transcript positions to the hit
                    hit.tpos_start = tstart_info['tpos']
                    hit.apos_start = tstart_info['apos']
                    hit.cpos_start = tstart_info['cpos']
                    hit.tpos_end = tend_info['tpos']
                    hit.apos_end = tend_info['apos']
                    hit.cpos_end = tend_info['cpos']
                    # Determine sequence ontology
                    self._fill_coding_so(hit)
                    self.hit_tr[hit.tid] = True
                else:
                    hit.so = 'UNK'
                coding_hits.append(hit)
            except DiscardHit:
                continue    
        
        return coding_hits
        
    def _coding_query(self, chrom=None, gpos=None, tid=None, tpos=None):
        """
        Query the coding table to generate a dict keyed by tid and containing 
        the transcript-coordinate positions of the genomic position.
        
        Queries can be made using either chrom and gpos or tid and tpos.
        """
        if chrom is not None and gpos is not None:
            gbin = cravat.get_ucsc_bins(gpos)[0]
            q = 'select v.tid, v.apos, v.cpos, v.tpos, v.base from '\
                +'coding as v join chrom as c on v.chromid=c.chromid '\
                +'where c.chrom="'+chrom+'" '\
                +'and v.binno='+str(gbin)+' '\
                +'and v.gpos='+str(gpos)+';'
        elif tid is not None and tpos is not None:
            q = 'select v.tid, v.apos, v.cpos, v.tpos, v.base from '\
                +'coding as v join chrom as c on v.chromid=c.chromid '\
                +'where v.tid="'+str(tid)+'" '\
                +'and v.tpos='+str(tpos)+';'
        else:
            raise Exception('Must include (chrom and gpos) or (tid and tpos)')
        self.c.execute(q)
        qr = self.c.fetchall()
        headers = [x[0] for x in self.c.description]
        td = {}
        for r in qr:
            d = dict(zip(headers, r))
            tid = d['tid']
            del d['tid']
            td[tid] = d
        return td
        
    def _fill_positions(self, hit, map_dict):
        """ 
        Fill Hit object with info relevant to transcript sequence
        """
        # Position in transcript coords of variant before correcting for strand
        orig_tpos = codon_to_tpos(map_dict['apos'], map_dict['cpos'])
        if hit.transcript.strand == '+':
            hit.cref = hit.gref
            hit.calt = hit.galt
            hit.apos_start = map_dict['apos']
            hit.cpos_start = map_dict['cpos']
            hit.tpos_start = orig_tpos
        else:
            # Make corrections needed for minus strand transcript
            hit.cref, shift = cravat.switch_strand(hit.gref, start_strand='+')
            hit.calt, _ = cravat.switch_strand(hit.galt, start_strand='+')
            hit.tpos_start = orig_tpos + shift
            if hit.tpos_start < 0:
                print('Strand switch resulted in non-coding')
                #TODO handle this case
            hit.apos_start, hit.cpos_start = tpos_to_codon(hit.tpos_start)
        hit.tpos_end = hit.tpos_start + len(hit.gref) - 1
        hit.apos_end, hit.cpos_end = tpos_to_codon(hit.tpos_end)
        
    def _fill_coding_so(self, hit):
        """
        Predict sequence ontology based on ref and alt base
        """
        if hit.gref == hit.galt:
            hit.so = 'SYN'
        else:
            if hit.gref == '-':
                extra_bases = len(hit.galt)%3
                if extra_bases == 0:
                    hit.so = 'IIV'
                elif extra_bases == 1:
                    hit.so = 'FI1'
                elif extra_bases == 2:
                    hit.so = 'FI2'
            elif hit.galt == '-':
                extra_bases = len(hit.gref)%3
                if extra_bases == 0:
                    hit.so = 'IDV'
                elif extra_bases == 1:
                    hit.so = 'FD1'
                elif extra_bases == 2:
                    hit.so = 'FD2'
            elif len(hit.gref) == 1 and len(hit.galt) == 1:
                self._fill_snv_pchange(hit)
                if hit.aref != hit.aalt:
                    if hit.aref == '*':
                        hit.so = 'STL'
                    elif hit.aalt == '*':
                        hit.so = 'STG'
                    else:
                        hit.so = 'MIS'
                else:
                    hit.so = 'SYN'
            else:
                hit.so = 'CSS'
    
    def _fill_snv_pchange(self, hit):
        """
        Get amino-acid change from single nucleotide variant
        """
        q = 'select codon from codon where tid=%d and apos=%d' \
            %(hit.tid, hit.apos_start)
        self.c.execute(q)
        hit.full_ref = self.c.fetchone()[0]
        hit.full_alt = hit.full_ref[:hit.cpos_start - 1] \
                       + hit.calt \
                       + hit.full_ref[hit.cpos_start:]
        hit.aref = cravat.translate_codon(hit.full_ref)
        hit.aalt = cravat.translate_codon(hit.full_alt)
    
    def _fill_transcript_info(self, hit):
        """
        Query transcript and transcript info
        
        Put information into Transcript object stored in Hit.transcript
        """
        q = 'select * from transcript where tid="%s"  and source in ("%s");'\
            %(hit.tid, '", "'.join(self.gene_sources))
        self.c.execute(q)
        transcript_headers = [x[0] for x in self.c.description]
        transcript_rows = self.c.fetchall()
        if not(transcript_rows):
            raise DiscardHit()
        for trow in transcript_rows:
            tdict = dict(zip(transcript_headers, trow))
            hit.transcript.load_from_transcript_table(tdict)
        q = 'select * from transcript_info where tid="%s";' %hit.tid
        self.c.execute(q)
        transcript_info_headers = [x[0] for x in self.c.description]
        transcript_info = dict(zip(transcript_info_headers, self.c.fetchone()))
        hit.transcript.load_from_transcript_info_table(transcript_info)
            
    def _get_placeholder_uniprot(self):
        placeholder_uniprots = ['uniprot1']*1+['uniprot2']*3+['uniprot3']*3
        return random.choice(placeholder_uniprots)
    
    def _combine_to_crx_data(self, crv_data, all_hits):
        """
        Combine all Hit objects to make a dict with crx fields
        """
        # Define the crx dict
        crx_data = {x['name']:'' for x in cravat.crx_def}
        # Crv data gets duplicated in crx dict
        for col_name, value in crv_data.items():
            crx_data[col_name] = value
        primary_so = '' # Initially set to least severe so
        primary_transc_alen = 0
        primary_transc = ''
        primary_hugo = ''
        all_maps = {}
        alt_transcripts = {}
        primary_has_protein = False
        for hit in all_hits:
            if hit.hit_type == 'intergenic': 
                continue
            elif hit.hit_type in ['coding', 'noncoding']:
                # Replace empty ref_base with data from hit if available
                if crx_data['ref_base'] == '' and hit.gref != '':
                    crx_data['ref_base'] = hit.gref
                # Add to all maps dict
                if hit.apos_start != None:
                    aref = hit.aref if hit.aref is not None else '_'
                    aalt = hit.aalt if hit.aalt is not None else '_'
                    a_change = aref + str(hit.apos_start) + aalt
                else:
                    a_change = None
                if hit.cref != None and hit.tpos_start != None and hit.calt != None:
                    cref = hit.cref if hit.cref is not None else '_'
                    calt = hit.calt if hit.calt is not None else '_'
                    c_change = cref + str(hit.tpos_start) + calt
                else:
                    c_change = None
                protein = hit.transcript.protein
                so = hit.so
                hugo = hit.transcript.hugo
                transc = hit.transcript.names_by_source[self.primary_gene_source]
                if hugo not in all_maps: all_maps[hugo] = []
                hit_list = [protein, a_change, so, transc, c_change]
                all_maps[hugo].append(hit_list)
                # Add to alt transcripts dict
                if transc not in alt_transcripts:
                    alt_transcripts[transc] = []
                for t_source, t_name in hit.transcript.names_by_source.items():
                    if t_source != self.primary_gene_source:
                        alt_transcripts[transc].append(t_name)
                # Determine whether current hit is more deleterious than
                # all previous hits
                more_severe = cravat.more_severe_so(so, primary_so)
                equally_severe = so == primary_so
                longer = hit.transcript.alen > primary_transc_alen
                cur_has_protein = protein is not None
                if (cur_has_protein or not(primary_has_protein)) \
                   and (more_severe or (equally_severe and longer)):
                    primary_hugo = hugo
                    primary_transc = transc
                    primary_transc_alen = hit.transcript.alen
                    primary_so = hit.so
                    primary_has_protein = cur_has_protein
        # Fill crx dict with information from most deleterious transcript
        crx_data['hugo'] = primary_hugo
        if primary_hugo != '':
            crx_data['coding'] = 1
        else:
            crx_data['coding'] = 0
        crx_data['transcript'] = primary_transc
        crx_data['so'] = primary_so
        # Fill crx dict with all mappings
        crx_data['all_mappings'] = json.dumps(all_maps,
                                                         separators=(',', ':'))
        return crx_data, alt_transcripts
    
def tpos_to_codon(tpos):
    """
    Convert a transcript coordinate to an amino-acid number and codon index
    """
    py_tpos = tpos - 1
    apos = int(py_tpos/3) + 1 # int() truncates to floor
    cpos = py_tpos%3 + 1
    return apos, cpos

def codon_to_tpos(apos, cpos):
    """
    Convert an amino-acid number and codon index to a transcript coordinate
    """
    return 3*(apos - 1) + cpos

class FrozenClass(object):
    """
    FrozenClass does not accept new attributes while frozen
    """
    __frozen = False
    def freeze(self):
        self.__frozen = True
    def unfreeze(self):
        self.__frozen = False
    def __setattr__(self, name, value):
        if hasattr(self, name) or not(self.__frozen):
            object.__setattr__(self, name, value)
        else:
            raise AttributeError('Cannot set name %r on object of type %s' % (
                name, self.__class__.__name__))
    def __str__(self):
        return ', '.join(['%s:(%s)' %(k, str(v)) 
                          for k, v in self.__dict__.items()])
        
class Transcript(FrozenClass):
    """
    Holds information from transcript and transcript info tables
    """
    def __init__(self):
        self.tid = None
        self.protein = None
        self.hugo = None
        self.alen = None
        self.clen = None
        self.chrom = None
        self.strand = None
        self.names_by_source = {}
        self.freeze()
        
    def load_from_transcript_table(self, d):
        self.tid = d['tid']
        self.names_by_source[d['source']] = d['name']
    
    def load_from_transcript_info_table(self, d):
        self.protein = d['sprot']
        self.hugo = d['hugo']
        self.strand = d['strand']
        self.alen = d['alen']
        self.clen = self.alen * 3
        self.chrom = d['chrom']

class Hit(FrozenClass):
    """
    Holds information in crv dict
    """
    def __init__(self):
        self.uid = None
        self.chrom = None
        self.gpos = None
        self.gref = None
        self.galt = None
        self.hit_type = None
    
    def load_crv(self, crv_data):
        self.uid = crv_data['uid']
        self.chrom = crv_data['chrom']
        self.gpos = crv_data['pos']
        self.gref = crv_data['ref_base']
        self.galt = crv_data['alt_base']

class IntergenicHit(Hit):
    """
    Hits that are not in gene or near-gene regions
    """
    def __init__(self):
        super().__init__()
        self.hit_type = 'intergenic'
        self.freeze()
        
class NoncodingHit(Hit):
    """
    Holds information from noncoding table
    """
    def __init__(self):
        super().__init__()
        self.hit_type = 'noncoding'
        self.tid = None
        self.gbin = None
        self.so = None
        self.tpos_start = None
        self.cpos_start = None
        self.cref = None
        self.calt = None
        self.apos_start = None
        self.aref = None
        self.aalt = None
        self.transcript = Transcript()
        self.freeze()

class CodingHit(Hit):
    """
    Holds information from coding table
    """
    def __init__(self):
        super().__init__()
        self.hit_type = 'coding'
        # Position from start transcript coding region
        self.tpos_start = None
        self.tpos_end = None
        # Ref and Alt bases on transcript strand
        self.cref = None
        self.calt = None
        # Position within the codon (1, 2, or 3)
        self.cpos_start = None
        self.cpos_end = None
        # Position within translated amino-acid chain
        self.apos_start = None
        self.apos_end = None
        # Ref and alt amino-acids
        self.aref = None
        self.aalt = None
        # Bin number in coding table
        self.gbin = None
        self.so = None
        # Nucleotide sequence of all affected codons
        self.full_ref = None
        self.full_alt = None
        # tid in coding, transcript and transcript_info tables
        self.tid = None
        # Transcript information is held here
        self.transcript = Transcript()
        self.freeze()
        
class DiscardHit(Exception):
    """
    Used internally to signal that a hit should not be included in the main list
    """
    pass
        
if __name__ == '__main__':
    mapper = Mapper()
    mapper.run()                