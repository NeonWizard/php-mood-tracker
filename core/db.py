import sqlite3


def dict_factory(cursor, row):
	d = {}
	for i, col in enumerate(cursor.description):
		d[col[0]] = row[i]
	return d

class DB:
	def __init__(self, dbFileName):
		self.conn = sqlite3.connect(dbFileName+".db")
		self.conn.row_factory = dict_factory

		self.curs = self.conn.cursor()

	def buildQuery(self, search=[], options=[]):
		if search:
			sql = "WHERE "
			sql += " AND ".join(search)
		else:
			sql = ""

		if options:
			sql += " ".join(options)

		return sql

	def query(self, sql):
		self.curs.execute(sql)
		return self.curs.fetchall()


DB = DB('mood-tracker')
