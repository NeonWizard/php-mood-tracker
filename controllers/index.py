class IndexController(Controller):
	def __init__(self):
		self.userModel = Core.MODEL('USER')

		Controller.__init__(self)

	def index(self):
		self.viewArg("var", "this is a test variable")
		self.viewArg("users", self.userModel.select())

		self.template = "index.html"
