import sqlite3
from sqlite3 import Error
import os

#TODO
#Usage guide/desc
class CravatDatabase:
    chrls = ["chr1", "chr2", "chr3", "chr4", "chr5", "chr6", "chr7", "chr8", "chr9", "chr10", "chr11", "chr12", "chr13", "chr14", "chr15", "chr16", "chr17", "chr18", "chr19", "chr20", "chr21", "chr22", "chrM", "chrX", "chrY"]
    #Creates new database object with file path for database, dictionary of columns to be created in the format of {col name : data type}, and tag specifying either a (g)ene or (v)ariant database
    def __init__(self, db_loc, col_dict, tag):
        print("Creating database")
        try:
            self.db_loc = db_loc
            self.tag = tag
            self.col_dict = col_dict
            self.conn = sqlite3.connect(self.db_loc)
            self.curs = self.conn.cursor()
            assert isinstance(self.conn, sqlite3.Connection)
            assert isinstance(self.curs, sqlite3.Cursor)
            db_len = len(col_dict)
            #creating sqlite statement strings
            if(tag == "v"):
                exe_str = "(pos integer, alt text, "
                self.ref_str = "(pos, alt, "
                self.wilds = "(?, ?, "
            elif (tag == "g"):
                exe_str = "(gname text, "
                self.wilds = "(?, "
                self.ref_str = "(gname, "
            else:
                raise Error("Invalid tag. Please specify either v for variant database or g for gene database")
            j = 1
            for x, y in col_dict.items():
                exe_str += x
                exe_str += " "
                exe_str += y
                self.wilds += "?"
                self.ref_str += x
                if j < db_len:
                    exe_str += ", "
                    self.wilds += ", "
                    self.ref_str += ", "
                j += 1
            exe_str += ");"
            self.wilds += ");"
            self.ref_str += ")"
            #executing sqlite statements
            if(tag == "v"):
                for x in self.chrls:
                    self.curs.execute('CREATE TABLE IF NOT EXISTS {i} {exe_str}'.format(i=x, exe_str=exe_str))
            else:
                self.curs.execute('CREATE TABLE IF NOT EXISTS genes {exe_str}'.format(exe_str=exe_str))
            print("Database created")
        except Error as e:
            print(e)
            self.conn.close()

    #Accepts filename for data file. Assumes a naming convention of {filename}.chr{number} for each chr file if variant db
    def parser(self, filename, col_idx):
        try:
            print("Data insertion start")
            self.curs.execute("PRAGMA synchronous = 0;")
            self.curs.execute("PRAGMA journal_mode = MEMORY;")
            if(self.tag == "v"):
                #variant insertions
                for x in self.chrls:
                    print("Starting {i} insertion".format(i=x))
                    with open("{filename}.{chr}".format(filename=filename, chr=x)) as f:
                        for i,l in enumerate(f):
                            #Skip first line of file (column names)
                            if i > 0:
                                #Strip whitespace and split on tabs
                                toks = l.strip("\r\n").split("\t")
                                #data contains pos and alt to start
                                data = [int(toks[col_idx[0]])]
                                data.append(toks[col_idx[1]])
                                #Columns with annotator specific information
                                p = 2
                                while p < len(col_idx):
                                    #Add null for empty entries (dbNSFP uses . to denote an empty cell)
                                    if(toks[col_idx[p]] == "."):
                                        data.append(None)
                                    else:
                                        data.append(toks[col_idx[p]]) #Figure out casting
                                    p += 1
                                self.curs.execute("INSERT INTO {tname}{ref} VALUES{wilds}".format(tname=x, ref=self.ref_str, wilds=self.wilds), data)
                    self.conn.commit()
                    print("Finished {i} insertion".format(i=x))
            else:
                #gene insertions
                with open("{filename}".format(filename=filename)) as f:
                    for i,l in enumerate(f):
                        if i > 0:
                            toks = l.strip("\r\n").split("\t")
                            data = [toks[0]]
                            p = 1
                            while p < len(col_idx):
                                if(toks[col_idx[p]] == "."):
                                    data.append(None)
                                else:
                                    data.append(float(toks[col_idx[p]])) #Figure out casting
                                p += 1
                            self.curs.execute("INSERT INTO genes{ref} VALUES{wilds}".format(ref=self.ref_str, wilds=self.wilds), data)
                self.conn.commit()
            self.curs.execute("PRAGMA synchronous = 1;")
            self.curs.execute("PRAGMA journal_mode = DELETE;")
            print("Data insertion finished")
        except Error as e:
            print(e)
            self.conn.close()

    #Accepts file path for database, creates simple indexes based on position and alt base
    def indexer(self):
        try:
            print("Database indexing start")
            if self.tag == "v":
                for x in self.chrls:
                    self.curs.execute("CREATE INDEX idx_{num}_posalt ON {num}(pos, alt);".format(num = x))
            else:
                self.curs.execute("CREATE INDEX idx_genes_name ON genes(gname);")
            print("Database indexing finished. Database fully functional!")
        except Error as e:
            print(e)
            self.conn.close()

#TODO
#Command line params
#Typecasting
#Generic input files
#Removal of empty rows?
if __name__ == "__main__":
    #Dictionary of column names and data types
    d = {"rvis_evs":"real", "rvis_perc_evs":"real", "rvis_fdr_exac":"real", "rvis_exac":"real", "rvis_perc_exac":"real"}
    #Change to annotator directory
    os.chdir("C:/Users/trak/open-cravat-modules-karchinlab/annotators")
    #Creating new annotator directory
    os.makedirs("rvis/data", exist_ok=True)
    #Path to database
    p = os.path.join(os.getcwd(), "rvis", "data", "rvis.sqlite")
    #Creating database
    db = CravatDatabase(p, d, "g")
    #Path to data file(s)
    wpath = os.path.join('E:', 'dbNSFPv3.5a', 'dbNSFP3.5_gene.complete')
    #Indexes of columns needed from datafile(s), make sure they are ordered in correlation with database col order
    col_idx = [0, 36, 37, 38, 39, 40]
    #Insert data from datafile(s) into database
    db.parser(wpath, col_idx)
    #Index database
    db.indexer()
    #Close db connection
    db.conn.close()
