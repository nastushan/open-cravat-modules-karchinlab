import sys
import os
from cravat import BasePostAggregator
from cravat import InvalidData
import sqlite3

class CravatPostAggregator (BasePostAggregator):

    def check(self):
        self.cursor.execute('select col_name from sample_header ' +\
                            'where col_name="base__zygosity"')
        has_zygosity = self.cursor.fetchone() is not None
        self.cursor.execute('select colval from info where colkey="_converter_format"')
        is_vcf = self.cursor.fetchone()[0] == 'vcf'
        return has_zygosity and not(is_vcf)

    def setup (self):
        pass
    
    def cleanup (self):
        pass
        
    def annotate (self, input_data):
        uid = str(input_data['base__uid'])
        q = 'select base__zygosity from sample where base__uid=?'
        self.cursor.execute(q,(uid,))
        out = {'zygosity': ';'.join([r[0] for r in self.cursor])}
        return out

if __name__ == '__main__':
    summarizer = CravatPostAggregator(sys.argv)
    summarizer.run()
