import os
from dBase import *
from filesystem import *

class Pipe(object):
    
    """ Upper repository-level class """

    def __init__(self, repo=os.environ['REPO']):

        self.repo = repo
        self.db = DBase()
        self.fs = PipeFolders(self.repo)
        self.dict = self._setDict()
        self.elementsDict = self._setElementsDict()


    def _setDict(self):

        pass

    # Dictionary of projects
        
    def _setElementsDict(self):

        return self.db.getProjectsDict()

    

    # Add new project

    def add(self, projName):
        
        try:
            if projName in self.elementsDict.keys():
                raise ValueError, 'Project with this name already exists'
        
        except ValueError, e:
            print e
            pass
        
        else:
            newProjDb = self.db.addProject(projName)          
            self.fs.addProject(projName)
            self.elementsDict[projName] = newProjDb['id']  
            newProj = Project(newProjDb['id'])
            
            print "Project %s created" % projName    

            return newProj





class Project(Pipe):

    def __init__(self, id, isEmpty=False):
        
        self.id = id
        super(Project, self).__init__()
        self.projName = self._setProjName()
        self.path = os.path.join(self.repo, self.projName)


    # Dictionary of sequences

    def _setElementsDict(self):

        return self.db.getSequencesDict(self.id)

    # Self shotgun fields values

    def _setDict(self):

        return self.db.getProject(self.id)

    def _setProjName(self):

        return self.dict['name']

    



    def add(self, seqName):

        try:
            
            if seqName in self.elementsDict.keys():
                raise ValueError, 'Sequence with the same name already exists'
        
        except ValueError, e:
            print e
            pass
        
        else:
            newSeqDb = self.db.addSequence(seqName, self.id)
            self.fs.addSequence(self.projName, seqName)
            self.elementsDict[seqName] = newSeqDb['id']
            newSeq = Sequence(newSeqDb['id'])
            
            print "Sequence %s created" % seqName
            
            return newSeq




class Sequence(Project):

    def __init__(self, id):
        super(Sequence, self).__init__(id)
        self.seqName = self._setSeqName()
        self.path = os.path.join(self.path, 'film', 'sequences', self.seqName)
    

    # Self shotgun fields values

    def _setDict(self):
        return self.db.getSequence(self.id)

    # Dictionary of shots

    def _setElementsDict(self):

        return {x['name']:x['id'] for x in self.dict['shots']}


    def _setProjName(self):

        return self.dict['project']['name']

    def _setSeqName(self):

        return self.dict['code']

    def add(self, shName):

        try:
            
            if shName in self.elementsDict.keys():
                raise ValueError, 'Shot with the same name already exists'
        
        except ValueError, e:
            print e
            pass
        
        else:
            newShDb = self.db.addShot(shName, self.id, self.dict['project']['id'])
            self.fs.addShot(self.projName, self.seqName, shName)
            self.elementsDict[shName] = newShDb['id']
            newSh = Shot(newShDb['id'])
            
            print "Shot %s created" % shName
            
            return newSh






class Shot(Sequence):

    def __init__(self, id):
        super(Shot, self).__init__(id)
        self.shName = self._setShName()
        self.path = os.path.join(self.path, 'shots', self.shName)

    # Self shotgun fields values

    def _setDict(self):
        return self.db.getShot(self.id)

    # Dictionary of shots

    def _setElementsDict(self):

        return {x['name']:x['id'] for x in self.dict['tasks']}


    def _setProjName(self):

        return self.dict['project']['name']

    def _setSeqName(self):

        return self.dict['sg_sequence']['name']

    def _setShName(self):

        return self.dict['code']


if __name__ == '__main__':
    # test = Project(164)
    test = Sequence(236)
    print test.path
