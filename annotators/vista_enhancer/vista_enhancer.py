import sys
import os
import sqlite3
from cravat import BaseAnnotator
from cravat import InvalidData
from cravat.util import get_ucsc_bins

class CravatAnnotator (BaseAnnotator):

    def annotate(self, input_data):
        out = {}
        
        chrom = input_data['chrom']
        pos = input_data['pos']
        features = [] 
        q = 'select feature from data where chrom="{chrom}" and start<={pos} and end>={pos};'.format(
            chrom=chrom,
            pos=pos
        )
        self.cursor.execute(q)
        print(q) 
        features = [r[0].strip() for r in self.cursor if r[0] is not None]
        out['features'] = ','.join(features)
        print(out)
        return out
        
if __name__ == '__main__':
    module = CravatAnnotator(sys.argv)
    module.run()
