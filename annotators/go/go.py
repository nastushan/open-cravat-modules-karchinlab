import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def annotate(self, input_data):
        out = {}
        hugo = input_data['hugo']
        # if 'go_aspect' in self.conf:
        #     aspect_filter = self.conf['go_aspect'].strip();
        # else:
        #     aspect_filter = 'F';
        
        q = 'SELECT name, go_name.dname, go_name.id, aspect, refer, evidence FROM go_annotation JOIN go_name ON go_annotation.id=go_name.id WHERE hugo="%s";' \
            %(hugo)
        self.cursor.execute(q)
        result = self.cursor.fetchall()
        if result:
            name_list = []
            id_list = []
            aspect_list = []
            ref_list = []
            evi_list = []
            for res in result:
                name_list.append(res[0])
                id_list.append(res[1])
                aspect_list.append(res[2])
                ref_list.append(res[3])
                evi_list.append(res[4])
            out['name'] = ';'.join(name_list)
            out['id'] = ';'.join(id_list)
            out['aspect'] = ';'.join(aspect_list)
            out['ref'] = ';'.join(ref_list)
            out['evidence'] = ';'.join(evi_list)
        return out
    
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()