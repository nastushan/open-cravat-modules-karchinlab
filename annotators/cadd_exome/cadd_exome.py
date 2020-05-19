import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        self.cursor.execute('select * from prefixes;')
        self.which_col = {}
        for row in self.cursor:
            ref, alt, prefix = row
            self.which_col[ref+alt] = prefix
        self.cursor.execute('select name from sqlite_master where type="table" and name like "chr%";')
        self.valid_chroms = set([row[0] for row in self.cursor])

    def annotate(self, input_data, secondary_data=None):
        chrom = input_data['chrom']
        if chrom not in self.valid_chroms:
            return
        prefix_key = input_data['ref_base']+input_data['alt_base']
        prefix = self.which_col.get(prefix_key)
        score_col = prefix+'_score'
        phred_col = prefix+'_phred'
        pos = input_data['pos']
        q = f'select {score_col}, {phred_col} from {chrom} where pos={pos}'
        self.cursor.execute(q)
        row = self.cursor.fetchone()
        if row:
            return {'score':row[0],'phred':row[1]}
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
