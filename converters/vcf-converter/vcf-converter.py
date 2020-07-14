from cravat import BaseConverter
from cravat import BadFormatError
from cravat import ExpectedException
from cravat import InvalidData
import re
from collections import OrderedDict
from cravat.inout import CravatWriter
from cravat import constants
import os
import logging
import traceback
import vcf
from io import StringIO
import copy

class CravatConverter(BaseConverter):

    def __init__(self):
        self.format_name = 'vcf'
        self._in_header = True
        self._first_variant = True
        self._buffer = StringIO()
        self._reader = None
        self.addl_cols = [
            {'name':'phred','title':'Phred','type':'string'},
            {'name':'filter','title':'VCF filter','type':'string'},
            {'name':'zygosity','title':'Zygosity','type':'string'},
            {'name':'alt_reads','title':'Alternate reads','type':'int'},
            {'name':'tot_reads','title':'Total reads','type':'int'},
            {'name':'af','title':'Variant allele frequency','type':'float'},
            {'name':'hap_block','title':'Haplotype block ID','type':'int'},
            {'name':'hap_strand','title':'Haplotype strand ID','type':'int'},
        ]

    def check_format(self, f): 
        if f.name.endswith('.vcf'):
            return True
        if f.name.endswith('.vcf.gz'):
            return True
        first_line = f.readline()
        if first_line.startswith('##fileformat=VCF'):
            return True

    def setup(self, f):
        self.logger = logging.getLogger('cravat.converter')
        self.input_path = f.name

    def convert_line(self, l):
        if l.startswith('#'):
            if self._in_header:
                self._buffer.write(l)
            return self.IGNORE
        if self._first_variant:
            self._first_variant = False
            self._in_header = False
            self._buffer.seek(0)
            self._reader = vcf.Reader(self._buffer)
        self._buffer.seek(0)
        self._buffer.truncate()
        self._buffer.write(l)
        self._buffer.seek(0)
        variant = next(self._reader)
        self.logger.info(str(variant))
        wdict_blanks = {}
        for gtn,alt in enumerate(variant.ALT):
            new_pos, new_ref, new_alt = self.trim_variant(variant.POS, variant.REF, alt.sequence)
            wdict_blanks[str(gtn+1)] = {
                'chrom': variant.CHROM,
                'pos': new_pos,
                'ref_base': new_ref,
                'alt_base': new_alt,
                'tags': variant.ID,
                'phred': variant.QUAL,
                'filter': None, #FIXME
            }
        self.logger.info(wdict_blanks)
        wdicts = []
        for call in variant.samples:
            for gt in call.gt_alleles:
                if gt == '0':
                    continue
                wdict = copy.copy(wdict_blanks[gt])
                wdict['sample_id'] = call.sample
                wdict['zygosity'] = 'het' if call.is_het else 'hom'
                wdict['alt_reads'] = None #FIXME
                wdict['tot_reads'] = None #FIXME
                wdict['af'] = None #FIXME
                wdict['hap_block'] = None #FIXME
                wdict['hap_strand'] = None #FIXME
                wdicts.append(wdict)
        return wdicts

    def trim_variant(self, pos, ref, alt):
        if len(ref) == 1 and len(alt) == 1:
            return pos, ref, alt
        ref = list(ref)
        alt = list(alt)
        adj = 0
        while ref and alt and ref[0]==alt[0]:
            adj += 1
            ref.pop(0)
            alt.pop(0)
        while ref and alt and ref[-1]==alt[-1]:
            ref.pop()
            alt.pop()
        ref = ''.join(ref) if ref else '-'
        alt = ''.join(alt) if alt else '-'
        return pos+adj, ref, alt