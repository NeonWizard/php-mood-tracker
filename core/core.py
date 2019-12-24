import os

from core.table import Table
from config import config

class Core:
	def __init__(self):
		self._path = ""
		self._params = []
		self._session = {}
		self._headers = {}
		self._cookies = {}
		self._sendCookies = {}

		self._responseCode = 200
		self._persistResponse = False

		# --- Import models ---
		self._MODELS = {}
		for root, dirs, fileNames in os.walk("models"):
			for fileName in fileNames:
				exec(open(root+"/"+fileName).read())
				modelName = fileName.rstrip(".py")
				self._MODELS[modelName.upper()] = locals()[modelName[0].upper() + modelName[1:] + "Model"]()


	def redirect(self, path):
		self.HEADERSET("Location", path)
		self.RCODESET(303, True)


	def MODELS(self, name=None):
		if name:
			return self._MODELS[name]
		return self._MODELS

	def HEADERSET(self, key, val, responseCode=None):
		key = key.upper()
		if responseCode:
			self._responseCode = responseCode
		self._headers[key] = val
	def HEADERS(self, key=None):
		if not key:
			return self._headers.items()
		return self._headers[key]

	def RCODESET(self, responseCode, force=False):
		if not self._persistResponse:
			self._responseCode = responseCode
			self._persistResponse = force
	def RCODE(self):
		return self._responseCode

	def PATHSET(self, path):
		self._path = path
	def PATH(self):
		return self._path

	def PARAMSSET(self, params):
		self._params = params
	def PARAMS(self):
		return self._params

	def CONFIG(self):
		return config

	def COOKIELOAD(self, key, val): 	# load it for reading, but don't send back
		self._cookies[key] = val
	def COOKIESET(self, key, val):		# Set for reading and sending back to client
		self._cookies[key] = val
		self._sendCookies[key] = val
	def COOKIES(self, key=None):		# Look up cookie(s)
		if not key:
			return self._cookies.items()

		# key = key.lower()
		if key in self._cookies:
			return self._cookies[key]
		return None
	def COOKIES_TO_SEND(self):			# List all cookies to send back to client
		return self._sendCookies.items()

	def SESSET(self, key, val):
		self._session[key] = val
	def SES(self, key=None):
		if not key:
			return self._session

		if key not in self._session: return None
		return self._session[key]

	def USERSET(self, key, val):
		self._session['USER'][key] = val
	def USER(self, key=None):
		if 'USER' not in self._session: return None

		if not key:
			return self._session['USER']
		return self._session['USER'][key]


Core = Core() # I'll keep abusing python until it gives me singletons :^)
