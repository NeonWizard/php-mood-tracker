from core.db import DB

class Table:
	def __init__(self, tableName):
		self.tableName = tableName

	def select(self, search=[], options=[], keys=['*'], joins=[]):
		sql = "SELECT {} FROM {} ".format(",".join(keys), self.tableName)
		sql += DB.buildQuery(search, options)

		return DB.query(sql)

	# Update a row in the table
	#
	# @param array 'data'		Values to be updated
	# @param array 'where'		WHERE clauses
	# @param array 'joins'		Optional array of JOIN clauses
	#
	# @return None
	def update(self, data, where, joins=[]):
		sql = "UPDATE {} {} SET {}".format(self.tableName, " ".join(joins), ", ".join(data))
		sql += DB.buildQuery(where)

		DB.query(sql)

	# Insert a new row into the table
	#
	# @param dict 'data'		Dict to insert
	# @param string 'option'	'ignore' 	= 'INSERT IGNORE'
	#							'replace' 	= 'REPLACE INTO'
	# @return None
	def insert(self, data, option=''):
		method = "INSERT"
		if option:
			method = "INSERT IGNORE" if option=="ignore" else "REPLACE"

		keys, vals = [], []
		for key, val in data.items():
			keys.append(key)
			vals.append(val)

		sql = "{} INTO {} ({}) VALUES ({})".format(
			method,
			self.tableName,
			", ".join(keys),
			", ".join(["?" for _ in range(len(vals))]) # one question mark for every value inserted
		)

		DB.query(sql, vals)

	# Delete a row from table by ID
	#
	# @param int 'id'	Id of row
	#
	# @return None
	def delete(self, id):
		sql = "DELETE FROM {} WHERE id=?".format(self.tableName)

		DB.query(sql, [id])
