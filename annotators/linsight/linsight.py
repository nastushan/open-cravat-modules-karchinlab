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

if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
