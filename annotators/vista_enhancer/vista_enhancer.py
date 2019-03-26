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
        element = ""
        q = 'select features, element from data where chrom="{chrom}" and start<={pos} and end>={pos};'.format(
            chrom=chrom,
            pos=pos
        )
        self.cursor.execute(q)
        for r in self.cursor:
            print(r[1])
            if r[0] is not None:
                features.append(r[0].strip())
                element = r[1].strip()
        out['features'] = ','.join(features)
        out['element'] =element 
        return out
        
if __name__ == '__main__':
    module = CravatAnnotator(sys.argv)
    module.run()
