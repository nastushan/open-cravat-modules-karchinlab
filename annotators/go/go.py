import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def annotate(self, input_data):
        out = {}
        hugo = input_data['hugo']
        if 'go_aspect' in self.conf:
            aspect_filter = self.conf['go_aspect'].strip();
        else:
            aspect_filter = 'F';
        
        q = 'SELECT name, go_name.go_id, go_aspect FROM go_annotation JOIN go_name ON go_annotation.go_id=go_name.go_id WHERE hugo="%s";' \
            %(hugo)
        self.cursor.execute(q)
        result = self.cursor.fetchall()
        if result:
            list = []
            idlist = []
            alist = []
            for res in result:
                if res[2] in aspect_filter:
                    list.append(res[0])
                    idlist.append(res[1])
                    alist.append(res[2])
            out['name'] = ';'.join(list)
            out['id'] = ';'.join(idlist)
            out['aspect'] = ';'.join(alist)
        return out
    
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()