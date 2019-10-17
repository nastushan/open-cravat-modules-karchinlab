import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        pass
    
    def annotate(self, input_data, secondary_data=None):
        self.logger.warn(secondary_data)
        out = {}
        out['snps'] = 'a'
        out['r2s'] = 'b'
        out['dprimes'] = 'c'
        return out
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()