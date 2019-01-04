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
        self.cursor.execute('SELECT biogrid FROM genes WHERE gname= ?;', [hugo])
        row = self.cursor.fetchone()
        if row is not None:
            rawlist = row[0].split('|')
            glist = []
            for raw in rawlist:
                glist.append(raw[:raw.find('[')])
            out['biogrid'] = row[0]
            out['genes'] = ';'.join(glist)
        return out
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
