#!/usr/bin/python
from shotgun_api3 import Shotgun

class DBase(object):
	"""Wrapper for database, currently it's Shotgun"""



	def __init__(self):

		sgSite = 'https://chimneypot.shotgunstudio.com'
		scriptName = 'dBase'
		scriptKey = '729a76955455909c79f6d90262bb9fbe9186b92b'

		self.db = Shotgun(sgSite, scriptName, scriptKey)
		
		
	def getProjects(self, status='Active'):
		
		filters = [['sg_status', 'is', status]]
		fields = ['name', 'id']
		projectsListRaw = self.db.find("Project", filters, fields)
		projectDict = {x['name']:x['id'] for x in projectsListRaw}

		return projectDict

	def getSequences(self, projectId):

		filters = [['project','is',{'type':'Project','id':projectId}]]
		fields = ['code', 'id']
		sequencesListRaw = self.db.find("Sequence", filters, fields)
		sequencesDict = {x['code']:x['id'] for x in sequencesListRaw}

		return sequencesDict
	
	def getShots(self, sequenceId):

		filters = [['sg_sequence','is',{'type':'Sequence','id':sequenceId}]]
		fields = ['code', 'id']
		sequencesListRaw = self.db.find("Shot", filters, fields)
		sequencesDict = {x['code']:x['id'] for x in sequencesListRaw}

		return sequencesDict	

if __name__ == '__main__':
	a = DBase()
	print a.getShots(219)