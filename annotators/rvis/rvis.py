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
        hugo = input_data['hugo']
        self.cursor.execute('SELECT rvis_evs, rvis_perc_evs, rvis_fdr_exac, rvis_exac, rvis_perc_exac FROM genes WHERE gname= ?;', [hugo])
        row = self.cursor.fetchone()
        if row is not None:
            out['rvis_evs'] = chkCast(row[0])
            out['rvis_perc_evs'] = chkCast(row[1])
            out['rvis_fdr_exac'] = chkCast(row[2])
            out['rvis_exac'] = chkCast(row[3])
            out['rvis_perc_exac'] = chkCast(row[4])
        return out
    
    def cleanup(self):
        pass

def chkCast(item):
    if item is not None:
        return float(item)
    else:
        return item
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()