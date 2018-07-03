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
        
        out = {'ncrnaclass': [],
               'ncrnaname': []}
        
        bins = get_ucsc_bins(pos)
        pos = str(pos)
        for bin in bins:
            query = 'select class, name from ncrna ' +\
                'where binno=' + str(bin) + ' and ' +\
                'chrom="' + chrom + '" and ' +\
                'start<=' + pos + ' and end>=' + pos
            self.cursor.execute(query) 
            results = self.cursor.fetchall()
            
            if len(results) == 0:
                continue
            
            for result in results:
                (ncrna_class, ncrna_name) = result
                out['ncrnaclass'].append(ncrna_class)
                out['ncrnaname'].append(ncrna_name)
        
        out['ncrnaclass'] = ','.join(out['ncrnaclass'])
        out['ncrnaname'] = ','.join(out['ncrnaname'])
        
        return out
        
if __name__ == '__main__':
    module = CravatAnnotator(sys.argv)
    module.run()