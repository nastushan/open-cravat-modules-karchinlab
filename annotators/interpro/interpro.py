import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        assert isinstance(self.dbconn, sqlite3.Connection)
        assert isinstance(self.cursor, sqlite3.Cursor)
    
    def annotate(self, input_data, secondary_data=None):
        out = {}
        stmt = 'SELECT uniprot_acc, domain FROM {chr} WHERE pos = {pos} AND alt = "{alt}"'.format(chr=input_data["chrom"], pos=int(input_data["pos"]), alt = input_data["alt_base"])
        self.cursor.execute(stmt)
        row = self.cursor.fetchone()
        if row is not None:
            out['uniprot_acc'] = row[0]
            out['domain'] = row[1]
        return out
    
    def cleanup(self):
        self.dbconn.close()
        pass

    def build_gene_collection (self, hugo, input_data, gene_data):
        domain = input_data['domain']
        if domain == None:
            return
        domain_toks = domain.split(';')
        for domain_tok in domain_toks:
            if domain_tok == '.':
                continue
            domain_toks2 = domain_tok.split('|')
            for domain_tok2 in domain_toks2:
                if domain_tok2 not in gene_data[hugo]['domain']:
                    gene_data[hugo]['domain'].append(domain_tok2)

    def summarize_by_gene (self, hugo, gene_collection):
        input_data = gene_collection[hugo]
        domains = '; '.join(input_data['domain'])
        if domains == '':
            out = None
        else:
            out = {'domain': domains}
        return out

if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
