import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def annotate(self, input_data, secondary_data=None):
        chrom = input_data['chrom'].replace('chr','')
        q = 'select score from revel where chrom="' + chrom + '" and pos=' + str(input_data['pos']) + ' and ref="' + input_data['ref_base'] + '" and alt="' + input_data['alt_base'] + '"'
        self.cursor.execute(q)
        r = self.cursor.fetchone()
        if r:
            out = {'score': r[0]}
        else:
            out = None
        return out
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
