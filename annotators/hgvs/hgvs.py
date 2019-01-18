import sys
from cravat import BaseAnnotator
from cravat import InvalidData
from cravat import translate_codon, aa_let_to_abbv, AllMappingsParser
import sqlite3
import os
import re
import math

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        self.cursor.execute('select * from transsequence limit 1;')
        self.transsequence_headers = [x[0] for x in self.cursor.description]
        
    def _get_hgvs_g(self, chrom, pos, ref, alt):
        """
        Gets genomic level hgvs variant.
        """
        chrom_short = chrom.replace('chr','')
        if chrom_short == 'X' or chrom_short == 'x':
            chrom_num = '23'
        elif chrom_short == 'Y' or chrom_short == 'y':
            chrom_num = '24'
        elif len(chrom_short) < 2:
            chrom_num = '0' + chrom_short
        else:
            chrom_num = chrom_short
            
        hgvs_g = 'NC_0000%s.%s:g.' \
            %(chrom_num, self.conf['nc_assembly_version'])
        
        hgvs_g += self._get_hgvs_nuc(pos, ref, alt)
        
        return hgvs_g
    
    def _get_hgvs_r(self, transcript, pos, ref, alt):
        """
        Gets transcript level hgvs variant.
        """
        ref = ref.replace('T','u').lower()
        alt = alt.replace('T','u').lower()
        hgvs_nuc = self._get_hgvs_nuc(pos, ref, alt)
        hgvs_r = '%s:r.%s' %(transcript, hgvs_nuc)
        return hgvs_r
    
    def _get_hgvs_nuc(self, pos, ref, alt):
        """
        Gets nucleotide level hgvs change (.g and .r).
        """
        hgvs_nuc = ''
        start = pos
        end = str(int(pos) + len(ref) - 1)
        if ref == '-': # Insertion
            hgvs_nuc += '%s_%sins%s' %(str(int(start) - 1), start, alt)
        elif alt == '-': # Deletion
            if len(ref) == 1: # Single base deletion
                hgvs_nuc += '%sdel' %start
            else: # Multiple base deletion
                hgvs_nuc += '%s_%sdel' %(start, end)
        else:
            if len(ref) == 1 and len(alt) == 1: # Substitution
                hgvs_nuc += '%s%s>%s' %(start, ref, alt)
            else: # Deletion-insertion
                hgvs_nuc += '%s_%sdelins%s' %(start, end, alt)
        return hgvs_nuc
    
    def _get_repeat_info(self, s):
        for i in range(1,len(s)+1):
            unit = s[:i]
            if len(s)%len(unit) != 0:
                continue
            else:
                mult = int(len(s)/len(unit))
                if s == unit * mult:
                    return unit, mult
                else:
                    continue
        return s, 1
    
    def _count_seq_tail_repeats(self, seq, unit):
        n = 0
        if len(unit) > 0:
            try:
                while (seq[len(seq)-len(unit)*(n+1):
                           len(seq)-len(unit)*(n)] 
                       == unit):
                    n += 1
            except IndexError:
                pass
        return n
            
    
    def _get_hgvs_p(self, tseq):
        """
        Gets protein level hgvs variant.
        """
        hgvs_ref = ''
        hgvs_so = ''
        hgvs_alt = ''
        if tseq.pref != tseq.palt: # Not synonomous
            repeat_unit, repeat_count = self._get_repeat_info(tseq.palt)
            head_repeat_count = self._count_seq_tail_repeats(tseq.shared_phead,
                                                             repeat_unit)
            if tseq.fs_flag and not(tseq.cterm_ext_flag) and not(tseq.palt_and_tail.startswith('*')): # Frameshift
                hgvs_ref = aa_let_to_abbv(tseq.pref_and_tail[0]) \
                           + str(tseq.ppos_start+1)
                if not('*' in tseq.palt_and_tail):
                    count_to_stop = '?'
                else:
                    count_to_stop = str(len(tseq.palt_and_tail.split('*')[0])+1)
                hgvs_alt = '%sfs*%s' %(aa_let_to_abbv(tseq.palt_and_tail[0]), count_to_stop)
            elif head_repeat_count > 0 and tseq.pref == '': # Repeat or Duplication
                repeat_count += head_repeat_count
                unit_start_index = tseq.ppos_start - len(repeat_unit)
                head_unit = tseq.shared_phead[unit_start_index:]
                if len(head_unit) == 1:
                    hgvs_ref = '%s%d' %(aa_let_to_abbv(head_unit),
                                        unit_start_index+1)
                else:
                    hgvs_ref = '%s%d_%s%d' %(aa_let_to_abbv(head_unit[0]),
                                             unit_start_index+1,
                                             aa_let_to_abbv(head_unit[-1]),
                                             tseq.ppos_start)
                if repeat_count == 2: # Duplication
                    hgvs_so = 'dup'
                else: # Repeat 
                    hgvs_alt = '[%d]' %repeat_count
            elif tseq.cterm_ext_flag: # C-Terminal extension
                full_pref_len = len(tseq.ref_pseq)
                hgvs_ref = 'Ter%d' %full_pref_len
                palt_and_tail = tseq.palt + tseq.shared_ptail
                if palt_and_tail.endswith('*'):
                    full_palt_len = len(tseq.alt_pseq)
                    ext_len = full_palt_len - full_pref_len + 1
                else:
                    ext_len = '?'
                one_abbv_palt = aa_let_to_abbv(tseq.palt[0])
                hgvs_alt = '%sext*%s' %(one_abbv_palt, ext_len)
            else: # Substitution, Insertion, Deletion, Deletion-insertion
                hgvs_alt = aa_let_to_abbv(tseq.palt)
                if tseq.pref_len == 0: # Insertion
                    hgvs_so = 'ins'
                    prev_ppos = tseq.ppos_start
                    next_ppos = tseq.ppos_start + 1
                    try:
                        prev_aa = aa_let_to_abbv(tseq.shared_phead[-1])
                    except IndexError:
                        prev_aa = ''
                    try:
                        next_aa = aa_let_to_abbv(tseq.shared_ptail[0])
                    except IndexError:
                        next_aa = ''
                    if prev_aa and next_aa:
                        hgvs_ref = '%s%d_%s%d' %(prev_aa, prev_ppos, next_aa, next_ppos)
                    elif prev_aa and not(next_aa):
                        hgvs_ref = '%s%d' %(prev_aa, prev_ppos)
                    elif next_aa and not(prev_aa):
                        hgvs_ref = '%s%d' %(next_aa, next_ppos)
                elif tseq.pref_len == 1 or tseq.palt.endswith('*'): # Substitution or single-base Deletion/Deletion-insertion
                    hgvs_ref = aa_let_to_abbv(tseq.pref[0]) + str(tseq.ppos_start+1)
                    if tseq.palt_len == 0: # Deletion, single base
                        hgvs_so = 'del'    
                    elif tseq.palt_len == 1: # Substitution
                        hgvs_so = ''
                    else: # Delins, single base
                        hgvs_so = 'delins'
                else: # Many base Deletion/Deletion-insertion
                    first_aa = aa_let_to_abbv(tseq.pref[0])
                    first_ppos = tseq.ppos_start + 1
                    last_aa = aa_let_to_abbv(tseq.pref[-1])
                    last_ppos = tseq.ppos_start + len(tseq.pref)
                    hgvs_ref = '%s%d_%s%d' %(first_aa, first_ppos, last_aa, last_ppos)
                    if tseq.palt_len == 0: # Deletion
                        hgvs_so = 'del'
                    else: # Deletion-insertion
                        hgvs_so = 'delins'
        else: # Silent
            hit_aa = tseq.shared_phead[tseq.orig_ppos_start-1]
            hgvs_ref = aa_let_to_abbv(hit_aa) + str(tseq.orig_ppos_start)
            hgvs_so = '='
        hgvs_p = '%s:p.(%s%s%s)' %(tseq.protein, hgvs_ref, hgvs_so, hgvs_alt)
        return hgvs_p
    
    
    def annotate(self, input_data):
        out = {
               'genomic':'',
               'rna':'',
               'protein':'',
               'all_rna':'',
               'all_protein':''
               }
        chrom = input_data['chrom']
        pos = input_data['pos']
        ref = input_data['ref_base']
        alt = input_data['alt_base']
        map_parser = AllMappingsParser(input_data['all_mappings'])
        primary_transcript = input_data['transcript']
        
        hgvs_g = self._get_hgvs_g(chrom, pos, ref, alt)
        
        all_hgvs_r = []
        all_hgvs_p = []
        primary_hgvs_r = ''
        primary_hgvs_p = ''
        for mapping in map_parser.get_all_mappings():
            if not(mapping.tchange):
                continue
            q = 'select * from transsequence where ensemblt="%s";' %mapping.transcript
            self.cursor.execute(q)
            r = self.cursor.fetchone()
            if len(r) == 0:
                continue
            rd = dict(zip(self.transsequence_headers,r))
            tseq = TranscriptSequence(rd)
            tseq.set_aligned_protein(mapping.protein)
            tseq.alter_sequence(int(mapping.tpos_start), mapping.tref, mapping.talt)
            hgvs_r = self._get_hgvs_r(mapping.transcript,
                                      mapping.tpos_start+tseq.cds_start,
                                      mapping.tref,
                                      mapping.talt)
            all_hgvs_r.append(hgvs_r)
            hgvs_p = None
            if tseq.protein is not None:
                hgvs_p = self._get_hgvs_p(tseq)
            if hgvs_p is None:
                continue
            all_hgvs_p.append(hgvs_p)
            if mapping.transcript == primary_transcript:
                primary_hgvs_r = hgvs_r
                primary_hgvs_p = hgvs_p
                
        out['genomic'] = hgvs_g
        out['rna'] = primary_hgvs_r
        out['all_rna'] = ','.join(all_hgvs_r)
        out['protein'] = primary_hgvs_p
        out['all_protein'] = ','.join(all_hgvs_p)
        
        return out
    
