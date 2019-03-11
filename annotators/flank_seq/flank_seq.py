import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os
import requests
from bowtie_index import BowtieIndexReference

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        self.server_url = 'https://rest.ensembl.org'
        print(self.data_dir)
        fprefix = 'GCA_000001405.15_GRCh38_no_alt_analysis_set'
        prefix = os.path.join(self.data_dir,fprefix)
        self.btr = BowtieIndexReference(prefix)
    
    def annotate(self, input_data, secondary_data=None):
        out = {}
        chrom = input_data['chrom']
        start = input_data['pos']
        ref_bases = input_data['ref_base'].replace('-','')
        alt_bases = input_data['alt_base'].replace('-','')
        end=start+len(ref_bases)+1
        nflank = self.conf['options']['flanking_bases']
        range_start = start - nflank
        range_end = end + nflank
        range_len = range_end - range_start
        ref_seq = self.btr.get_stretch(chrom, range_start - 1, range_len)
        if ref_seq != '':
            alt_seq = ref_seq[:nflank] + alt_bases + ref_seq[nflank+len(ref_bases):]
            out['ref_seq'] = ref_seq
            out['alt_seq'] = alt_seq
        return out
 
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
