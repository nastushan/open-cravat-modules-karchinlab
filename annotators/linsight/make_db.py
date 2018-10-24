import pyliftover
import cravat.constants as constants

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
    f = open('/mnt/d/Git/tmp/linsight_files/linsight.bed')
    chroms = {}
    liftover = pyliftover.LiftOver(constants.liftover_chain_paths['hg19'])
    for line in f:
        [chrom, start, end, val] = line[:-1].split('\t')
        if chrom not in chroms:
            chroms[chrom] = open(chrom + '.txt', 'w')
        start = int(start)
        end = int(end)
        liftover_out = liftover.convert_coordinate(chrom, start)
        if liftover_out is not None and len(liftover_out) > 0:
            start = liftover_out[0][1]
        else:
            continue
        liftover_out = liftover.convert_coordinate(chrom, end)
        if liftover_out is not None and len(liftover_out) > 0:
            end = liftover_out[0][1]
        else:
            continue
        binno = get_bin(start, end)
        chroms[chrom].write(str(binno) + '\t' + str(start) + '\t' + str(end) + '\t' + val + '\n')
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

#make_db_data()
#make_db_load_sql()
