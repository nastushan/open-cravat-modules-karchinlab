import sqlite3

def get_data (queries):
    ret = {}
    try:
        dbpath = queries['dbpath']
        tab = queries['tab']
        rowkey = queries['rowkey']
        note = queries['note'].replace('"', "'")
        conn = sqlite3.connect(dbpath)
        c = conn.cursor()
        if tab == 'variant':
            q = 'update {} set base__note="{}" where base__uid={}'.format(
                tab, note, rowkey)
            c.execute(q)
        elif tab == 'gene':
            q = 'update {} set base__note="{}" where base__hugo="{}"'.format(
                tab, note, rowkey)
            c.execute(q)
        conn.commit()
        ret['status'] = 'success'
    except:
        import traceback
        traceback.print_exc()
        ret['status'] = 'fail'
    return ret
