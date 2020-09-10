from cravat.cravat_report import CravatReport
import sys
import datetime
import re
import csv
import zipfile
import os
import pandas as pd


class Reporter(CravatReport):

    def setup(self):

        outpath = f'{self.savepath}.example.txt'
        self.outfile = open(outpath, 'w')

    def write_header(self, level):

        self.level = level
        if level != 'variant':
            return
        # and sub.module=='base'

        col_names_to_include = ['base__chrom', 'base__pos', 'base__ref_base', 'base__alt_base',
                                'cosmic__id', 'base__coding', 'base__hugo', 'base__so', 'base__achange']

        rename_col_names_to_include = {'base__chrom': 'CHROM', 'base__pos': 'POS', 'base__ref_base': 'REF',
                                       'base__alt_base': 'ALT',
                                       'cosmic__id': 'ID', 'base__coding': 'Coding', 'base__hugo': 'Gene',
                                       'base__so': 'Sequence Ontology',
                                       'base__achange': 'Protein Change'}
        col_names = [rename_col_names_to_include.get(n, n) for n in col_names_to_include]

        all_columns = col_names
        all_col_names = [col for col in all_columns]
        line = '#' + '\t'.join(map(str, all_col_names))
        self.outfile.write(line + '\n')

        self.index = []
        for i, column in enumerate(self.colinfo[level]['columns']):
            if column['col_name'] in col_names_to_include:
                self.index.append(i)


    def write_table_row(self, row):

        if self.level != 'variant':
            return

        rows = [row[i] for i in self.index]
        str_row = [str(x) if x is not None else '' for x in rows]
        line = '\t'.join(str_row)
        self.outfile.write(line + '\n')

    def end(self):

        self.outfile.close()
        return os.path.realpath(self.outfile.name)


def main():
    reporter = Reporter(sys.argv)
    reporter.run()


if __name__ == '__main__':
    main()
