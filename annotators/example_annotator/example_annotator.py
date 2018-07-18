import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        """
        Set up data sources. 
        Cravat will automatically make a connection to 
        data/example_annotator.sqlite using the sqlite3 python module. The 
        sqlite3.Connection object is stored as self.dbconn, and the 
        sqlite3.Cursor object is stored as self.cursor.
        """
        # Verify the connection and cursor exist.
        assert isinstance(self.dbconn, sqlite3.Connection)
        assert isinstance(self.cursor, sqlite3.Cursor)
    
    def annotate(self, input_data, secondary_data=None):
        """
        The annotator parent class will call annotate for each line of the 
        input file. It takes one positional argument, input_data, and one
        keyword argument, secondary_data.
        
        input_data is a dictionary containing the data from the current input 
        line. The keys depend on what what file is used as the input, which can 
        be changed in the module_name.yml file. 
        Variant level includes the following keys: 
            ('uid', 'chrom', 'pos', 'ref_base', 'alt_base')
        Variant level crx files expand the key set to include:
            ('hugo', 'transcript','so','all_mappings')
        Gene level files include
            ('hugo', 'num_variants', 'so', 'all_so')
        
        secondary_data is used to allow an annotator to access the output of
        other annotators. It is described in more detail in the CRAVAT 
        documentation.
        
        annotate should return a dictionary with keys matching the column names
        defined in example_annotator.yml. Extra column names will be ignored, 
        and absent column names will be filled with None. Check your output
        carefully to ensure that your data is ending up where you intend.
        """
        out = {}

        ###### Get start_fraction
        # input_data['chrom'] is formatted as chr1, chr2, chrX etc. The chrom
        # column of the database omits the 'chr'. Need to convert formats.
        chrom = input_data['chrom'].replace('chr','')
        # Construct the query as a string
        length_query = 'select len from chrom_length where chrom="%s"' %chrom
        # Execute the query and store the result, if it exists.
        self.cursor.execute(length_query)
        length_result = self.cursor.fetchone()
        if length_result is not None:
            chrom_length = length_result[0]
            start_fraction = input_data['pos']/chrom_length
        else:
            start_fraction = None
        out['start_fraction'] = start_fraction

        ##### Get verbose_ref
        verbose_ref = ''
        for abbv in input_data['ref_base']:
            verbose_ref_query = 'select full_name from nucleotide_names where abbreviation="%s"' %abbv
            self.cursor.execute(verbose_ref_query)
            verbose_ref_result = self.cursor.fetchone()
            if verbose_ref_result is not None:
                verbose_ref += verbose_ref_result[0]
        out['verbose_ref'] = verbose_ref

        ##### Get ref_len
        cleaned_ref_base = input_data['ref_base'].replace('-','')
        out['ref_len'] = len(cleaned_ref_base)

        return out
    
    def cleanup(self):
        """
        cleanup is called after every input line has been processed. Use it to
        close database connections and file handlers. Automatically opened
        database connections are also automatically closed.
        """
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()