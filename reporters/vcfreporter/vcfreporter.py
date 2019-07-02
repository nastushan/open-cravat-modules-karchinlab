from cravat.cravat_report import CravatReport
import sys
import datetime
import re
import csv
import zipfile
import os
import aiosqlite3

class Reporter(CravatReport):

    def setup (self):
        self.wf = None
        self.csvwriter = None
        self.filenames = []
        self.filename = None
        self.filename_prefix = None
        if self.savepath == None:
            self.filename_prefix = 'cravat_result'
        else:
            self.filename_prefix = self.savepath
        if not 'type' in self.confs:
            self.info_type = 'separate'
        else:
            info_type = self.confs['type']
            if info_type in ['separate', 'combined']:
                self.info_type = self.confs['type']
            else:
                self.info_type = 'separate'
        self.info_fieldname_prefix = 'CRV'

    def end (self):
        if self.wf is not None:
            self.wf.close()
        zf = zipfile.ZipFile(self.filename_prefix + '.vcf.zip', mode='w', compression=zipfile.ZIP_DEFLATED)
        for filename in self.filenames:
            zf.write(filename, os.path.relpath(filename, start=os.path.dirname(filename)))
        zf.close()
        
    async def connect_db (self, dbpath=None):
        if dbpath != None:
            self.dbpath = dbpath
        if self.dbpath == None:
            sys.stderr.write('Provide a path to aggregator output')
            exit()
        if os.path.exists(self.dbpath) == False:
            sys.stderr.write(self.dbpath + ' does not exist.')
            exit()
        self.conn = await aiosqlite3.connect(self.dbpath)
        self.cursor = await self.conn.cursor()
        await self.cursor.execute('select distinct(base__sample_id) from sample')
        self.samples = []
        rows = await self.cursor.fetchall()
        if rows is None or len(rows) == 0:
            self.samples.append('NOSAMPLEID')
        else:
            for row in rows:
                self.samples.append(row[0])

    def write_preface (self, level): 
        self.level = level
        if self.wf is not None:
            self.wf.close()
        if level != 'variant':
            return
        self.filename = self.filename_prefix + '.' + level + '.vcf'
        self.filenames.append(self.filename)
        self.wf = open(self.filename, 'w', encoding='utf-8', newline='')
        self.csvwriter = csv.writer(self.wf, delimiter='\t', lineterminator='\n')
        lines = ['#fileformat=VCFv4.2',
            '#fileDate=' + datetime.datetime.now().strftime('%Y%m%d'),
        ]
        self.write_preface_lines(lines)

    def write_header (self, level):
        self.level = level
        if self.level != 'variant':
            return
        if self.info_type == 'separate':
            for column in self.colinfo[self.level]['columns']:
                col_name = column['col_name']
                col_type = column['col_type'].capitalize()
                col_desc = column['col_desc']
                if col_name in ['base__uid', 'base__chrom', 'base__pos', 'base__ref_base', 'base__alt_base']:
                    continue
                if col_desc is None:
                    col_desc = ''
                line = '#INFO=<ID={},Number=A,Type={},Description="{}">'.format(col_name, col_type, col_desc)
                self.write_preface_line(line)
            line = 'CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t'
            line += '\t'.join(self.samples)
            self.write_preface_line(line)
        elif self.info_type == 'combined':
            line = '#INFO=<ID={},Number=A,Type=String,Description="OpenCRAVAT annotation. Format: '.format(self.info_fieldname_prefix)
            columns_to_add = []
            for column in self.colinfo[self.level]['columns']:
                col_name = column['col_name']
                col_type = column['col_type'].capitalize()
                col_desc = column['col_desc']
                if col_name in ['base__uid', 'base__chrom', 'base__pos', 'base__ref_base', 'base__alt_base']:
                    continue
                columns_to_add.append(col_name)
            line += '|'.join(columns_to_add)
            self.write_preface_line(line)
            line = 'CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t'
            line += '\t'.join(self.samples)
            self.write_preface_line(line)
            
    def write_table_row (self, row):
        if self.level != 'variant':
            return
        columns = self.colinfo[self.level]['columns']
        row = list(row)
        writerow = []
        info = []
        chrom = None
        pos = None
        uid = None
        ref = None
        alt = None
        qual = '.'
        filt = '.'
        fmt = 'GT'
        for i in range(len(columns)):
            column = columns[i]
            col_name = column['col_name']
            cell = row[i]
            if cell is None or cell == '':
                if self.info_type == 'separate':
                    continue
                elif self.info_type == 'combined':
                    info.append('')
            else:
                if col_name == 'base__uid':
                    uid = cell
                    continue
                if col_name == 'base__chrom':
                    chrom = cell.lstrip('chr')
                elif col_name == 'base__pos':
                    pos = cell
                elif col_name == 'base__ref_base':
                    ref = cell
                elif col_name == 'base__alt_base':
                    alt = cell
                elif col_name == 'base__all_mappings':
                    cell = cell.replace('; ', '&')
                    cell = cell.replace(' ', '-')
                    if self.info_type == 'separated':
                        infocell = col_name + '=' + cell
                        info.append(infocell)
                    elif self.info_type == 'combined':
                        infocell = cell
                        info.append(infocell)
                elif col_name == 'tagsampler__numsample':
                    continue
                elif col_name == 'tagsampler__samples':
                    samples_with_variant = cell.split(',')
                    sample_cols = []
                    for s in self.samples:
                        if s in samples_with_variant:
                            sample_cols.append('1|1')
                        else:
                            sample_cols.append('')
                else:
                    if type(cell) is str and ' ' in cell:
                        cell = cell.replace(' ', '~')
                    if self.info_type == 'separate':
                        infocell = column['col_name'] + '=' + str(cell)
                    elif self.info_type == 'combined':
                        infocell = str(cell)
                    info.append(infocell)
        if self.info_type == 'separate':
            infoline = ';'.join(info)
        elif self.info_type == 'combined':
            infoline = self.info_fieldname_prefix + '=' + '|'.join(info)
        writerow = [chrom, str(pos), str(uid), ref, alt, qual, filt, infoline, fmt]
        writerow.extend(sample_cols)
        self.write_body_line(writerow)

    def write_body_lines (self, lines):
        if self.level != 'variant':
            return
        for line in lines:
            self.write_body_line(line)
    
    def write_body_line (self, row):
        if self.level != 'variant':
            return
        self.wf.write('\t'.join(row) + '\n')
    
    def write_preface_lines (self, lines):
        if self.level != 'variant':
            return
        for line in lines:
            self.write_preface_line(line)
    
    def write_preface_line (self, line):
        if self.level != 'variant':
            return
        self.wf.write('#' + line + '\n')

    def substitute_val (self, level, row):
        if level in self.column_subs:
            for i in self.column_subs[level]:
                if row[i] is not None:
                    sub = self.column_subs[level][i]
                    for target in sub:
                        row[i] = re.sub('\\b' + target + '\\b', sub[target], row[i])
        return row

def main ():
    reporter = Reporter(sys.argv)
    reporter.run()

if __name__ == '__main__':
    main()
