import sqlite3
from sqlite3 import Error
import os

#TODO
# Usage guide/desc
# db_auto is a semi-automated database creation tool developed for use in creating sqlite databases for annotators. Users can specify what columns they wish to see added to the database along with corresponding 
# data file(s) to be inserted into the database. 
class CravatDatabase:
    # chrls = ["chr1", "chr2", "chr3", "chr4", "chr5", "chr6", "chr7", "chr8", "chr9", "chr10", "chr11", "chr12", "chr13", "chr14", "chr15", "chr16", "chr17", "chr18", "chr19", "chr20", "chr21", "chr22", "chrM", "chrX", "chrY"]
    #Creates new database object with file path for database, dictionary of columns to be created in the format of {col name : data type}, list of table names, and a grouped primary key (can be an empty string)
    def __init__(self, db_loc, col_dict, tnames, primary_key):
        print("Creating database")
        try:
            self.db_loc = db_loc
            self.col_dict = col_dict
            self.conn = sqlite3.connect(self.db_loc)
            self.curs = self.conn.cursor()
            self.tnames = tnames
            assert isinstance(self.conn, sqlite3.Connection)
            assert isinstance(self.curs, sqlite3.Cursor)
            self.db_len = len(col_dict)
            #creating sqlite statement strings
            exels = []
            wildls = []
            refls = []
            for col_name, col_type in col_dict.items():
                exels.append("{name} {type}".format(name=col_name, type=col_type))
                wildls.append("?")
                refls.append("{name}".format(name=col_name))
            #column name and data type for statment
            exe_str = ', '.join(exels)
            #wildcard statement for data insertion (?s for each column)
            self.wilds = ', '.join(wildls)
            #column names for data insertion statement
            self.ref_str = ', '.join(refls)
            if primary_key != '':
                primary_key = ', primary key({keys})'.format(keys=primary_key)
            #executing sqlite statements
            for name in self.tnames:
                self.curs.execute('CREATE TABLE IF NOT EXISTS {name} ({exe_str} {primary_key});'.format(name=name, exe_str=exe_str, primary_key=primary_key))
            print("Database created")
        except Error as e:
            print(e)
            self.conn.close()

    #Accepts list of filenames for data files, list of col indexes (columns wanted from datafiles), and number of lines to skip at beginning when reading data files
    def parser(self, filenames, col_idx, skip_num):
        try:
            #Skip 'skip_num' number of lines of file
            skip_num = skip_num - 1
            print("Data insertion start")
            self.curs.execute("PRAGMA synchronous = 0;")
            self.curs.execute("PRAGMA journal_mode = MEMORY;")
            #begin insertions
            fnum = 0 #Filenumber corresponds to entry in tnames (list of files must be ordered to match list of table names)
            for filename in filenames:
                print("Starting {name} insertion".format(name=filename))
                with open("{filename}".format(filename=filename)) as f:
                    for i,l in enumerate(f):
                        if i > skip_num:
                            #Strip whitespace and split on tabs (assumes file is tsv formatted)
                            toks = l.strip("\r\n").split("\t")
                            data = []
                            colnum = 0 #Index of column in dictionary
                            for col in col_idx:
                                #Add null for user specified entries (dbNSFP uses . to denote an empty cell)
                                if self.nullChk(toks[col]):
                                    data.append(None)
                                else:
                                    data.append(self.myCast(toks[col], colnum)) #Figure out user specified casting
                                colnum += 1
                            if not self.rmRow(data):
                                #Ignores insertion of data that violates any constraints (i.e. if unique constraint column is not unique, row will be discarded and insertion will continue)
                                self.curs.execute("INSERT or IGNORE INTO {tname}({ref}) VALUES({wilds});".format(tname=self.tnames[fnum], ref=self.ref_str, wilds=self.wilds), data)
                self.conn.commit()
                print("Finished {name} insertion".format(name=filename))
                fnum += 1
            self.curs.execute("PRAGMA synchronous = 1;")
            self.curs.execute("PRAGMA journal_mode = DELETE;")
            print("Data insertion finished")
        except Error as e:
            print(e)
            self.conn.close()

    #Accepts list of cols to create 1 index on (per table)
    def indexer(self, cols):
        try:
            print("Database indexing start")
            for tname in self.tnames:
                #Index formatted to have table name and specified index name
                self.curs.execute("CREATE INDEX idx_{tname}_{iname} ON {tname}({cols});".format(tname = tname, cols=', '.join(cols), iname=''.join(cols)))
            print("Database indexing finished. Database fully functional!")
        except Error as e:
            print(e)
            self.conn.close()

    #Checks passed cell for a null/none type identifier (ex. '#' or '.' used to denote no data) and returns a boolean as to whether it should be added to the database as a null value
    def nullChk(self, cell):
        if cell == '':
            return True
        else:
            return False

    #Casts passed cell to the corresponding python data type associated with the sqlite data type for that column
    def myCast(self, cell, colnum):
        #Converts sqlite real to python float
        if self.col_dict.get(list(self.col_dict)[colnum]) == 'real':
            return float(cell)
        #Converts sqlite integer to python int
        elif self.col_dict.get(list(self.col_dict)[colnum]) == 'integer':
            return int(cell)
        #No conversion
        else:
            return cell

    #Returns a boolean to determine if the passed row should be added to the database (ex. all columns are null or an empty column requires the whole row to be irrelevant)
    def rmRow(self, row):
        #Counts number of empty cells in row, will remove if count exceeds specified number of empty cells
        if row.count(None) >= 2:
            return True
        else:
            return False

def tsv_converter(infile, outfile, skip_num):
    with open("{filename}".format(filename=infile)) as inf, open("{filename}".format(filename=outfile), "w") as outf:
        for i,l in enumerate(inf):
            if i > skip_num - 1:
                l = l.replace(';','\t')
                l = l.replace('_',' ')
                outf.write(l)

#TODO
#Generic input files
if __name__ == "__main__":
    #Convert original data file to a more standardized tsv format. Edit the tsv_converter method as needed
    tsv_converter("Original Data File", "Formatted Data File", 0)
    #Dictionary of column names and data types, constraints (i.e. single primary key, unique, etc.) can be added after data type
    d = {"column name" : "data type [unique | not null | primary key]"}
    # OPTIONAL string of primary keys (grouped), comma separated. If no keys needed or only a singular key leave an empty string or declare above after data type
    k = 'key1, key2'
    #List of table names
    t = ["name 1", "name 2"]
    #Change to annotator directory
    os.chdir("C:/Your/Annotator/Directory/Here")
    #Creating new annotator directory
    os.makedirs("Annotator Name/data", exist_ok=True)
    #Path to database
    p = os.path.join(os.getcwd(), "Annotator Name", "data", "Annotator Name.sqlite")
    #Creating database
    db = CravatDatabase(p, d, t, k)
    #Path to data file(s)
    #If data files are stored under User folder, use expanduser command. Else, use join
    #wpath = os.path.expanduser('~/Documents/Data/Data File')
    wpath = os.path.join('C:','Data','Data File')
    #List of files
    files = [wpath]
    #Indexes of columns needed from datafile(s), make sure they are ordered in correlation with database col order
    col_idx = [1,2]
    #Number of lines to skip at beginning of file (headers, etc.), leave at 0 if no lines are to be skipped
    skip_num = 0
    #Insert data from datafile(s) into database
    db.parser(files, col_idx, skip_num)
    #List of columns to index on (one index is created using all items in list)
    cols = ['column name']
    #Index database
    db.indexer(cols)
    #Close db connection
    db.conn.close()
