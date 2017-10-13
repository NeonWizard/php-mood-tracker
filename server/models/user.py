from core.table import Table

class User:
	def __init__(self):
		self.userTable = Table('User')

	def getById(self, id):
		rows = self.select([
			"id LIKE {}".format(id)
		])

		if rows:
			return rows[0]
		else:
			None

	def select(self, search=[], options=[], keys=['*'], joins=[]):
		return self.userTable.select(search, options, keys, joins)
