import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        pass
        self.chroms = set(['chr'+str(n) for n in range(1,23)]+['chrX','chrY','chrM'])
    
    def annotate(self, input_data, secondary_data=None):
        out = {}
        chrom = input_data['chrom']
        pos = input_data['pos']
        ref = input_data['ref_base']
        alt = input_data['alt_base']
        if (len(ref) != 1 and len(alt) != 1) or (chrom not in self.chroms):
            return out
        self.cursor.execute(f'select score, med, seqs from {chrom} where pos=? and ref=? and alt=?', [pos, ref, alt])
        r = self.cursor.fetchone()
        if r:
            out['score'], out['med'], out['seqs'] = r
            if out['score'] <= 0.05:
                out['prediction'] = 'DAMAGING'
            else:
                out['prediction'] = 'TOLERATED'
            if out['med'] <= 3.25:
                out['confidence'] = 'HIGH'
            else:
                out['confidence'] = 'LOW'
        return out
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()