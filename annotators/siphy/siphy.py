import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        assert isinstance(self.dbconn, sqlite3.Connection)
        assert isinstance(self.cursor, sqlite3.Cursor)
    
    def annotate(self, input_data, secondary_data=None):
        out = {}
        stmt = 'SELECT pi,logodds,logodds_rank FROM {chr} WHERE pos = {pos} AND alt = "{alt}"'.format(chr=input_data["chrom"], pos=int(input_data["pos"]), alt = input_data["alt_base"])
        self.cursor.execute(stmt)
        row = self.cursor.fetchone()
        if row is not None:
            pi = str(row[0]).replace(':', ';')
            out['pi'] = pi
            out['logodds'] = float(row[1])
            out['logodds_rank'] = float(row[2])
        return out
    
    def cleanup(self):
        self.dbconn.close()
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()