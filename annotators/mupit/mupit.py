import sys
import os
from cravat import BaseAnnotator
from cravat import InvalidData

class CravatAnnotator(BaseAnnotator):

    def annotate (self, input_data):
        out = {}
        allowed_sos = ['MIS', 'INI', 'IND']
        sos = input_data['mapping_parser'].get_uniq_sos()
        proceed = False
        for so in sos:
            if so in allowed_sos:
                proceed = True
                break
        if proceed == False:
            return
        chrom = input_data['chrom']
        pos = str(input_data['pos'])
        sql = 'select * from mupit where ' +\
            'chrom="' + chrom + '" and ' +\
            'start<=' + pos + ' and ' +\
            'stop>=' + pos
        self.cursor.execute(sql)
        ret = self.cursor.fetchone()
        if ret != None:
            link = 'http://www.cravat.us/MuPIT_Interactive?gm=' +\
                chrom + ':' + pos
            out = {'link': link, 'hugo': input_data['hugo']}
            return out

    def build_gene_collection (self, hugo, input_data, gene_data):
        link = input_data['link']
        if link != None:
            gm = link.split('=')[1]
            if gm not in gene_data[hugo]['link']:
                gene_data[hugo]['link'].append(gm)
    
    def summarize_by_gene (self, hugo, gene_collection):
        input_data = gene_collection[hugo]
        gm = ','.join(input_data['link'])
        if gm == '':
            out = None
        else:
            link = 'http://www.cravat.us/MuPIT_Interactive?gm=' + gm
            out = {'link': link}
        return out

if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()