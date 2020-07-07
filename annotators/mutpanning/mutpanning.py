import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os
import webbrowser

class CravatAnnotator(BaseAnnotator):
    def annotate(self, input_data):
        q ='select No_Cancer_Types, M_Frequency, Best_Q_Value, Supporting_Literature, TCGA_Marker_Papers, dNdS_Study, Tumor_Portal, Bailey_Database, Cancer_Types ' + \
                            'from Genes where Hugo="%s";'%input_data['hugo']
        self.cursor.execute(q)
        row = self.cursor.fetchone()

        if row:
            out = {'No_Cancer_Types': row[0] , 'Max_Frequency': row[1], 'Best_Q_Value': row[2], 'Supporting_Literature': row[3], 'TCGA_Marker_Papers': row[4], 'dNdS_Study': row[5] , 'Tumorportal' : row[6], 'Bailey_Database': row[7], 'Cancer_Type': row[8]}
            if row[3] == 1:
                out['Supporting_Literature'] = 'Yes'
            else: 
                out['Supporting_Literature'] = None

            if row[4] == 1:
                out['TCGA_Marker_Papers'] = '32015527'
            else: 
                out['TCGA_Marker_Papers'] = None
            
            if row[5] == 1:
                out['dNdS_Study'] = '29906452'
            else: 
                out['dNdS_Study'] = None

            if row[6] == 1:
                out['Tumorportal'] = '24390350'
            else: 
                out['Tumorportal'] = None

            if row[7] == 1:
                out['Bailey_Database'] = '30096302' 
            else: 
                out['Bailey_Database'] = None

        else:
            out = None
        return out

        
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()