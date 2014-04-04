import os

class data(object):
    def __init__(self, containerPath, taskName, parent = None):
        self.containerPath = str(containerPath)
        self.containerName = str(self.containerPath.rsplit('/')[-1])
        self.taskName = str(taskName)

    def getDataPath(self, type):
        if type == 'cache':
            dataPath = 'data/cache'
        else:
            dataPath = 'data/anim'

        return str(os.path.join(self.containerPath, dataPath))

    #add data to current scene
    def addData(self, nodeName, dataType):
        taskDataPath = os.path.join(self.getDataPath(dataType), self.taskName)
        nodePath = os.path.join(taskDataPath, nodeName)

        startVersion = 0
        versionPath = ''
        #mkdir cache for current scene
        if not os.path.exists(taskDataPath): os.mkdir(taskDataPath)
        #mkdir cache for current node
        if not os.path.exists(nodePath): os.mkdir(nodePath)
        
        if not os.listdir(nodePath):
            versionPath = os.path.join(nodePath, str(startVersion).zfill(4))
            os.mkdir(versionPath)
        else:
            currentVersion = int(max(os.listdir(nodePath)))
            if os.path.exists(os.path.join(nodePath, str(startVersion).zfill(4))):
                versionPath = os.path.join(nodePath, str(currentVersion + 1).zfill(4))
                os.mkdir(versionPath)
        return versionPath

    def getContainerData(self, dataType):
        containerDataDict = {}
        taskDict = {}
        nodeDict = {}
        versionDict = {}
        cache = ''

        containerDataPath = os.path.join(self.containerPath, 'data', dataType)
        for task in os.listdir(containerDataPath):
            for node in os.listdir(os.path.join(containerDataPath, task)):
                for version in os.listdir(os.path.join(containerDataPath, task, node)):
                    for cache in os.listdir(os.path.join(containerDataPath, task, node, version)):
                        
                        if dataType == 'cache':
                            ext = cache.rsplit('.')[-1]
                            if ext == 'bgeo':
                                cache = cache.replace('.' + ext, '').rsplit('.')[0] + '.$F4.bgeo'

                    versionDict[version] = cache
                    nodeDict[node] = versionDict
                    taskDict[task] = nodeDict

        return taskDict

    def getLastVersion(self, nodeName, dataType):
        versionsDict = self.getContainerData(dataType)[self.taskName][nodeName]
        lastVersionNumber = versionsDict.keys()[-1]
        return os.path.join(self.getDataPath(dataType), self.taskName, nodeName, lastVersionNumber, versionsDict[lastVersionNumber])


class project(object):
    def __init__(self, repoPath, projectName, parent = None):
        self.repoPath = str(repoPath)
        self.projectName = str(projectName)
        self.projectPath = os.path.join(self.repoPath, self.projectName)
        self.seqsPath = os.path.join(self.repoPath, self.projectName, 'film/sequences')
        self.assetsPath = os.path.join(self.repoPath, self.projectName, 'film/assets')

        self.projectList = ['edit', 'film', 'out', 'ref', 'src', 'temp']
        self.outList = ['dailies', 'hires']
        self.filmList = ['assets', 'sequences']
        self.assetList = ['cache', 'fx', 'HDA', 'light', 'materials', 'mattepaint', 'rig', 'shader', 'surface']

        self.containerList = ['anim', 'comp', 'data', 'fx', 'light', 'out', 'proxy', 'src']
        self.dataList = ['anim', 'cache', 'render', 'tracks']

    def create(self):
        if not os.path.exists(self.projectPath):
            os.mkdir(self.projectPath)
            for prj in self.projectList:
                prjFolder = os.path.join(self.projectPath, prj)
                os.mkdir(prjFolder)

                if prj == 'out':
                    for out in self.outList:
                        outFolder = os.path.join(self.projectPath, prj, out)
                        os.mkdir(outFolder)

                if prj == 'film':
                    for film in self.filmList:
                        filmFolder = os.path.join(self.projectPath, prj, film)
                        os.mkdir(filmFolder)

                        if film == 'assets':
                            for asset in self.assetList:
                                assetFolder = os.path.join(self.projectPath, prj, film, asset)
                                os.mkdir(assetFolder)
        else:
            print ''.join(['Project', ' [', self.projectName, '] ', 'already have'])

    def addContainer(self, path, name, short = None):
        if not os.path.exists(os.path.join(path, name)):
            self.containerPath = os.path.join(path, name)
            os.mkdir(self.containerPath)
            if short:
                self.containerList = self.containerList[0:-2]
            for cont in self.containerList:
                        contFolder = os.path.join(self.containerPath, cont)
                        os.mkdir(contFolder)

                        if cont == 'data':
                            for data in self.dataList:
                                dataFolder = os.path.join(self.containerPath, cont, data)
                                os.mkdir(dataFolder)
            return self.containerPath
        else:
            print ''.join(['Container', ' [', name, '] ', 'already have'])

    def addSeq(self, seqName):
        if not os.path.exists(os.path.join(self.seqsPath, seqName)):
            seqPath = self.addContainer(self.seqsPath, seqName, True)                
            os.mkdir(os.path.join(seqPath, 'shots'))
            return seqPath
        else:
            print ''.join(['Sequence', ' [', seqName, '] ', 'already have'])

    def addShot(self, seqPath, shotName):
        if not os.path.exists(os.path.join(seqPath, 'shots', shotName)):
            shotPath = self.addContainer(os.path.join(seqPath, 'shots'), shotName)
            return shotPath
        else:
            print ''.join(['Shot', ' [', shotName, '] ', 'already have'])
