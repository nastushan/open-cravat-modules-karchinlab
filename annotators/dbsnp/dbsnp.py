import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os
from cravat.util import get_ucsc_bins, reverse_complement

class CravatAnnotator(BaseAnnotator):

    def annotate(self, input_data):
        out = None
        chrom = input_data['chrom']
        pos = input_data['pos']
        ref_len = len(input_data['ref_base'])
        alt = input_data['alt_base']
        sql = ("SELECT snp FROM {} "
                "WHERE pos='{}'"
                " AND ref_len='{}'"
                " AND alt='{}'").format(chrom, pos, ref_len, alt)
        q = self.cursor.execute(sql)
        snp_ids = ','.join(['rs' + str(i[0]) for i in q.fetchall()])
        if snp_ids == "":
            return out
        out = {}
        out['snp'] = snp_ids
        return out
    
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
