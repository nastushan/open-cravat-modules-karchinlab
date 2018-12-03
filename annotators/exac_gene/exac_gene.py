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
        self.cursor.execute('SELECT exac_pli,exac_prec,exac_pnull,exac_nontcga_pli,exac_nontcga_prec,exac_nontcga_pnull,exac_nonpsych_pli,exac_nonpsych_prec,exac_nonpsych_pnull,exac_del_score,exac_dup_score,exac_cnv_score,exac_cnv_flag FROM genes WHERE gname= ?;', [hugo])
        row = self.cursor.fetchone()
        if row is not None:
            out['exac_pli'] = self.myCast(row[0])
            out['exac_prec'] = self.myCast(row[1])
            out['exac_pnull'] = self.myCast(row[2])
            out['exac_nontcga_pli'] = self.myCast(row[3])
            out['exac_nontcga_prec'] = self.myCast(row[4])
            out['exac_nontcga_pnull'] = self.myCast(row[5])
            out['exac_nonpsych_pli'] = self.myCast(row[6])
            out['exac_nonpsych_prec'] = self.myCast(row[7])
            out['exac_nonpsych_pnull'] = self.myCast(row[8])
            out['exac_del_score'] = self.myCast(row[9])
            out['exac_dup_score'] = self.myCast(row[10])
            out['exac_cnv_score'] = self.myCast(row[11])
            out['exac_cnv_flag'] = row[12]
        return out
    
    def cleanup(self):
        pass
    
    def myCast(self, item):
        if item is None:
            return item
        else:
            return float(item)
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()