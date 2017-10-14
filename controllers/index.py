class Index(Controller):
	def __init__(self):
		Controller.__init__(self)

	def index(self):
		self.template = "login.html"

	def hello_world(self):
		self.template = "index.html"


INDEX_CONTROLLER = Index()
