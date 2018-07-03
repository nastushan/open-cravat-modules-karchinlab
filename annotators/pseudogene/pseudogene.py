import sys
import os
import sqlite3
from cravat import BaseAnnotator
from cravat.util import get_ucsc_bins

class CravatAnnotator (BaseAnnotator):

    def annotate(self, input_data):
        out = {}
        
        chrom = input_data['chrom']
        pos = input_data['pos']
        
        out = {'pseudogene_hugo': [],
               'pseudogene_transcript': []}
        
        bins = get_ucsc_bins(pos)
        pos = str(pos)
        for bin in bins:
            query = 'select tid ' +\
                'from exon ' +\
                'where chrom="' + chrom +\
                '" and binno=' + str(bin) +\
                ' and start<=' + pos +\
                ' and end>=' + pos
            self.cursor.execute(query) 
            results = self.cursor.fetchall()
            
            if len(results) == 0:
                continue
            
            for result in results:
                tid = str(result[0])
                query = 'select enst, hugo from transcript where ' +\
                    'tid=' + tid
                self.cursor.execute(query)
                (enst, hugo) = self.cursor.fetchone()
                out['pseudogene_hugo'].append(hugo)
                out['pseudogene_transcript'].append(enst)
        
        out['pseudogene_hugo'] = ','.join(out['pseudogene_hugo'])
        out['pseudogene_transcript'] = ','.join(out['pseudogene_transcript'])
        
        return out

if __name__ == '__main__':
    module = CravatAnnotator(sys.argv)
    module.run()