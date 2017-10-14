class Maryn(Controller):
	def __init__(self):
		Controller.__init__(self)

	def index(self):
		self.template = "maryn.html"


MARYN_CONTROLLER = Maryn()
