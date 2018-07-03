import sqlite3
import os

def get_data (queries):
    response = {}
    
    dbpath = queries['dbpath'][0]
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    
    query = 'select name from sqlite_master where type="table" and name="variant_filtered"'
    cursor.execute(query)
    r = cursor.fetchone()
    no_coding = 0
    no_noncoding = 0
    if r is not None:
        query = 'select base__hugo from variant inner join variant_filtered on variant.base__uid=variant_filtered.base__uid'
        cursor.execute(query)
        results = cursor.fetchall()
        for result in results:
            hugo = result[0]
            if hugo == '':
                no_noncoding += 1
            else:
                no_coding += 1
    response['data'] = {'no_coding': no_coding, 'no_noncoding': no_noncoding}
    
    return response