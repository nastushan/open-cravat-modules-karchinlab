import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):
    def annotate(self, input_data, secondary_data=None):
        out = None
        # Don't run on alt contigs
        if len(input_data['chrom']) > 5: return None
        # Dont run on non-missense mutations
        ref = input_data['ref_base']
        alt = input_data['alt_base']
        if not(len(ref.replace('-','')) == 1 and len(ref.replace('-','')) == 1): return None
        q = 'select score from {tname} where pos={pos} and alt="{alt}"'.format(
            tname = input_data['chrom'],
            pos = input_data['pos'],
            alt = input_data['alt_base'],
            )
        self.cursor.execute(q)
        r = self.cursor.fetchone()
        if r:
            out = {'score': r[0]}
        return out
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
