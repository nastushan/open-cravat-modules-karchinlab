import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def setup(self):
        pass

    def annotate(self, input_data, secondary_data=None):
        out = {}

        # get input details
        input_chrom = input_data['chrom'].lower().replace('chr','')
        input_pos = input_data['pos']
        input_ref = input_data['ref_base']
        input_alt = input_data['alt_base']

        sql_q = 'SELECT  African, European, Middle_Eastern, CS_Asian, East_Asian, Oceanian, Native_American FROM hgdp_table WHERE CHR="%s" AND POS=%s AND REF="%s" and ALT="%s";' \
            %(input_chrom, input_pos, input_ref, input_alt)
        self.logger.warn(sql_q)
        self.cursor.execute(sql_q)
        sql_q_result = self.cursor.fetchone()
        if sql_q_result:
            out['african_allele_freq'] = sql_q_result[0]
            out['european_allele_freq'] = sql_q_result[1]
            out['middle_eastern_allele_freq'] = sql_q_result[2]
            out['cs_asian_allele_freq'] = sql_q_result[3]
            out['east_asian_allele_freq'] = sql_q_result[4]
            out['oceanian_allele_freq'] = sql_q_result[5]
            out['native_american_allele_freq'] = sql_q_result[6]
            return out
        else:
            return None

    def cleanup(self):
        pass

if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
