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
        reflen = len(ref_base)
        altlen = len(alt_base)
        if ref_base == '-' or alt_base == '-':
            q = 'select clin_sig, disease_refs, diseases from clinvar_' +\
                chrom + ' where position=' + str(pos)
        else:
            q = 'select clin_sig, disease_refs, diseases from clinvar_' +\
                chrom + ' where position=' + str(pos) + ' and refbase="' +\
                ref_base + '" and altbase="' + alt_base + '"'

        sig = ''
        refs = ''
        diseases = ''

        self.cursor.execute(q)
        qr = self.cursor.fetchone()
        if qr:
            sig = qr[0]
            refs = ';'.join(qr[1].split(','))
            diseases = qr[2]

        return {'sig':sig,
                'refs':refs,
                'diseases':diseases}
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
