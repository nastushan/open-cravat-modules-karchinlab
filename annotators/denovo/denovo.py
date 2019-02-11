import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os
from functools import reduce

class CravatAnnotator(BaseAnnotator):
    """
    CravatAnnotator for the Denovo module.

    Querying attributes (input_data):
        chrom, pos, ref_base, alt_base

    Return attributes (out):
        PubmedId, PrimaryPhenotype, Validation

    Attributes:
        sql_template (str): A sql template for querying Denovo db. Use format str
        instance method to insert chrom, pos, ref_base, and alt_base.
    """
    
    sql_template = \
    ("SELECT "
        "PubmedId, PrimaryPhenotype, Validation "
    "FROM Denovo "
        "WHERE Chr='{}' "
        "AND Position='{}' "
        "AND Reference='{}' "
        "AND Alternate='{}' "
    ";")

    @staticmethod
    def concat(accum, x):
        """
        Concat a 2D-list into another 2D-list along the indices. Use with functools.reduce.
        Ex:
            [[1,2,3], [4,5,6], [7,8,9]] -> [[1,4,7], [2,5,8], [3,6,9]]
        Arguments:
            accum (list<list>): 2D array that accumulates consecutive concats.
            x (list): The next list to add to concatanation.
        Return:
            concated (list<list>): Concatanated 2D list.
        """
        for arr, el in zip(accum, x):
            arr.append(el)
        return accum

    def setup(self):
        pass

    def annotate(self, input_data):
        """
        Query the denovo db and return any matched variants in `out` dict.
        """
        out = None
        sql = self.sql_template.format(
            input_data['chrom'].strip('chr'),
            input_data['pos'],
            input_data['ref_base'],
            input_data['alt_base']
        )
        result = self.cursor.execute(sql).fetchall()
        if not result:
            return out
        concated = reduce(self.concat, result, [[] for i in range(len(result[0]))])
        concated = [','.join(arr) for arr in concated]
        out = {
            'PubmedId': concated[0] + '[WEB:]https://www.ncbi.nlm.nih.gov/pubmed/?term=' + concated[0],
            'PrimaryPhenotype': concated[1],
            'Validation': concated[2]
        }
        return out

    def cleanup(self):
        pass
    
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
