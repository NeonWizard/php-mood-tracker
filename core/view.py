from mako.template import Template
from mako.lookup import TemplateLookup

class View():
	def __init__(self):
		self.args = {}

	def assign(self, key, val):
		self.args[key] = val

	def render(self, filename, vars=[]):
		t = Template(filename=("views/"+filename), lookup=TemplateLookup(directories=[".", ]))
		return str(t.render(**self.args))
