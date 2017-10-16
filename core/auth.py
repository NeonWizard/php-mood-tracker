import random
import datetime

from core.core import Core
from core.table import Table

class Auth:
	def isLoggedIn(self):
		return bool(Core.USER())

	# Validate a user login attempt
	#
	# @param username
	# @param password
	#
	# @return None
	def authenticateUser(self, username, password):
		if self.isLoggedIn():
			Core.redirect("/")
			return

		userdata = Core.MODEL('USER').getByUsername(username)
		if userdata and password == userdata['password']:
			self.authSuccess(userdata, True)
			return True
		else:
			return False

	# Authorization success
	def authSuccess(self, userdata, fromLogin=False):
		# Set session stuff
		Core.SESSET('USER', userdata)

		# Store session to DB if coming from login
		if fromLogin:
			token = self.createToken()
			Core.COOKIESET('session', token)
			self.storeSession(userdata['id'], token)
			Core.redirect("/")

	# Create a random token to identify a user after login
	def createToken(self):
		return str(random.randrange(1000000))

	def logout(self):
		pass


	def lookupSession(self, token):
		userSessionTable = Table('UserSession')
		sessiondata = userSessionTable.select([
			'token = "{}"'.format(token)
		])
		if sessiondata:
			return sessiondata[0]
		return None

	def validateSession(self, token):
		sessiondata = self.lookupSession(token)
		if not sessiondata:
			return False

		# Check if session is expired, if so delete from DB and return False
		now = datetime.datetime.now()
		expiry = datetime.datetime.strptime(sessiondata['expiry'], "%Y-%m-%d %H:%M:%S.%f")
		if now > expiry:
			userSessionTable = Table('UserSession')
			userSessionTable.delete(sessiondata['id'])
			return False

		userdata = Core.MODEL('USER').getById(sessiondata['userId'])
		self.authSuccess(userdata)

		return True

	# Set or update a user's session in the DB
	#
	# @param userId		Id of the user
	# @param token 		Token to set for identification/reauthorization
	def storeSession(self, userId, token):
		now = datetime.datetime.now()
		expiry = now + datetime.timedelta(days=1)

		userSessionTable = Table('UserSession')
		userSessionTable.insert({
			'userId': userId,
			'token': token,
			'expiry': str(expiry)
		})


Auth = Auth()
