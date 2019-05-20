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
        
        q = 'select BEB_AF,GIH_AF,ITU_AF,PJL_AF,STU_AF from '\
            +'thousandgenomes_%s where position=%s and refbase="%s" and altbase="%s";' \
            %(chrom, pos, ref, alt)
        self.cursor.execute(q)
        result = self.cursor.fetchone()
        if result:
            out['beb_af'] = result[0] 
            out['gih_af'] = result[1]
            out['itu_af'] = result[2] 
            out['pjl_af'] = result[3] 
            out['stu_af'] = result[4] 
        return out
    def cleanup(self):
        pass

if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()