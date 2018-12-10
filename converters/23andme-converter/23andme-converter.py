from cravat import BaseConverter
from cravat import BadFormatError

class CravatConverter(BaseConverter):
    comp_base = {'A':'T','T':'A','C':'G','G':'C','-':'-','N':'N'}
    
    def __init__(self):
        self.format_name = '23andme'
    
    def check_format(self, f):
        return '23andMe' in f.readline()
    
    def setup(self, f):
        pass
    
    def convert_line(self, l):
        ret = []
        if l.startswith('#'): return []
        toks = l.strip('\r\n').split('\t')
        tags = toks[0]
        chrom = toks[1]
        pos = toks[2]
        ref = ''
        sample = None
        geno = list(toks[3])
        for var in geno:
            if var != '-' and var != 'D' and var != 'I':
                alt = var
                wdict = {'tags':tags,
                    'chrom':chrom,
                    'pos':pos,
                    'ref_base':ref,
                    'alt_base':alt,
                    'sample_id':sample}
                ret.append(wdict)
        return ret
