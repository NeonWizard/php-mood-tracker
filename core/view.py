class View():
	def __init__(self):
		self.args = []

	def assign(self, key, val):
		self.args[key] = val

	def render(self, fileName, vars=[]):
		return open("views/"+fileName).read()
