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
        self.cursor.execute('select biogrid, id from biogrid_id left join genes on biogrid_id.gname=genes.gname where biogrid_id.gname = ?;', [hugo])
        row = self.cursor.fetchone()
        if row is not None:
            if row[0] is not None:
                rawlist = row[0].split('|')
            else:
                rawlist = []
            glist = []
            for raw in rawlist:
                glist.append(raw[:raw.find('[')])
            glist.sort()
            glist = filter(None, glist)
            out['biogrid'] = row[0]
            out['acts'] = ';'.join(glist)
            out['id'] = row[1]
        return out
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
