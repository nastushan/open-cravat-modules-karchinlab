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
        stmt = 'SELECT uk10k_twins_ac, uk10k_twins_af, uk10k_alspac_ac, uk10k_alspac_af FROM {chr} WHERE pos = {pos} AND alt = "{alt}"'.format(chr=input_data["chrom"], pos=int(input_data["pos"]), alt = input_data["alt_base"])
        self.cursor.execute(stmt)
        row = self.cursor.fetchone()
        if row is not None:
            out['uk10k_twins_ac'] = self.myCast(row[0])
            out['uk10k_twins_af'] = self.myCast(row[1])
            out['uk10k_alspac_ac'] = self.myCast(row[2])
            out['uk10k_alspac_af'] = self.myCast(row[3])
        return out
    
    def cleanup(self):
        self.dbconn.close()
        pass

    def myCast(self, item):
        if item is None:
            return item
        else:
            return float(item)
    
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()