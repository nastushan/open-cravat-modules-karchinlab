import sys
import os
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3

class CravatAnnotator(BaseAnnotator):

    def annotate(self, input_data):
        self.cursor.execute('select rationale, agents_therapy ' +
                            'from target where gene="%s";'%input_data['hugo'])
        row = self.cursor.fetchone()
        if row:
            out = {'rationale': row[0], 'therapy': row[1]}
        else:
            out = None
        return out
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()