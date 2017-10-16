class UserModel(Table):
	def __init__(self):
		self.tableName = "User"

		self.requiredFields = ['firstName', 'lastName', 'username', 'password']
		self.optionalFields = ['email']

	def check(self, data):
		for req in self.requiredFields:
			if req not in data:
				return False
		for opt in self.optionalFields:
			if opt not in data:
				data[opt] = ""

		return data

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


	def add(self, data):
		import bcrypt

		data = self.check(data)
		if not data:
			return False

		data['password'] = bcrypt.hashpw(data['password'].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

		self.insert(data)
