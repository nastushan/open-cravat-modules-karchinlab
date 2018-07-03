import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os
import stouffer

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        pval_path = os.path.join(self.annotator_dir,'data','pvals.txt')
        self.pvals = {}
        sig3_round = lambda x: float('{:.3g}'.format(float(x)))
        with open(pval_path) as f:
            f.readline()
            for l in f:
                toks = l.strip('\r\n').split('\t')
                score = float(toks[0])
                pval = sig3_round(toks[1])
                self.pvals[score] = pval
    
    def annotate(self, input_data):
        out = {}
        ref_base = input_data['ref_base']
        alt_base = input_data['alt_base']
        single_base = len(ref_base) == 1 and len(alt_base) == 1
        indel = ref_base == '-' or alt_base == '-'
        snv = single_base and not(indel)
        if not(snv):
            return out
        chrom = input_data['chrom']
        pos = input_data['pos']
        q = 'select c.score, t.transcript, t.alen from '+chrom+' as c '\
            +'join transcript as t '\
            +'on c.tid = t.tid '\
            +'where c.pos='+str(pos)+' and '\
            +'c.alt="'+alt_base+'";'
        self.cursor.execute(q)
        rows = self.cursor.fetchall()
        if len(rows) > 0:
            results = []
            max_alen_index = rows.index(max(rows, key=lambda row: row[2]))
            for i, row in enumerate(rows):
                score = row[0]
                transc = row[1]
                pvalue = self.pvals.get(score, 0.0)
                result = '{0}:({1:.3f}:{2:.3g})'.format(transc, score, pvalue)
                if i == max_alen_index:
                    out['score'] = score
                    out['transcript'] = transc
                    out['pval'] = pvalue
                    result = '*'+result
                results.append(result)
            out['results'] = (',').join(results)
        return out
    
    def build_gene_collection (self, hugo, input_data, gene_data):
        score = input_data['score']
        pval = input_data['pval']
        if hugo not in gene_data:
            gene_data[hugo] = {'score': [], 'pval': []}
        if score != None:
            gene_data[hugo]['score'].append(score)
        if pval != None:
            gene_data[hugo]['pval'].append(pval)
    
    def summarize_by_gene (self, hugo, gene_collection):
        out = None
        input_data = gene_collection[hugo]
        scores = input_data['score']
        pvals_non_unique = input_data['pval']
        pvals = list(set(pvals_non_unique))
        if len(scores) > 0:
            out = {}
            out['max_score'] = max(scores)
            out['mean_score'] = round(sum(scores)/len(scores),3)
            if len(pvals) > 0:
                raw_gene_pval = stouffer.stouffer(pvals)[1]
                gene_pval = round(raw_gene_pval, 3)
                out['gene_pval'] = gene_pval
            else:
                out['gene_pval'] = None
        return out

if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()