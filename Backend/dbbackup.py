import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor

conn.execute("SELECT * FROM Stores")

with conn:
    with open('db_dump.sql','w') as f :
        for line in conn.iterdump():
            f.write('%s\n' %line)