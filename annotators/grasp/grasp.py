import sys
import os
import sqlite3
from cravat import BaseAnnotator
from cravat.util import get_ucsc_bins

class CravatAnnotator (BaseAnnotator):

    def annotate(self, input_data):
        out = {}
        
        chrom = input_data['chrom']
        pos = input_data['pos']
        
        out = {'nhlbi': [],
               'pmid': [],
               'phenotype': []}
        
        bins = get_ucsc_bins(pos)
        pos = str(pos)
        for bin in bins:
            query = 'select nhlbi, pmid, pvalue, phenotype ' +\
                'from grasp ' +\
                'where chrom="' + chrom +\
                '" and binno=' + str(bin) +\
                ' and pos=' + pos +\
                ' order by pvalue desc;'
            self.cursor.execute(query) 
            results = self.cursor.fetchall()
            if len(results) == 0:
                continue
            for result in results:
                (nhlbi, pmid, pvalue, phenotype) = result
                out['nhlbi'].append(nhlbi)
                out['pmid'].append(pmid)
                pvalue = '{:.4f}'.format(pvalue)
                out['phenotype'].append(phenotype + '(' + str(pvalue) + ')')
        out['nhlbi'] = ','.join([str(v) for v in out['nhlbi']])
        out['pmid'] = ','.join([str(v) for v in out['pmid']])
        out['phenotype'] = ','.join([str(v) for v in out['phenotype']])
        if out['phenotype'] == '':
            out = None
        return out

if __name__ == '__main__':
    module = CravatAnnotator(sys.argv)
    module.run()