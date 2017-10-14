class Login(Controller):
	def __init__(self):
		Controller.__init__(self)

	def index(self):
		self.template = "login.html"


LOGIN_CONTROLLER = Login()
