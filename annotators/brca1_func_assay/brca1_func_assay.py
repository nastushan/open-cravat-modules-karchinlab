import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        dir_path = os.path.dirname(os.path.realpath(__file__))
        datafile_path = os.path.join(dir_path, "data", "parseddatafile.tsv")
        with open(datafile_path) as f:
            self.d = {}
            for l in f:
                toks = l.strip("\r\n").split("\t")
                self.d["-".join(toks[0:4])] = toks[4:]
        pass
    
    def annotate(self, input_data, secondary_data=None):
        chromkey = input_data["chrom"].replace("chr","")
        poskey = str(input_data["pos"])
        ref_base = input_data["ref_base"]
        alt_base = input_data["alt_base"]
        l1 = [chromkey, poskey, ref_base, alt_base]
        finalkey = "-".join(l1)
        out = {}
        if finalkey in self.d:
            out['score'] = float(self.d.get(finalkey)[0])
            out['class'] = self.d.get(finalkey)[1]
        return out
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()