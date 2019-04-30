from cravat import BaseConverter
from cravat import BadFormatError

import re

class CravatConverter(BaseConverter):
    
    def __init__(self):
        self.format_name = 'vcf'
        self.samples = []
        self.var_counter = 0
        self.addl_cols = [{'name':'phred',
                           'title':'Phred',
                           'type':'string'},
                          {'name':'filter',
                           'title':'VCF filter',
                           'type':'string'},
                          {'name':'zygosity',
                           'title':'Zygosity',
                           'type':'string'},
                          {'name':'alt_reads',
                           'title':'Alternate reads',
                           'type':'int'},
                          {'name':'tot_reads',
                           'title':'Total reads',
                           'type':'int'},
                          {'name':'af',
                           'title':'Variant allele frequency',
                           'type':'float'},
                          {'name': 'hap_block',
                           'title': 'Haplotype block ID',
                           'type': 'int'},
                          {'name': 'hap_strand',
                           'title': 'Haplotype strand ID',
                           'type': 'int'}]
    
    def check_format(self, f): 
        vcf_format = False
        if f.name.endswith('.vcf'):
            vcf_format = True
        first_line = f.readline()
        if first_line.startswith('##fileformat=VCF'):
            vcf_format = True
        second_line = f.readline()
        if second_line.startswith('##source=VarScan'):
            self.vcf_format = 'varscan'
        else:
            self.vcf_format = 'unknown'
        return vcf_format
    
    def setup(self, f):
        
        vcf_line_no = 0
        for line in f:
            vcf_line_no += 1
            if len(line) < 6:
                continue
            if line[:6] == '#CHROM':
                toks = re.split('\s+', line.rstrip())
                if len(toks) > 8:
                    self.samples = toks[9:]
                break
    
    def convert_line(self, l):
        if l.startswith('#'): return None
        self.var_counter += 1
        toks = l.strip('\r\n').split('\t')
        toklen = len(toks)
        all_wdicts = []
        if toklen < 5:
            raise BadFormatError('At least CHROM POS ID REF ALT columns are needed')
        [chrom, pos, tag, ref, alts] = toks[:5]
        if toklen >= 6:
            qual = toks[5]
            if qual == '.': qual = None
        else:
            qual = None
        if toklen >= 7:
            filter = toks[6]
            if filter == '.': filter = None
        else:
            filter = None
        if toklen >= 8:
            info = toks[7]
            if info == '.': info = None
        else:
            info = None
        if tag == '.':
            tag = None
        alts = alts.split(',')
        len_alts = len(alts)
        if toklen <= 8 and toklen >= 5:
            for altno in range(len_alts):
                wdict = None
                alt = alts[altno]
                newpos, newref, newalt = self.extract_vcf_variant('+', pos, ref, alt)
                if newalt == '*': # VCF 4.2
                    continue
                wdict = {'tags':tag,
                         'chrom':chrom,
                         'pos':newpos,
                         'ref_base':newref,
                         'alt_base':newalt,
                         'sample_id':'no_sample',
                         'phred': qual,
                         'filter': filter,
                }
                all_wdicts.append(wdict)
        elif toklen > 8:
            sample_datas = toks[9:]
            genotype_fields = {}
            genotype_field_no = 0
            for genotype_field in toks[8].split(':'):
                genotype_fields[genotype_field] = genotype_field_no
                genotype_field_no += 1
            if not ('GT' in genotype_fields):
                raise BadFormatError('No GT Field')
            gt_field_no = genotype_fields['GT']
            for sample_no in range(len(sample_datas)):
                sample = self.samples[sample_no]
                sample_data = sample_datas[sample_no].split(':')
                gts = {}
                for gt in sample_data[gt_field_no].replace('/', '|').split('|'):
                    if gt == '.':
                        continue
                    else:
                        gts[int(gt)] = True
                for gt in sorted(gts.keys()):
                    wdict = None
                    if gt == 0:
                        continue
                    else:
                        alt = alts[gt - 1]
                        newpos, newref, newalt = self.extract_vcf_variant('+', pos, ref, alt)
                        if newalt == '*': # VCF 4.2
                            continue
                        zyg = self.homo_hetro(sample_data[gt_field_no])
                        depth, alt_reads, af = self.extract_read_info(sample_data, gt, gts, genotype_fields)
                        if depth == '.': depth = None
                        if alt_reads == '.': alt_reads = None
                        if af == '.': af = None
                        if 'HP' in genotype_fields:
                            hp_field_no = genotype_fields['HP']
                            haplotype_block = sample_data[hp_field_no].split(',')[0].split('-')[0]
                            haplotype_strand = sample_data[hp_field_no].split(',')[0].split('-')[1]
                            wdict = {'tags':tag,
                                     'chrom':chrom,
                                     'pos':newpos,
                                     'ref_base':newref,
                                     'alt_base':newalt,
                                     'sample_id':sample,
                                     'phred': qual,
                                     'filter': filter,
                                     'zygosity': zyg,
                                     'tot_reads': depth,
                                     'alt_reads': alt_reads,
                                     'af': af,
                                     'hap_block': haplotype_block,
                                     'hap_strand': haplotype_strand,                               
                                     } 
                        else:
                            wdict = {'tags':tag,
                                     'chrom':chrom,
                                     'pos':newpos,
                                     'ref_base':newref,
                                     'alt_base':newalt,
                                     'sample_id':sample,
                                     'phred': qual,
                                     'filter': filter,
                                     'zygosity': zyg,
                                     'tot_reads': depth,
                                     'alt_reads': alt_reads,
                                     'af': af, 
                                     'hap_block': None,
                                     'hap_strand': None,                               
                                     }
                        all_wdicts.append(wdict)
        return all_wdicts
 
    #The vcf genotype string has a call for each allele separated by '\' or '/'
    #If the call is the same for all allels, return 'hom' otherwise 'het'
    def homo_hetro(self, gt_str):
        if '.' in gt_str:
            return '';
        
        gts = gt_str.strip().replace('/', '|').split('|')
        for gt in gts:
            if gt != gts[0]:
                return 'het'
        return 'hom'            

    #Extract read depth, allele count, and allele frequency from optional VCR information
    def extract_read_info (self, sample_data, gt, gts, genotype_fields): 
        depth = ''
        alt_reads = ''
        ref_reads = ''
        af = ''
        #AD contains 2 values usually ref count and alt count unless there are 
        #multiple alts then it will have alt 1 then alt 2.
        if self.vcf_format == 'varscan':
            if 'AD' in genotype_fields and 'RD' in genotype_fields:
                try:
                    ref_reads = sample_data[genotype_fields['RD']]
                except:
                    ref_reads = ''
                try:
                    alt_reads = sample_data[genotype_fields['AD']]
                except:
                    alt_reads = ''
        else:
            if 'AD' in genotype_fields and genotype_fields['AD'] <= len(sample_data): 
                if 0 in gts.keys():
                    #if part of the genotype is reference, then AD will have #ref reads, #alt reads
                    try:
                        ref_reads = sample_data[genotype_fields['AD']].split(',')[0]
                    except:
                        ref_reads = ''
                    try:
                        alt_reads = sample_data[genotype_fields['AD']].split(',')[1]
                    except:
                        alt_reads = ''
                elif gt == max(gts.keys()):    
                    #if geontype has multiple alt bases, then AD will have #alt1 reads, #alt2 reads
                    try:
                        alt_reads = sample_data[genotype_fields['AD']].split(',')[1]
                    except:
                        alt_reads = ''
                else:
                    try:
                        alt_reads = sample_data[genotype_fields['AD']].split(',')[0]
                    except:
                        alt_reads = ''
        if alt_reads != '' and ref_reads != '':
            # Default dp = ref+alt
            depth = int(alt_reads) + int(ref_reads)   
        elif 'DP' in genotype_fields and genotype_fields['DP'] <= len(sample_data): 
            # DP is fallback because some callers apply additional filters to DP which are not applied to AD
            depth = sample_data[genotype_fields['DP']] 
        else:
            depth = ''
        if 'AF' in genotype_fields and genotype_fields['AF'] <= len(sample_data):
            try:
                af = round(float(sample_data[genotype_fields['AF']] ),3)
            except:
                af = ''
        elif depth != '' and alt_reads != '':
            #if AF not specified, calc it from alt and ref reads
            af = None
            try: # Handle cases where alt_reads and/or depth are a placeholder character like '.'
                int(alt_reads)
                int(depth)
            except ValueError:
                af = ''
            if af is None:
                if int(depth) == 0: # Uncommon case where a filter has removed all reads but call is still made
                    af = ''
                else:
                    af = round(int(alt_reads) / int(depth),3)
        else:
            af = ''
        if type(af) == float: # Bound af to [0.0, 1.0]
            if af > 1.0:
                af = 1.0
            elif af < 0.0:
                af = 0.0
        return depth, alt_reads, af

    def extract_vcf_variant (self, strand, pos, ref, alt):

        reflen = len(ref)
        altlen = len(alt)
        
        # Returns without change if same single nucleotide for ref and alt. 
        if reflen == 1 and altlen == 1 and ref == alt:
            return pos, ref, alt
        
        # Trimming from the start and then the end of the sequence 
        # where the sequences overlap with the same nucleotides
        new_ref2, new_alt2, new_pos = \
            self.trimming_vcf_input(ref, alt, pos, strand)
                
        if new_ref2 == '' or new_ref2 == '.':
            new_ref2 = '-'
        if new_alt2 == '' or new_alt2 == '.':
            new_alt2 = '-'
        
        return new_pos, new_ref2, new_alt2
    
    # This function looks at the ref and alt sequences and removes 
    # where the overlapping sequences contain the same nucleotide.
    # This trims from the end first but does not remove the first nucleotide 
    # because based on the format of VCF input the 
    # first nucleotide of the ref and alt sequence occur 
    # at the position specified.
    #     End removed first, not the first nucleotide
    #     Front removed and position changed
    def trimming_vcf_input(self, ref, alt, pos, strand):
        pos = int(pos)
        reflen = len(ref)
        altlen = len(alt)
        minlen = min(reflen, altlen)
        new_ref = ref
        new_alt = alt
        new_pos = pos
        # Trims from the end. Except don't remove the first nucleotide. 
        # 1:6530968 CTCA -> GTCTCA becomes C -> GTC.
        for nt_pos in range(0, minlen - 1): 
            if ref[reflen - nt_pos - 1] == alt[altlen - nt_pos - 1]:
                new_ref = ref[:reflen - nt_pos - 1]
                new_alt = alt[:altlen - nt_pos - 1]
            else:
                break    
        new_ref_len = len(new_ref)
        new_alt_len = len(new_alt)
        minlen = min(new_ref_len, new_alt_len)
        new_ref2 = new_ref
        new_alt2 = new_alt
        # Trims from the start. 1:6530968 G -> GT becomes 1:6530969 - -> T.
        for nt_pos in range(0, minlen):
            if new_ref[nt_pos] == new_alt[nt_pos]:
                if strand == '+':
                    new_pos += 1
                elif strand == '-':
                    new_pos -= 1
                new_ref2 = new_ref[nt_pos + 1:]
                new_alt2 = new_alt[nt_pos + 1:]
            else:
                new_ref2 = new_ref[nt_pos:]
                new_alt2 = new_alt[nt_pos:]
                break  
        return new_ref2, new_alt2, new_pos
