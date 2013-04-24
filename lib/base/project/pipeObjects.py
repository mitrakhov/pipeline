import os
from dBase import *
from filesystem import *

class Pipe(object):

    def __init__(self):

        self.repo = os.environ['REPO']
        self.db = DBase()
        self.fs = PipeFolders()
        self.dict = self.db.getProjects()

    def rename(self, repoNew):

        if type(repoNew) is str:
            self.repo = repoNew
            print "Repo is changed to %s" % self.repo
        else:
            print "Not a proper value for repo"

    def add(self, projName):
        
        newProjDb = self.db.addProject(projName)
        self.dict[projName] = newProjDb['id']
        
        self.fs.addProject(projName)

        newProj = Project(projName)

        return newProj




class Project(Pipe):

    def __init__(self, projName):
        super(Project, self).__init__()
        self.projName = projName
        self.projId = self.dict[projName]
        self.dict = self.db.getSequences(self.projId)
        self.path = os.path.join(self.repo, self.projName)

class Sequence(Project):

    def __init__(self, projName, seqName):
        super(Sequence, self).__init__(projName)
        self.seqName = seqName
        self.seqId = self.dict[seqName]
        self.dict = self.db.getShots(self.seqId)
        self.path = os.path.join(self.path, 'film', 'sequences', self.seqName)

class Shot(Sequence):

    def __init__(self, projName, seqName, shName):
        super(Shot, self).__init__(projName, seqName)
        self.shName = shName
        self.shId = self.dict[self.shName]
        self.path = os.path.join(self.path, 'shots', self.shName)

if __name__ == '__main__':
    test = Pipe()
    new = test.add('NewTestVlad')
    print new
