import os
import hou

def makeCachePath(object, mode):
    #get all path from HOUDINI VARIABLES

    sceneName = hou.getenv('HIPNAME').rsplit('.v',1)[0]
    dataPath = hou.getenv('DATA')
    geoPath = os.path.join(dataPath, "geo")
    scenePath = os.path.join(geoPath, sceneName)
    nodePath = os.path.join(scenePath, object.name())

    startVersion = 0
    
    #get mode - get cache info
    if mode == 'get':
        cachesList = []
        if os.path.exists(nodePath):
            for n in sorted(os.listdir(nodePath)):
                cachesList.append(os.path.join(nodePath, n))
            return cachesList
    
    #add mode - add new cache path
    if mode == 'add':
        versionPath = ''
        #mkdir cache for current scene
        if not os.path.exists(scenePath): os.mkdir(scenePath)
        #mkdir cache for current node
        if not os.path.exists(nodePath): os.mkdir(nodePath)
        
        if not os.listdir(nodePath):
            versionPath = os.path.join(nodePath, str(startVersion).zfill(3))
            os.mkdir(versionPath)
        else:
            currentVersion = int(max(os.listdir(nodePath)))
            if os.path.exists(os.path.join(nodePath, str(startVersion).zfill(3))):
                versionPath = os.path.join(nodePath, str(currentVersion + 1).zfill(3))
                os.mkdir(versionPath)
        return versionPath


def abcCacheWrite(startFrame, endFrame, subFrame, mode):

    selectedNodes = hou.selectedNodes()
    parent = selectedNodes[0].parent()
    ropnet = hou.node(parent.path()).createNode("ropnet")

    message = ''
    for n in selectedNodes:

        if mode == 'add':
            cachePath = makeCachePath(n, 'add')
        else:
            cachePath = makeCachePath(n, 'get')[-1]

        message += 'NODE' + ' - ' + n.path() + ' > ' + 'CACHE - $DATA/geo/' + cachePath.split('geo/')[1] + '/' + n.name() + '.abc' + '\n'
        alembic = hou.node(ropnet.path()).createNode("alembic")
        alembic.setName(n.name()+"_alembic")
    
        hou.node(alembic.path()).parm("trange").set(1)
        hou.node(alembic.path()).parm("f1").set(startFrame)
        hou.node(alembic.path()).parm("f2").set(endFrame)
        hou.node(alembic.path()).parm("f3").set(1.0/subFrame)
        hou.node(alembic.path()).parm("filename").set(cachePath + "/" + n.name() + ".abc")
        hou.node(alembic.path()).parm("objects").set(n.path())

        submitButton = alembic.parm("execute")
        hou.Parm.pressButton(submitButton)

    hou.ui.displayMessage(message)
    ropnet.destroy()
