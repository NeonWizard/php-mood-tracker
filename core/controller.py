from core.core import Core
from core.view import View

class Controller:
	def __init__(self):
		self.header = "html-header.html"
		self.footer = "html-footer.html"

	def run(self):
		self.template = ""
		self.view = View()

		self.errors = []

		action = Core.PARAMS()[1] if len(Core.PARAMS()) > 1 else 'index'

		if not getattr(self, action, None):
			return self._404()

		try:
			getattr(self, action)()
		except Exception as e:
			self.error('An error has occurred, please contact an administrator.')
			self.error(str(e))

		self.assignDefaultArgs()

		return self.render() # returns (status_code, html)

	def assignDefaultArgs(self):
		self.viewArg("PATH", Core.PATH())
		self.viewArg("PARAMS", Core.PARAMS())
		self.viewArg("CONFIG", Core.CONFIG())

	def render(self):
		self.viewArg('errors', self.errors)

		if not self.template:
			self.template = (self.__class__.__name__).lower().replace("controller", "") + ".html"

		html = self.view.render(self.header)
		html += self.view.render(self.template)
		html += self.view.render(self.footer)

		return (200, html)

	def viewArg(self, key, val):
		self.view.assign(key, val)

	def error(self, text):
		self.errors.append(text)


	def _404(self):
		self.template = "404.html"
		return self.render()
