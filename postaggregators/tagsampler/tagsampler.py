import sys
import os
from cravat import BasePostAggregator
from cravat import InvalidData
import sqlite3

class CravatPostAggregator (BasePostAggregator):

    def check(self):
        self.cursor.execute('select col_name from sample_header ' +\
                        'where col_name="base_sample_id"')
        return self.cursor.fetchone() != None

    def setup (self):
        self.cursor_a = self.dbconn.cursor()
    
    def cleanup (self):
        self.cursor_a.close()
        
    def annotate (self, input_data):
        uid = str(input_data['base__uid'])
        q = 'select base__sample_id from sample where base__uid=' + uid
        self.cursor_a.execute(q)
        samples = {}
        for row in self.cursor_a.fetchall():
            samples[row[0]] = True
        numsample = len(samples)
        samples = list(samples.keys())
        samples.sort()
        samples = ','.join(samples)
        q = 'select base__tags from mapping where base__uid=' + uid
        self.cursor_a.execute(q)
        tags = ','.join([v[0] for v in self.cursor_a.fetchall()])
        out = {'numsample': numsample, 'samples': samples, 'tags': tags}
        return out

if __name__ == '__main__':
    summarizer = CravatPostAggregator(sys.argv)
    summarizer.run()