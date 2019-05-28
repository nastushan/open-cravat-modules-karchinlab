import sys
from cravat import BaseAnnotator
from cravat import InvalidData
from pyliftover import LiftOver

import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def setup(self):
        pass

    def annotate(self, input_data, secondary_data=None):
        out = {}
        input_chrom = input_data['chrom'].lower().replace('chr','')
        input_pos = input_data['pos']
        input_ref = input_data['ref_base']
        input_alt = input_data['alt_base']
        sql_q = 'SELECT Frequencies FROM abraom WHERE Chr="%s" AND Start=%s AND Ref="%s" and Alt="%s";' \
                %(input_chrom, input_pos, input_ref, input_alt)
        self.cursor.execute(sql_q)
        sql_q_result = self.cursor.fetchone()
        if sql_q_result:
            out['allele_freq'] = sql_q_result[0]
            return out
        else:
            return None

    def cleanup(self):
        pass

if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
