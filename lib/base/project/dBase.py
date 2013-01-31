from shotgun_api3 import Shotgun

class DBase(object):
	"""Wrapper for database, currently it's Shotgun"""
	def __init__(self, sgSite, scriptName, scriptKey):
		self.db = Shotgun(sgSite, scriptName, scriptKey)
		
		
	def createObject(self, objName, objType):
		sg.create(objType, {'name':objName})
		    