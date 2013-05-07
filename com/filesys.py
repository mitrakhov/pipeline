import os

class data(object):
    def __init__(self, levelName, dataPath, parent = None):
        self.levelName = levelName
        self.dataPath = dataPath


    def setlevelName(self, levelName):
        self.levelName = levelName


    def getlevelName(self):
        return self.levelName


    def setDataPath(self, dataPath):
        self.dataPath = dataPath


    def getDataPath(self):
        return self.dataPath
 

    def getSceneDataPath(self):
        return [ os.path.join(self.dataPath, x) for x in os.listdir(self.dataPath) ]


    def getSceneName(self):
        return [x.rsplit('/')[-1] for x in self.getSceneDataPath()]


    def getNodePath(self, node):
        self.node = node
        nodePath = []
        for n in self.getSceneDataPath():
            nodePath.append(os.path.join(n, self.node))
        return nodePath


    #add data to current scene
    def addData(self, currentSceneName, node):
        self.node = node
        self.currentSceneName = currentSceneName
        sceneDataPath = ''
        
        for n, m in zip(self.getSceneDataPath(), self.getNodePath(self.node)):
            if self.currentSceneName in n:
                sceneDataPath = n
                nodePath = m
     
        startVersion = 0
        versionPath = ''
        #mkdir cache for current scene
        if not os.path.exists(sceneDataPath): os.mkdir(sceneDataPath)
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


    #get data for the current scene, get data from dict data[NODENAME][numberOfVersion][file]
    #format example 
    #print data['fire'][-1][-1]
    def getData(self, currentSceneName):
        self.currentSceneName = currentSceneName     
        sceneDataPath = ''
        nodeDict = {}     

        for n in self.getSceneDataPath():
            if self.currentSceneName in n:
                sceneDataPath = n

        nodes = sorted(os.listdir(sceneDataPath))

        for node in nodes:
            nodePath = os.path.join(sceneDataPath, node)
            versions = os.listdir(nodePath)
            cachesList = []
            for version in sorted(versions):
                #cachesList.append(version)
                filePath = os.path.join(sceneDataPath, node, version)
                
                files = sorted(os.listdir(filePath))
                if files:
                    ext = files[0].rsplit('.')[-1]
                    if ext == 'abc':
                        fullPath = os.path.join(filePath, files[0])

                    elif ext == 'bgeo':
                         file = files[0].replace('.' + ext, '').rsplit('.')[0] + '.$F4.bgeo'
                         fullPath = os.path.join(filePath, file)
                    cachesList.append([version, fullPath])

            nodeDict[node] = cachesList

        return nodeDict


    #get all data from the level, get data from dict data[SCENENAME][NODENAME][numberOfVersion]
    #format example 
    #print data['debris']['fire'][-1][-1]
    def getAllData(self):
        scenesDict = {}

        for n in self.getSceneName():
            scenesDict[n] = self.getData(n)
        return scenesDict