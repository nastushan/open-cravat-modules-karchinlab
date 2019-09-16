import sys
import os
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        q = 'select gene, class from cgl'
        self.cursor.execute(q)
        qr = self.cursor.fetchall()
        self.d = {}
        for r in qr:
            self.d[r[0]] = r[1]
    
    def annotate(self, input_data):
        out = {}
        hugo = input_data['hugo']
        if hugo in self.d:
            cglclass = self.d[hugo]
        else:
            cglclass = ''
        out['class'] = cglclass
        
        return out
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()