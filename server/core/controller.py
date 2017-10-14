from core.view import View

class Controller:
	def __init__(self):
		self.args = []
		self.template = ""
		self.view = View()

		self.errors = []

		self.header = "html-header.html"
		self.footer = "html-footer.html"

	def run(self, params):
		action = params[1] if len(params) > 1 else 'index'

		if not getattr(self, action, None):
			return self._404()

		try:
			getattr(self, action)()
		except Exception as e:
			self.error('An error has occurred, please contact an administrator.')
			self.error(str(e))

		return self.render() # returns (status_code, html)

	def render(self):
		if self.errors:
			self.viewArg('errors', self.errors)

		if not self.template:
			self.template = (self.__class__.__name__).lower() + ".html"

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
