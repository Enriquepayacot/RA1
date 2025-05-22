import sqlite3

conn = sqlite3.connect('artroplastias.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS registros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT,
        lado TEXT,
        articulacion TEXT,
        tipo TEXT,
        diagnostico TEXT,
        implante TEXT,
        cirujano TEXT,
        centro TEXT,
        observaciones TEXT
    )
''')

conn.commit()
conn.close()
