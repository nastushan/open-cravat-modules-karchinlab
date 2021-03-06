import aiosqlite
import os

async def get_data (queries):
    response = {}
    dbpath = queries['dbpath']
    if 'numgo' in queries:
        num_go = queries['numgo']
    else:
        num_go = 10

    conn = await aiosqlite.connect(dbpath)
    cursor = await conn.cursor()

    hugos = []

    table = 'gene_filtered'
    query = 'select name from sqlite_master where type="table" and ' +\
        'name="' + table + '"'
    await cursor.execute(query)
    r = await cursor.fetchone()
    if r is not None:
        query = 'select distinct base__hugo from ' + table
        await cursor.execute(query)
        hugos = [v[0] for v in await cursor.fetchall() if len(v[0].strip()) > 0]
    else:
        table = 'gene'
        query = 'select name from sqlite_master where type="table" and ' +\
            'name="' + table + '"'
        await cursor.execute(query)
        r = await cursor.fetchone()
        if r is not None:
            query = 'select distinct base__hugo from ' + table
            await cursor.execute(query)
            hugos = [v[0] for v in await cursor.fetchall() if len(v[0].strip()) > 0]
    await cursor.close()
    await conn.close()
    '''
    query = 'select name from sqlite_master where type="table" and ' +\
        'name="variant"'
    cursor.execute(query)
    r = cursor.fetchone()
    if r is not None:
        query = 'select distinct base__hugo from variant'
        cursor.execute(query)
        hugos = [v[0] for v in cursor.fetchall() if len(v[0].strip()) > 0]
    '''

    if hugos == []:
        return response

    conn = await aiosqlite.connect(os.path.join(os.path.dirname(__file__), 
                                        'data', 
                                        'wggosummary.sqlite'))
    cursor = await conn.cursor()

    go = {}
    for hugo in hugos:
        query = 'select go_id from go_annotation where hugo="' + hugo +\
            '" and go_aspect="F"'
        await cursor.execute(query)
        for row in await cursor.fetchall():
            go_id = row[0]
            if go_id in go:
                go[go_id]['geneCount'] += 1
            else:
                go[go_id] = {'go': go_id, 'geneCount': 1}

    # Creates a list of keys.
    go_ids = [*go]

    sorted_go_ids = sorted(go_ids, key=lambda k: go[k]['geneCount'], reverse=True)

    data = []
    # Adds total genes.
    #ret.append({'go': 'Total genes', 
    #            'geneCount': len(hugos), 
    #            'description': 'Total genes'})
    for go_num in range(min(num_go, len(sorted_go_ids))):
        go_id = sorted_go_ids[go_num]
        query = 'select name from go_name where go_id="' + go_id + '"'
        await cursor.execute(query)
        for row in await cursor.fetchone():
            go_desc = row
        go[go_id]['description'] = go_desc
        data.append(go[go_id])
    
    # Remove protein_binding from the names, it crowds out all the others
    rm_index = -1
    for i,v in enumerate(data):
        if v['description'] == 'protein binding':
            rm_index = i
            break
    if rm_index != -1:
        data = data[:rm_index]+data[rm_index+1:]

    response['data'] = data

    await cursor.close()
    await conn.close()
    return response
