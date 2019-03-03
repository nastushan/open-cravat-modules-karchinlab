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
        self.cursor.execute('SELECT ess_gene, ess_gene_crispr, ess_gene_crispr2, ess_gene_gene_trap, indispensability_score, indispensability_pred  FROM genes WHERE gname= ?;', [hugo])
        row = self.cursor.fetchone()
        if row is not None:
            out['ess_gene'] = row[0]
            out['ess_gene_crispr'] = row[1]
            out['ess_gene_crispr2'] = row[2]
            out['ess_gene_gene_trap'] = row[3]
            out['indispensability_score'] = row[4]
            out['indispensability_pred'] = row[5]
        return out
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
