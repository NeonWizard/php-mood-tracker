import os

from core.table import Table

class Core:
	def __init__(self):
		# --- Import models ---
		self._MODELS = {}
		for root, dirs, fileNames in os.walk("models"):
			for fileName in fileNames:
				exec(open(root+"\\"+fileName).read())
				modelName = fileName.rstrip(".py")
				self._MODELS[modelName.upper()] = locals()[modelName[0].upper() + modelName[1:] + "Model"]


	def MODELS(self):
		return self._MODELS

	def MODEL(self, name):
		return self._MODELS[name]


Core = Core() # I'll keep abusing python until it gives me singletons :^)