class TranscriptSequence(object):
    def __init__(self, rowd):
        self.full_seq = rowd['sequence'].upper()
        self.cds_start = rowd['cds_start']-1
        self.cds_end = rowd['cds_stop']
        self.transcript = rowd['ensemblt']
        self.protein = rowd.get('protein')
        self.ref_tseq = self.full_seq[self.cds_start:self.cds_end]
        self.ref_pseq, self.ref_extra = self._translate_bases(self.ref_tseq)
        self.tpos_start = None
        self.orig_ppos_start = None
        self.alt_tseq = None
        self.alt_pseq = None
        self.alt_extra = None
        self.pref = None
        self.palt = None
        self.ppos_start = None
        self.fs_flag = False
    
    def set_aligned_protein(self, protein_name):
        self.protein = protein_name
        
    def alter_sequence(self, tpos_start, ref, alt):
        self.orig_ppos_start = math.floor(tpos_start/3)
        ref = ref.replace('-','')
        alt = alt.replace('-','')
        full_seq_var_start = self.cds_start + tpos_start - 1
        self.alt_tseq = self.full_seq[self.cds_start : full_seq_var_start] \
                        +alt \
                        +self.full_seq[ full_seq_var_start + len(ref) : ]
        self.alt_pseq, self.alt_extra = self._translate_bases(self.alt_tseq)
        head, pref, palt, tail = _trim_sequence(self.ref_pseq, self.alt_pseq)
        # if tail == '*':
        #     pref += '*'
        #     palt += '*'
        #     tail = ''
        self.pref = pref
        self.palt = palt
        self.shared_phead = head
        self.shared_ptail = tail
        self.pref_and_tail = self.pref + self.shared_ptail
        self.palt_and_tail = self.palt + self.shared_ptail
        self.ppos_start = len(head)
        self.ppos_end = self.ppos_start + len(self.pref)
        self.pref_len = len(self.pref)
        self.palt_len = len(self.palt)
        self.fs_flag = (len(ref) - len(alt))%3 != 0
        self.cterm_ext_flag = pref == '*'
        
    def _translate_codons(self, bases): 
        """
        Translates bases in groups of three. Drops trailing bases.
        """
        if not(bases): return ''
        bases = bases.upper()
        aas = ''
        for i, _ in enumerate(bases):
            if i%3 == 2:
                codon_bases = ''.join(bases[i-2:i+1])
                aa = translate_codon(codon_bases, fallback='?')
                aas += aa
                if aa == '*':
                    break
        return aas
        
    def _translate_bases(self, bases): 
        """
        Translates bases in groups of three. Returns trailing bases.
        """
        full_seq_length = len(bases)
        num_extra_bases = full_seq_length % 3
        if num_extra_bases > 0:
            codon_bases = bases[:-num_extra_bases]
            extra_bases = bases[-num_extra_bases:]
        else:
            codon_bases = bases
            extra_bases = ''  
        aas = self._translate_codons(codon_bases)
        return aas, extra_bases
    
def _trim_sequence(a, b):
    """
    Examines two sequences and trims the matching parts of the head and tail
    """
    head = ''
    tail = ''
    while (a and b and (a[0] == b[0])):
        head += a[0]
        a = a[1:]
        b = b[1:]
    while (a and b and (a[-1] == b[-1])):
            tail = a[-1] + tail
            a = a[:-1]
            b = b[:-1]
    return head, a, b, tail

if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()