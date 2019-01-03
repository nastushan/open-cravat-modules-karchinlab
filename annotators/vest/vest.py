import sys
import os
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import re
from cravat.inout import AllMappingsParser
import stouffer

class CravatAnnotator(BaseAnnotator):

    def setup(self):
        pvalue_basedir = os.path.join(self.data_dir,'VESTpvalue')
        self.pvalue_table = {}
        self.pvalue_table['MIS'] = self.get_pval_table(os.path.join(pvalue_basedir,'missense_hg38.pval.csv'))
        self.pvalue_table['FV'] = self.get_pval_table(os.path.join(pvalue_basedir,'frameshift_hg38.pval.csv'))
        self.pvalue_table['IV'] = self.get_pval_table(os.path.join(pvalue_basedir,'inframe_hg38.pval.csv'))
        self.pvalue_table['SPL'] = self.get_pval_table(os.path.join(pvalue_basedir,'splicesite_hg38.pval.csv'))
        self.pvalue_table['STG'] = self.get_pval_table(os.path.join(pvalue_basedir,'stopgain_hg38.pval.csv'))
        self.pvalue_table['STL'] = self.get_pval_table(os.path.join(pvalue_basedir,'stoploss_hg38.pval.csv'))
        self.transc_aa_so_re = re.compile('(.*):([A-Z,\*,_]*)(\d*)([A-Z,\*,_]*)\((.*)\)')
        self.transc_aa_re = re.compile('(.*):([A-Z,\*,_]*)(\d*)([A-Z,\*,_]*)')
        self.cannonical_chrom_re = re.compile('(?i)chr(\d{1,2}|x|y|un)')
    
    def annotate(self, input_data):
        out = {'transcript':'',
               'score':'',
               'pval':'',
               'score_mis':'',
               'score_fsv':'',
               'score_inv':'',
               'score_stg':'',
               'score_stl':'',
               'score_spl':'',
               'all_results':'',
               'hugo':''}
        chrom = input_data['chrom']
        if len(chrom) > 5:
            chrom_main = self.cannonical_chrom_re.match(chrom).group(0)
        else:
            chrom_main = chrom
        p = input_data['mapping_parser']
        
        primary_transcript = input_data['transcript']
        if primary_transcript is None:
            return
        primary_mapping = p.get_transcript_mapping(input_data['transcript'])
        primary_so = primary_mapping.so
        pos = input_data['pos']
        alt = input_data['alt_base']
        
        transc_ontologies = {}
        for mapping in p.mappings:
            so = mapping.so
            if so in ['MIS','STG','STL']:
                transc_ontologies[mapping.transcript] = so
        if transc_ontologies == {}:
            return
                    
        q = 'select v.score, t.name from '+chrom_main+' as v join transcript '\
             +'as t on v.tid=t.tid join chrom as c on v.cid=c.cid where '\
             +'c.name="'+chrom+'" and v.pos='+str(pos)+' and v.alt="'+alt+'";'
        self.cursor.execute(q)
        qr = self.cursor.fetchall()
        if qr:
            precomp_data = []
            for r in qr:
                score = r[0]
                transc = r[1]
                if transc not in transc_ontologies:
                    continue
                transc_so = transc_ontologies[transc]
                if transc_so in self.pvalue_table:
                    pval = self.pvalue_table[transc_so][score]
                else:
                    pval = 0.0
                transc_vest_result = '%s(%s:%s)' %(transc, score, pval)
                precomp_data.append({'score':score,
                                     'transcript':transc,
                                     'pval':pval,
                                     'full_result':transc_vest_result})
            scores = [x['score'] for x in precomp_data]
            all_results_list = [x['full_result'] for x in precomp_data]
            max_score = max(scores)
            max_index = scores.index(max_score)
            worst_mapping = precomp_data[max_index]
            worst_transcript = worst_mapping['transcript']
            worst_pval = worst_mapping['pval']
            all_results_list[max_index] = '*'+all_results_list[max_index]
            
            out['transcript'] = worst_transcript
            out['score'] = max_score
            out['pval'] = worst_pval
            out['all_results'] = ','.join(all_results_list)
            out['hugo'] = input_data['hugo']
            
        return out
    
    def get_pval_table(self, pfile):
        pval_tab=dict()
        
        pval_file = open(pfile, 'r')
        pval_file.readline()
        for line in pval_file:
            items=line.strip().split(',')
            score = float(items[0].strip('\"'))
            pval = float(items[1])
            pval_tab[score] = pval
    
        return pval_tab

    def build_gene_collection (self, hugo, input_data, gene_data):
        score = input_data['score']
        pval = input_data['pval']
        if score != None:
            gene_data[hugo]['score'].append(score)
            gene_data[hugo]['pval'].append(pval)
    
    def summarize_by_gene (self, hugo, gene_collection):
        out = None
        input_data = gene_collection[hugo]
        scores = input_data['score']
        pvals_non_unique = input_data['pval']
        pvals = list(set(pvals_non_unique))
        if len(scores) > 0:
            out = {}
            raw_gene_pval = stouffer.stouffer(pvals)[1]
            out['max_score'] = max(scores)
            out['mean_score'] = round(sum(scores)/len(scores),3)
            out['gene_pval'] = round(raw_gene_pval, 3)
        return out

if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
