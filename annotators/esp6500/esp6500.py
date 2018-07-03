import sys
import os
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3

class CravatAnnotator(BaseAnnotator):

    def annotate(self, input_data):
        out = {}
        chrom = input_data['chrom'].lower()
        pos = input_data['pos']
        ref = input_data['ref_base']
        alt = input_data['alt_base']
        
        aa = ''
        ea = ''
        
        q = 'select ea_pop_af, aa_pop_af from esp6500_%s where position=%s and refbase="%s" and altbase="%s";' \
            %(chrom, pos, ref, alt)
        self.cursor.execute(q)
        qr = self.cursor.fetchone()
        if qr:
            ea = qr[0]
            aa = qr[1]
            out['ea_pop_af'] = ea
            out['aa_pop_af'] = aa
            return out
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()