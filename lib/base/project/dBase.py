#!/usr/bin/python
from shotgun_api3 import Shotgun

class DBase(object):
    """Wrapper for database, currently it's Shotgun"""



    def __init__(self):

        sgSite = 'https://chimneypot.shotgunstudio.com'
        scriptName = 'dBase'
        scriptKey = '729a76955455909c79f6d90262bb9fbe9186b92b'

        self.db = Shotgun(sgSite, scriptName, scriptKey)
        
        
    def getProjectsDict(self, status='Active', owner='kiev'):
        
        filters = [ ['sg_status', 'is', status],
                ['sg_project_owner', 'is', owner]
                ]
        fields = ['name', 'id']
        projectsListRaw = self.db.find("Project", filters, fields)
        projectDict = {x['name']:x['id'] for x in projectsListRaw}

        return projectDict

    def getSequencesDict(self, projId):

        filters = [['project','is',{'type':'Project','id':projId}]]
        fields = ['code', 'id']
        sequencesListRaw = self.db.find("Sequence", filters, fields)
        sequencesDict = {x['code']:x['id'] for x in sequencesListRaw}

        return sequencesDict
    
    def getShots(self, seqId):

        filters = [['sg_sequence','is',{'type':'Sequence','id':seqId}]]
        fields = ['code', 'id']
        sequencesListRaw = self.db.find("Shot", filters, fields)
        sequencesDict = {x['code']:x['id'] for x in sequencesListRaw}

        return sequencesDict    

    def addProject(self, projName, status='Active', owner='kiev'):

        data = {
            'name': projName,
            'sg_status': status,
            'sg_project_owner': owner
            }

        newProj = self.db.create('Project', data)

        return newProj

    def addSequence(self, seqName, projId):

        data = {
            'project': {'type': 'Project', 'id': projId},
            'code': seqName
            }

        newSeq = self.db.create('Sequence', data)

        return newSeq

    def addShot(self, shName, seqId, projId):

        data = {
            'project': {'type': 'Project', 'id': projId},
            'sg_sequence': {'type': 'Sequence', 'id': seqId},
            'code': shName
            }

        newSh = self.db.create('Shot', data)

        return newSh       



    def getProject(self, projId):
        
        filters = [['id', 'is', projId]]
        fields = ['name']
        proj = self.db.find_one("Project", filters, fields)

        return proj

    def getSequence(self, seqId):
        
        filters = [['id', 'is', seqId]]
        fields = ['code', 'project', 'shots']
        seq = self.db.find_one("Sequence", filters, fields)

        return seq

    def getShot(self, shId):

        filters = [['id', 'is', shId]]
        fields = ['code', 'project', 'sg_sequence', 'tasks']
        sh = self.db.find_one("Shot", filters, fields)

        return sh





if __name__ == '__main__':
    a = DBase()
    print a.getShot(3799)