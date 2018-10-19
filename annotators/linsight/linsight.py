import sys
from cravat import BaseAnnotator
from cravat import InvalidData

class CravatAnnotator(BaseAnnotator):
    def annotate(self, input_data, secondary_data=None):
        out = {}
        chrom = input_data['chrom']
        pos = input_data['pos']
        binno = str(get_bin(pos, pos))
        pos = str(pos)
        q = 'select val from ' + chrom + ' where binno=' + binno + ' and start<=' + pos + ' and end>=' + pos
        try:
            self.cursor.execute(q)
        except:
            return None
        r = self.cursor.fetchone()
        self.logger.info('r=' + str(r))
        if r == None:
            out = None
        else:
            out['value'] = r[0]
        return out

def bins_for_range (start, end):
    start_bin = start
    end_bin = end - 1
    start_bin = start_bin >> 17
    end_bin = end_bin >> 17
    bin_offsets = [512 + 64 + 8 + 1, 64 + 8 + 1, 8 + 1, 1, 0]
    for bin_offset in bin_offsets:
        yield bin_offset + start_bin, bin_offset + end_bin
        start_bin = start_bin >> 3
        end_bin = end_bin >> 3
    return None

def get_bin (start, end):
    for start_bin, end_bin in bins_for_range(start, end):
        if start_bin == end_bin:
            return start_bin
    return None

def make_db_data ():
    f = open('linsight.bed')
    chroms = {}
    for line in f:
        [chrom, start, end, val] = line[:-1].split('\t')
        if chrom not in chroms:
            chroms[chrom] = open(chrom + '.txt', 'w')
        binno = get_bin(int(start), int(end))
        chroms[chrom].write(str(binno) + '\t' + str(start) + '\t' + str(end) + '\t' + str(val) + '\n')
    for chrom in chroms:
        chroms[chrom].close()

def make_db_load_sql ():
    import glob
    datafilepaths = glob.glob('chr*.txt')
    wf = open('linsight.sql', 'w')
    wf.write('.separator "\t"\n')
    for filepath in datafilepaths:
        chrom = filepath.split('.')[0]
        wf.write('create table ' + chrom + ' (binno int, start int, end int, val float);\n')
        wf.write('create index ' + chrom + '_idx on ' + chrom + ' (binno);\n')
        wf.write('.import ' + filepath + ' ' + chrom + '\n')
    wf.close()

if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
