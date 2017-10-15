import sqlite3

conn = sqlite3.connect("../../mood-tracker.db")
curs = conn.cursor()

curs.executescript(open("create_tables.sql").read())
conn.commit()

curs.executescript(open("seed_db.sql").read())
conn.commit()
