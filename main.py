from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import parse_qs
import http.cookies as cookies
import os, sys
sys.dont_write_bytecode = True


# 	------------ AVAILABLE DATATYPES --------------
#	Core 			--- Center of the application
#	DB				--- Provides access to SqLite3 database
#	Table 			--- Abstract layer on top of database table
#	Controller 		--- Controls endpoint(s)
#	Auth			--- User authorization and identification

#	config			--- Server-wide configuration details


from core.core 			import Core
from core.table 		import Table
from core.controller 	import Controller
from core.auth 			import Auth

from config 			import config


class Handler(BaseHTTPRequestHandler):
	def end_headers(self):
		BaseHTTPRequestHandler.end_headers(self)

	def handle404(self):
		Core.HEADERSET("Content-Type", "text/plain")
		self.send_response(404, "This path doesn't exist.")

	def getJSON(self):
		# --- Error handling ---
		if "Content-Length" not in self.headers:
			print("Content-Length not present in headers")
			return (400, {})
		if self.headers["Content-Length"] == "0":
			print("Content-Length is equal to 0")
			return (400, {})

		# Parse body
		raw_body = self.rfile.read(int(self.headers["Content-Length"]))

		try:
			body = json.loads(raw_body.decode("utf-8"))
		except json.decoder.JSONDecodeError:
			print("JSON not valid.")
			print(raw_body)
			body = {}
			return (400, {})

		print("Body: " + str(body))
		return (200, body)

	def getHTMLEncoded(self):
		if "Content-Length" not in self.headers:
			print("Content-Length not present in headers")
			return (400, {})
		if self.headers["Content-Length"] == "0":
			print("Content-Length is equal to 0")
			return (400, {})

		raw_body = self.rfile.read(int(self.headers["Content-Length"]))

		return (200, parse_qs(raw_body.decode("utf-8")))


	def loadCookie(self):
		if "Cookie" in self.headers:
			self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
		else:
			self.cookie = cookies.SimpleCookie()


	def sendError(self, status_code, error):
		self.send_response(status_code, error)

	def send_response(self, status_code=None, content=None):
		debugContent = ""
		debugContent += "--- SENDING NEW RESPONSE ---" + "\n"
		if status_code:
			Core.RCODESET(status_code)
		BaseHTTPRequestHandler.send_response(self, Core.RCODE())
		debugContent += "\tStatus Code: " + str(Core.RCODE()) + "\n"

		Core.HEADERSET("Access-Control-Allow-Origin", "*")
		Core.HEADERSET("Access-Control-Allow-Headers", "*")
		Core.HEADERSET("Access-Control-Allow-Methods", "GET, POST, PUT")
		Core.HEADERSET("Access-Control-Allow-Credentials", "true")

		for cookie, val in Core.COOKIES():
			self.cookie[cookie] = val # abuse this to get morsel string
			self.send_header("Set-Cookie", self.cookie[cookie].OutputString())
			debugContent += "\tCookie: " + "\n"
			debugContent += "\t\t" + cookie + "\n"
			debugContent += "\t\t" + val + "\n"

		for header, val in Core.HEADERS():
			self.send_header(header, val)
			debugContent += "\tHeader: " + "\n"
			debugContent += "\t\t" + header + "\n"
			debugContent += "\t\t" + val + "\n"

		self.end_headers()

		if content:
			self.wfile.write(content.encode("utf-8"))
			self.wfile.flush()
			debugContent += "Content: " + str("\n".join(content.split("\n")[:3])) + "\n"

		if config.debug:
			print(debugContent)


	def do_OPTIONS(self):
		self.send_response()

	def do_GET(self):
		self.loadCookie()	# Always load the cookie regardless of whether it's used or not

		if self.path == "/":
			self.path = "/index"
		if self.path[:6] == "/login":
			self.path = "/login"


		params = self.path.strip("/").split("/")
		Core.__init__() # reset core


		# --- SERVE CSS/JS ---
		if params[0] == "public":
			# Fetching css/js
			if params[1] == "css":
				mimetype = "text/css"
			elif params[1] == "js":
				mimetype = "text/javascript"
			else:
				self.send_response(404)
				return

			Core.HEADERSET("Content-type", mimetype)
			try:
				self.send_response(200, open(self.path.lstrip("/")).read())
			except:
				self.send_response(404)

			return


		# --- AUTHENTICATION LOGIC ---
		if self.path != "/login":
			if 'session' not in self.cookie:
				# Redirect to login
				Core.redirect("/login")
				self.send_response()
				return
			else:
				if not Auth.validateSession(self.cookie['session'].value):
					# Invalid or nonexistent session, redirect to login
					Core.redirect("/login")
					self.send_response()
					return


		# --- AUTHENTICATION SUCCESS ---
		Core.PATHSET(self.path)


		i = len(params) - 1
		while i >= 0:
			classFileName = "controllers\\" + "\\".join(params[:i+1]) + ".py"
			if os.path.isfile(classFileName):
				className = classFileName[12:].rstrip(".py").replace("\\", "_")
				exec(open("controllers/"+className+".py").read())
				className = className[0].upper() + className[1:] + "Controller"

				Core.PARAMSSET(params[i:])

				controller = locals()[className]()
				status_code, html = controller.run()

				if status_code >= 200 and status_code <= 299:
					Core.HEADERSET("Content-type", "text/html")
					self.send_response(200, html)
				else:
					self.sendError(status_code, html)

				return

			i -= 1


		self.handle404()


	def do_POST(self):
		self.loadCookie()

		Core.HEADERSET("Content-type", "application/json")

		# this is hacky, find a solution
		Core.redirect(self.path) # redirect to same page after form submit

		if self.path == "/login":
			status_code, body = self.getHTMLEncoded()
			if status_code < 200 or status_code > 299:
				self.send_response()
				return

			if 'username' not in body or 'password' not in body:
				self.send_response()
				return

			if Auth.authenticateUser(body['username'][0], body['password'][0]):
				self.send_response()
				return
			else:
				self.send_response()
				return


		self.handle404()


def main():
	listen = ("127.0.0.1", 8080)
	server = HTTPServer(listen, Handler)

	print("Listening...")
	server.serve_forever()

if __name__ == "__main__":
	main()
