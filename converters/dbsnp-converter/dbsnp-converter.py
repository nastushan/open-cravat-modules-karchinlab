from cravat import BaseConverter
from cravat import BadFormatError
import re
import os
import sqlite3

class CravatConverter(BaseConverter):
    
    def __init__(self):
        self.format_name = 'dbsnp'
        self.rsid_re = re.compile('rs\d+')
        curdir = os.path.dirname(__file__)
        dbpath = os.path.join(curdir,'data','dbsnp.sqlite')
        self.dbconn = sqlite3.connect(dbpath)
        self.cursor = self.dbconn.cursor()
        self.query_template = 'select chrom, pos, ref_len, alt from dbsnp where rsid=?;'
    
    def check_format(self, f):
        for l in f:
            if l.startswith('#'):
                continue
            else:
                break
        return self.rsid_re.match(l) is not None
    
    def setup(self, f):
        pass
    
    def convert_line(self, l):
        if l.startswith('#'):
            return []
        rsid = l.rstrip('\r\n')
        rsnum = int(rsid.replace('rs',''))
        self.cursor.execute(self.query_template, [rsnum])
        out = []
        for r in self.cursor:
            wdict = {}
            chrom, pos, reflen, alt = r
            wdict = {
                'chrom':chrom,
                'pos':pos,
                'ref_base':'N'*reflen,
                'alt_base':alt,
                'tags': None,
                'sample_id': None
            }
        out.append(wdict)
        return out
