import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        pass

    def annotate(self, input_data, secondary_data=None):
        out = {}

        chrom = input_data['chrom']
        pos = input_data['pos']
        ref = input_data['ref_base']
        alt = input_data['alt_base']

        self.cursor.execute('select transcript from eqtls where chrom=? and pos=? and ref=? and alt=?', [chrom, pos, ref, alt])
        r = self.cursor.fetchone()
        if r:
            out['gene']= r[0]
        return out
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
