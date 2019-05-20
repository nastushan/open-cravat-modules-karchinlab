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
        
        q = 'select CEU_AF,FIN_AF,GBR_AF,IBS_AF,TSI_AF from '\
            +'thousandgenomes_%s where position=%s and refbase="%s" and altbase="%s";' \
            %(chrom, pos, ref, alt)
        self.cursor.execute(q)
        result = self.cursor.fetchone()
        if result:
            out['ceu_af'] = result[0] 
            out['fin_af'] = result[1] 
            out['gbr_af'] = result[2] 
            out['ibs_af'] = result[3] 
            out['tsi_af'] = result[4] 
        return out
    def cleanup(self):
        pass

if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()