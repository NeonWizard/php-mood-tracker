from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import parse_qs
import http.cookies as cookies
import os

from core.controller import Controller

# from models.user import User as UserModel
# UserModel().insert({
# 	'firstName': 'Simon',
# 	"lastName": "Oliver",
# 	"username": "olimon",
# 	"password": "bestsonev3r"
# })

class Handler(BaseHTTPRequestHandler):
	# Add CORS support
	def end_headers(self):
		self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
		self.send_header("Access-Control-Allow-Headers", "Content-Type, Content-Length")
		self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT")
		self.send_header("Access-Control-Allow-Credentials", "true")
		self.sendCookie()
		BaseHTTPRequestHandler.end_headers(self)

	def handle404(self):
		self.send_response(404)
		self.send_header("Content-Type", "text/plain")
		self.end_headers()

		self.wfile.write("This path doesn't exist.".encode("utf-8"))

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

	def loadCookie(self):
		if "Cookie" in self.headers:
			self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
		else:
			self.cookie = cookies.SimpleCookie()

	def sendCookie(self):
		if not hasattr(self, "cookie"): return

		for morsel in self.cookie.values():
			self.send_header("Set-Cookie", morsel.OutputString())

	def sendError(self, status_code, error):
		self.send_response(status_code)
		self.send_header("Content-Type", "text/plain")
		self.end_headers()
		self.wfile.write(error.encode("utf-8"))

	def do_OPTIONS(self):
		self.send_response(200)
		self.end_headers()

	def do_GET(self):
		# --- LOAD ALL CONTROLLERS ---
		for root, dirs, fileNames in os.walk("controllers"):
			for fileName in fileNames:
				exec(open(root+"\\"+fileName).read())

		self.loadCookie()	# Always load the cookie regardless of whether it's used or not

		if self.path == "/":
			self.path = "/index"

		params = self.path.strip("/").split("/")
		i = len(params) - 1
		while i >= 0:
			classFileName = "controllers\\" + "\\".join(params[:i+1]) + ".py"
			if os.path.isfile(classFileName):
				className = (classFileName.strip("controllers\\").strip(".py").replace("\\", "_") + "_controller").upper()

				controller = locals()[className]
				status_code, html = controller.run(self.path[i:].strip("/").split("/"))

				if status_code >= 200 and status_code <= 299:
					self.send_response(200)
					self.send_header("Content-Type", "text/html")
					self.end_headers()
					self.wfile.write(html.encode("utf-8"))
				else:
					self.sendError(status_code, html)

				return

			i -= 1


		self.handle404()


	def do_POST(self):
		self.loadCookie()

		if self.checkPath("/helloworld"):
			self.send_response(200)
			self.end_headers()
			print("POST request received.")
		else:
			self.handle404()


def main():
	listen = ("127.0.0.1", 8080)
	server = HTTPServer(listen, Handler)

	print("Listening...")
	server.serve_forever()

if __name__ == "__main__":
	main()
