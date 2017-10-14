class Index(Controller):
	def __init__(self):
		self.userModel = Core.MODEL('USER')()

		Controller.__init__(self)

	def index(self):
		self.template = "index.html"

	def hello_world(self):
		self.viewArg("var", "this is a test variable")
		self.viewArg("users", self.userModel.select())

		self.template = "helloworld.html"


INDEX_CONTROLLER = Index()
