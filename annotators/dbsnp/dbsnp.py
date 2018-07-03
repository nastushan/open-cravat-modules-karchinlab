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
        sql = 'select * from sqlite_master where name="' + chrom + '"'
        self.cursor.execute(sql)
        if self.cursor.fetchone() == None:
            return out
        start = input_data['pos']
        ref = input_data['ref_base']
        if ref == '-':
            end = start
        else:
            end = start + len(ref) - 1
        length = len(ref)
        bin = get_ucsc_bins(start, end)[0]
        alt = input_data['alt_base']
        q = 'select name, strand, observed from %s where bin=%s and chromStart=%s and chromEnd=%s and refNCBI="%s"'%(chrom, bin, start, end, ref)
        self.cursor.execute(q)
        results = self.cursor.fetchall()
        if results == None:
            return out
        out = {}
        for row in results:
            (name, strand, observed) = row
            obs_alts = observed.split('/')
            for obs_alt in obs_alts:
                if strand == '-':
                    try:
                        obs_alt = reverse_complement(obs_alt)
                    except KeyError:
                        pass
                if obs_alt == alt:
                    out['snp'] = name
                    return out
        if len(list(out.keys())) == 0:
            return None
        return out
    
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
