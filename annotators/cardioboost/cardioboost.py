import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):
    
    def annotate(self, input_data, secondary_data=None):
        q = 'select pathogenicity, classification, Phenotype from cardio where chrom = "{chrom}" and pos = {pos} and ref = "{ref}" and alt = "{alt}"'.format(
            chrom = input_data["chrom"] ,pos=int(input_data["pos"]), alt = input_data["alt_base"], ref = input_data["ref_base"])
        print(q)
        self.cursor.execute(q)
        rows = self.cursor.fetchall()
        out = {}
        for row in rows:
            if row[2] == 'Cardiomyopathy':
                a = round(row[0], 4)
                a = str(a)
                b = '; ' + row[1]
                c = a + b
                out['cardiomyopathy'] = c
                
            elif row[2] == 'Arrhthymias':
                a = round(row[0], 4)
                a = str(a)
                b = '; ' + row[1]
                c = a + b
                out['arrhthymias'] = c
                
                
        return out
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()

 