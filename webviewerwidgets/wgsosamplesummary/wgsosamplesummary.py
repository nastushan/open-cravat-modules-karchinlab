import sqlite3
import os

def get_data (queries):
    so_dic = {
        '':'Intergenic',
        'MIS':'Missense',
        'SYN':'Synonymous',
        'FI1':'Frameshift insertion',
        'FI2':'Frameshift insertion',
        'FD1':'Frameshift deletion',
        'FD2':'Frameshift deletion',
        'IIV':'Inframe insertion',
        'IDV':'Inframe deletion',
        'CSS':'Complex substitution',
        'STG':'Stopgain',
        'STL':'Stoploss',
        'SPL':'Splice site',
        '2KU':'2k upstream',
        '2KD':'2k downstream',
        'UT3':'3\' UTR',
        'UT5':'5\' UTR',
        'INT':'Intron',
        'UNK':'Unknown'
    }
    
    dbpath = queries['dbpath'][0]
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()

    q = 'select distinct base__sample_id from sample'
    cursor.execute(q)
    samples = [v[0] for v in cursor.fetchall()]
    samples.sort()
    
    q = 'select distinct variant.base__so from variant, variant_filtered where variant.base__uid=variant_filtered.base__uid'
    cursor.execute(q)
    sos = [so_dic[v[0]] for v in cursor.fetchall()]
    sos.sort()
    
    sosample = {}
    for so in sos:
        sosample[so] = []
        for sample in samples:
            sosample[so].append(0)
    
    for i in range(len(samples)):
        sample = samples[i]
        q = 'select variant.base__so, count(*) from variant, variant_filtered, sample where variant.base__uid=variant_filtered.base__uid and sample.base__uid=variant.base__uid and sample.base__sample_id="' + sample + '" group by variant.base__so order by variant.base__so'
        cursor.execute(q)
        for row in cursor.fetchall():
            (so, count) = row
            so = so_dic[so]
            sosample[so][i] += 1

    data = {}
    for so in sos:
        row = []
        for i in range(len(samples)):
            row.append(sosample[so][i])
        data[so] = row
    
    response = {'data': {'samples': samples, 'sos': sos, 'socountdata': data}}

    return response