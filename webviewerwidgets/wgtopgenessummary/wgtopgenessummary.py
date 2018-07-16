import sqlite3
import os

def get_data (queries):
    # hugo - aalen
    dbpath = os.path.join(os.path.dirname(__file__), 
                          'data',
                          'wgtopgenessummary.sqlite')
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    q = 'select hugo, aalen from genelen'
    cursor.execute(q)
    genelen = {}
    for row in cursor.fetchall():
        genelen[row[0]] = row[1]
    
    dbpath = queries['dbpath'][0]
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    
    gene_var_perc = {}
    q = 'select variant.base__hugo, count(*) from variant, variant_filtered where variant.base__uid=variant_filtered.base__uid group by variant.base__hugo'
    cursor.execute(q)
    for row in cursor.fetchall():
        hugo = row[0]
        if hugo == '':
            continue
        count = row[1]
        aalen = genelen[hugo]
        perc = count / aalen
        gene_var_perc[hugo] = perc
    
    num_gene_to_extract = 15
    sorted_hugos = sorted(gene_var_perc, key=gene_var_perc.get, reverse=True)
    extracted_hugos = sorted_hugos[:num_gene_to_extract]

    q = 'select distinct base__sample_id from sample'
    cursor.execute(q)
    num_total_sample = len(cursor.fetchall())
    genesampleperc = {}
    for hugo in extracted_hugos:
        q = 'select distinct(sample.base__sample_id) from sample, variant where variant.base__uid=sample.base__uid and variant.base__hugo="' + hugo + '"'
        cursor.execute(q)
        num_sample = len(cursor.fetchall())
        perc_sample = num_sample / num_total_sample
        genesampleperc[hugo] = perc_sample
    sorted_hugos = sorted(genesampleperc, key=genesampleperc.get, reverse=True)
    response = {'data': []}
    for hugo in sorted_hugos:
        response['data'].append([hugo, genesampleperc[hugo]])

    return response