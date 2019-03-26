import sys
import os
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        q = 'select hugo, role, inheritance, tumor_types_somatic, tumor_types_germline from cgc;'
        self.cursor.execute(q)
        qr = self.cursor.fetchall()
        self.d = {}
        for r in qr:
            self.d[r[0]] = [r[1], r[2], r[3], r[4]]
    
    def annotate(self, input_data):
        out = {}
        hugo = input_data['hugo']
        if hugo in self.d.keys():
            out['class'] = self.d[hugo][0]
            out['inheritance'] = self.d[hugo][1]
            out['tts'] = self.d[hugo][2]
            out['ttg'] = self.d[hugo][3]
            out['link'] = hugo
        
        return out
    
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()