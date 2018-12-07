from cravat import BaseConverter
from cravat import BadFormatError

class CravatConverter(BaseConverter):
    comp_base = {'A':'T','T':'A','C':'G','G':'C','-':'-','N':'N'}
    
    def __init__(self):
        self.format_name = 'ancestrydna'
    
    def check_format(self, f):
        return 'AncestryDNA' in f.readline()
    
    def setup(self, f):
        pass
    
    def convert_line(self, l):
        ret = []
        if l.startswith('#'): return []
        if l.startswith('rsid'): return []
        toks = l.strip('\r\n').split('\t')
        tags = toks[0]
        if int(toks[1]) >= 25: return []
        chrom = toks[1]
        pos = toks[2]
        ref = 'N'
        sample = None
        for var in toks[3:]:
            if var != '0':
                alt = var
                wdict = {'tags':tags,
                    'chrom':chrom,
                    'pos':pos,
                    'ref_base':ref,
                    'alt_base':alt,
                    'sample_id':sample}
                ret.append(wdict)
        return ret
