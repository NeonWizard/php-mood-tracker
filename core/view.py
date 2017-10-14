from mako.template import Template

class View():
	def __init__(self):
		self.args = {}

	def assign(self, key, val):
		self.args[key] = val

	def render(self, filename, vars=[]):
		t = Template(filename=("views/"+filename))
		return str(t.render(**self.args))
