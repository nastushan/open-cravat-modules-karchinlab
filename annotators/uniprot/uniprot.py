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
        self.cursor.execute('SELECT acc FROM genes WHERE gname= ?;', [hugo])
        row = self.cursor.fetchone()
        if row is not None:
            out['acc'] = row[0] + '[WEB:]https://www.uniprot.org/uniprot/' + row[0]
        return out
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
