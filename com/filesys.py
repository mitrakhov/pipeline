import os

class cache(object):
    def __init__(self, scenePath, dataPath, parent=None):
        self.scenePath = scenePath
        self.dataPath = dataPath


    def setScenePath(self, scenePath):
        self.scenePath = scenePath

    def getScenePath(self):
        return self.scenePath

    def setDataPath(self, dataPath):
        self.dataPath = dataPath

    def getDataPath(self):
        return self.dataPath

    def getSceneName(self):
        return self.scenePath.rsplit('/')[-1]

    def getSceneDataPath(self):
        return os.path.join(self.dataPath, self.getSceneName())

    def getNodePath(self, node):
        self.node = node
        return os.path.join(self.getSceneDataPath(), self.node)


    def addData(self, node):
        self.node = node

        sceneDataPath = self.getSceneDataPath()
        nodePath = self.getNodePath(self.node)
       
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


    def getData(self, node, version = None):
        self.node = node
        cachesDict = {}
        cachesList = []
        filePath = ''
        nodePath = self.getNodePath(self.node)

        if os.path.exists(nodePath):
            for n in sorted(os.listdir(nodePath)):
                fullPath = os.path.join(nodePath, n)
                cachesList.append(fullPath)
            cachesDict[self.node] = cachesList

        if version:
            for n in cachesDict.values()[0]:
                if version in n:
                    firstFile = sorted(os.listdir(n))[0]
                    ext = firstFile.rsplit('.')[-1]
                    #print ext
                    if ext == 'bgeo':
                        padding = firstFile.rsplit(self.node)[-1].rsplit('.')[1]
                        filePath = os.path.join(n, firstFile.replace(padding, '$F4'))
                    if ext == 'abc':
                        filePath = os.path.join(n, firstFile)

                    return filePath
                    
        else: return cachesDict


    def getAllSceneData(self, fullPath):
        self.fullPath = fullPath
        caches = {}
        for n in sorted(os.listdir(self.getSceneDataPath())):
            list = []
            for m in self.getData(n).values()[0]:
                if self.fullPath == True: list.append(m)
                else: list.append(m.rsplit('/')[-1])
            caches[n] = list
        return caches