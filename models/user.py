class UserModel(Table):
	def __init__(self):
		self.tableName = "User"

	def getById(self, id):
		rows = self.select([
			"id LIKE {}".format(id)
		])

		if rows:
			return rows[0]
		else:
			None

	def getByUsername(self, username):
		rows = self.select([
			"username LIKE '{}'".format(username)
		])

		if rows:
			return rows[0]
		else:
			None
