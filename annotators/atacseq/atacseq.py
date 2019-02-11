import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        self.query_template = 'select disease, CausalSNP, Element_type from ATACdata_pancancer where Chromosome=? and start<=? and ?<=end;'
    
    def annotate(self, input_data, secondary_data=None):
        out = {}
        chrom = input_data['chrom']
        pos = input_data['pos']
        q = 'select disease, CausalSNP, Element_type from ATACdata_pancancer where Chromosome="{}" and start<={} and {}<=end;'.format(chrom,pos-1,pos-1)
        self.cursor.execute(q)
        diseases = []
        snps = []
        elements = []
        for disease, snp, element in self.cursor:
            disease = disease if disease is not None else ''
            snp = snp if snp is not None else ''
            element = element if element is not None else ''
            diseases.append(disease)
            snps.append(snp)
            elements.append(element)
        if len(diseases) > 0:
            out['disease'] = ';'.join(diseases)
        if len(snps) > 0:
            out['snp'] = ';'.join(snps)
        if len(elements) > 0:
            out['element'] = ';'.join(elements)
        return out
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
