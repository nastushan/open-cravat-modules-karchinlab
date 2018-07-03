import sys
import os
from cravat import BaseAnnotator
from cravat import InvalidData

class CravatAnnotator(BaseAnnotator):

    def annotate (self, input_data):
        out = {}
        hugo = input_data['hugo']
        sql = 'select n, term from pubmed where hugo="' + hugo + '"'
        self.cursor.execute(sql)
        ret = self.cursor.fetchone()
        if ret != None and ret[0] != 0:
            (n, term) = ret
            out = {'n': n, 
                   'term': 'http://www.ncbi.nlm.nih.gov/pubmed?term=' + term}
        return out

if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()