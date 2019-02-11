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
        
        q = 'select Target_gene_name from capture where PIR_Chr="{cnum}" and PIR_Start<={pos} and PIR_End>={pos};'.format(cnum = chrom.replace('chr',''), pos=pos)
        print(q)
        self.cursor.execute(q)
        targets = [r[0] for r in self.cursor if r[0] is not None]
        out['targets'] = ';'.join(targets)
        return out
        
if __name__ == '__main__':
    module = CravatAnnotator(sys.argv)
    module.run()
