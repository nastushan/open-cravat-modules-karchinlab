import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        pass
    
    def annotate(self, input_data):
        out = {}
        cols = [
            'disease',
            'pmid',
            'init_samp',
            'rep_samp',
            'risk_allele',
            'pval',
            'or_beta',
            'ci'
        ]
        q = 'select {} from gwas where chrom="{}" and pos={}'.format(
            ', '.join(cols),
            input_data['chrom'],
            input_data['pos']
        )
        self.cursor.execute(q)
        qr = self.cursor.fetchone()
        if qr is not None:
            out = dict(zip(cols, qr))
        return out
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()