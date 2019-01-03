import sys
import os
from cravat import BasePostAggregator
from cravat import InvalidData
import sqlite3

class CravatPostAggregator (BasePostAggregator):

    def check(self):
        self.cursor.execute('select col_name from sample_header ' +\
                            'where col_name="base__zygosity"')
        return self.cursor.fetchone() != None

    def setup (self):
        pass
    
    def annotate (self, input_data):
        uid = str(input_data['base__uid'])
        q = 'select base__sample_id, base__phred, base__filter, ' +\
            'base__zygosity, ' +\
            'base__alt_reads, base__tot_reads, base__af from sample ' +\
            'where base__uid=' + uid
        self.cursor.execute(q)
        phreds = []
        filts = []
        zygosities = []
        altreads = []
        totreads = []
        afs = []
        for row in self.cursor.fetchall():
            (sample, phred, filt, zygosity, altread, totread, af) = row
            phreds.append(phred)
            filts.append(filt)
            zygosities.append(zygosity)
            altreads.append(altread)
            totreads.append(totread)
            afs.append(af)
        phred = ';'.join([str(v) for v in phreds])
        filter = ';'.join([str(v) for v in filts])
        zygosity = ';'.join([str(v) for v in zygosities])
        alt_reads = ';'.join([str(v) for v in altreads])
        tot_reads = ';'.join([str(v) for v in totreads])
        af = ';'.join([str(v) for v in afs])
        out = {'phred': phred, 'filter': filter, 'zygosity': zygosity, 
               'alt_reads': alt_reads, 'tot_reads': tot_reads, 'af': af}
        return out

if __name__ == '__main__':
    summarizer = CravatPostAggregator(sys.argv)
    summarizer.run()
