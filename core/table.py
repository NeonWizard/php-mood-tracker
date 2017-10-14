from core.db import DB

class Table:
	def __init__(self, tableName):
		self.tableName = tableName

	def select(self, search=[], options=[], keys=['*'], joins=[]):
		sql = "SELECT {} FROM {} ".format(",".join(keys), self.tableName)
		sql += DB.buildQuery(search, options)

		return DB.query(sql)
