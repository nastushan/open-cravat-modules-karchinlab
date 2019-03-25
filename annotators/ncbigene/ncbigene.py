import sys
from cravat import BaseAnnotator
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def annotate(self, input_data):
        out = {}
        hugo = input_data['hugo']
        q = 'SELECT description, id FROM ncbigene WHERE gene_symbol="%s";' %(hugo)
        self.cursor.execute(q)
        result = self.cursor.fetchall()
        if result:
            descs = []
            entrez = None
            for res in result:
                descs.append(res[0])
                entrez = res[1]
            out['ncbi_desc'] = ';'.join(descs)
            out['entrez'] = entrez
        return out

if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()