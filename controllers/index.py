class Index(Controller):
	def __init__(self):
		Controller.__init__(self)

	def index(self):
		self.template = "index.html"

	def hello_world(self):
		self.viewArg("var", "this is a test variable")

		self.template = "helloworld.html"


INDEX_CONTROLLER = Index()
