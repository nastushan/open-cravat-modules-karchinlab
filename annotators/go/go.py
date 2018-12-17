import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def annotate(self, input_data):
        out = {}
        hugo = input_data['hugo']
        
        q = 'SELECT dname, id, aspect, refer, evi FROM go_annotation JOIN go_name ON go_annotation.name=go_name.name WHERE go_name="%s";' \
            %(hugo)
        self.cursor.execute(q)
        result = self.cursor.fetchall()
        if result:
            id_list = []
            aspect_list = []
            ref_list = []
            evi_list = []
            for res in result:
                id_list.append(res[1])
                aspect_list.append(res[2])
                ref_list.append(res[3])
                evi_list.append(res[4])
            out['name'] = res[0]
            out['id'] = ';'.join(id_list)
            out['aspect'] = ';'.join(aspect_list)
            out['refer'] = ';'.join(ref_list)
            out['evi'] = ';'.join(evi_list)
        return out
    
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()