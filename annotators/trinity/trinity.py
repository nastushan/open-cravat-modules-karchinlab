import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):    
    def annotate(self, input_data):
        q = 'SELECT Rnaedit FROM trinity WHERE chrom = "{Chrom}" AND pos = {Pos} AND alt = "{Alt}" AND ref = "{Ref}"'.format(Chrom = input_data["chrom"] ,Pos=int(input_data["pos"]), Alt = input_data["alt_base"], Ref = input_data["ref_base"])
        self.cursor.execute(q)
        row = self.cursor.fetchone()
        if row:
            Rnaedit = str(row[0]).replace('@', '; ')
            out = {'Rnaedit': Rnaedit}
        else:
            out = None
        return out

    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
    
   
        