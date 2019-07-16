import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def annotate(self, input_data):
        out = {}
        chrom = input_data['chrom']
        pos = input_data['pos']
        ref = input_data['ref_base']
        alt = input_data['alt_base']
        
        q = '''select global, AFR, AMR, EAS, EUR, SAS from %s where pos=%s and ref="%s" and alt="%s";''' \
            %(chrom, pos, ref, alt)
        self.cursor.execute(q)
        result = self.cursor.fetchone()
#        result = self.cursor.fetchall()
        if result:
            out['af'] = result[0] 
            out['afr_af'] = result[1] 
            out['amr_af'] = result[2] 
            out['eas_af'] = result[3] 
            out['eur_af'] = result[4] 
            out['sas_af'] = result[5] 
        return out
    def cleanup(self):
        pass

if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()