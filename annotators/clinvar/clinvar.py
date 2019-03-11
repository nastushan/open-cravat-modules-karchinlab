import sys
import os
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3

class CravatAnnotator(BaseAnnotator):

    def annotate(self, input_data):
        chrom = input_data['chrom']
        pos = input_data['pos']
        ref_base = input_data['ref_base']
        alt_base = input_data['alt_base']
        if ref_base == '-' or alt_base == '-':
            q = 'select sig, disease_refs, disease_names, rev_stat, id from ' +\
                chrom + ' where pos=' + str(pos)
        else:
            q = 'select sig, disease_refs, disease_names, rev_stat, id from ' +\
                chrom + ' where pos=' + str(pos) + ' and ref="' +\
                ref_base + '" and alt="' + alt_base + '"'

        sig = ''
        refs = ''
        diseases = ''
        rev = ''
        id = ''

        self.cursor.execute(q)
        qr = self.cursor.fetchone()
        if qr is not None:
            sig = qr[0]
            refs = qr[1]
            diseases = qr[2]
            rev = qr[3]
            id = qr[4]

        return {'sig':sig,
                'disease_refs':refs,
                'disease_names':diseases,
                'rev_stat':rev,
                'id': id}
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
