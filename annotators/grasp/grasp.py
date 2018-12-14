import sys
import os
import sqlite3
from cravat import BaseAnnotator

class CravatAnnotator (BaseAnnotator):

    def setup(self):
        self.query_template = 'select nhlbi, pmid, pvalue, phenotype from grasp where chrom=? and pos=? order by pvalue desc;'

    def annotate(self, input_data):
        out = {}
        
        chrom = input_data['chrom']
        pos = input_data['pos']
        
        out = {'nhlbi': [],
               'pmid': [],
               'phenotype': []}
        
        self.cursor.execute(self.query_template, [chrom, pos]) 
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