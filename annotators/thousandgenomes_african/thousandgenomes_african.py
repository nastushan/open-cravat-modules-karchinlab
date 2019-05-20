import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def annotate(self, input_data):
        out = {}
        chrom = input_data['chrom']
        pos = input_data['pos']
        ref = input_data['ref_base']
        alt = input_data['alt_base']
        
        q = 'select ACB_AF,ASW_AF,ESN_AF,GWD_AF,LWK_AF,MSL_AF,YRI_AF from '\
            +'thousandgenomes_%s where position=%s and refbase="%s" and altbase="%s";' \
            %(chrom, pos, ref, alt)
        self.cursor.execute(q)
        result = self.cursor.fetchone()
        if result:
            out['acb_af'] = result[0] 
            out['asw_af'] = result[1] 
            out['esn_af'] = result[2] 
            out['gwd_af'] = result[3] 
            out['lwk_af'] = result[4] 
            out['msl_af'] = result[5] 
            out['yri_af'] = result[6] 
        return out
    def cleanup(self):
        pass

if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()