import os
import hou

def makeCachePath(object, mode):
    #get all path from HOUDINI VARIABLES

    sceneName = hou.getenv('HIPNAME').rsplit('.v',1)[0]
    #sceneName = hou.getenv('HIPNAME')
    print sceneName
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
            versionPath = os.path.join(nodePath, str(startVersion).zfill(4))
            os.mkdir(versionPath)
        else:
            currentVersion = int(max(os.listdir(nodePath)))
            if os.path.exists(os.path.join(nodePath, str(startVersion).zfill(4))):
                versionPath = os.path.join(nodePath, str(currentVersion + 1).zfill(4))
                os.mkdir(versionPath)
        return versionPath


def cacheWrite(startFrame, endFrame, subFrame, format, mode):
#expected format abc(Alembic), bgeo(Houdini bgeo)
#expected mode add,


    selectedNodes = hou.selectedNodes()
    parent = selectedNodes[0].parent()
    ropnet = hou.node(parent.path()).createNode("ropnet")

    hou.setFrame(startFrame)

    message = ''

    for n in selectedNodes:

        if mode == 'version': cachePath = makeCachePath(n, 'add')
        if mode == 'overwrite': cachePath = makeCachePath(n, 'get')[-1]
           
        if format == 'abc': cacheProperty = ['abc', 'alembic', 'filename', '.abc', 'objects']
        if format == 'bgeo': cacheProperty = ['$F4.bgeo', 'geometry', 'sopoutput', '.$F4.bgeo', 'soppath']


        message += 'NODE' + ' - ' + n.path() + ' > ' + 'CACHE - $DATA/geo/' + cachePath.split('geo/')[1] + '/' + n.name() + '.' + cacheProperty[0] + '\n'
        
        
        ropNode = hou.node(ropnet.path()).createNode(cacheProperty[1])

        ropNode.setName(n.name()+"_ropNode")
    
        hou.node(ropNode.path()).parm("trange").set(1)
        hou.node(ropNode.path()).parm("f1").set(startFrame)
        hou.node(ropNode.path()).parm("f2").set(endFrame)
        hou.node(ropNode.path()).parm("f3").set(1.0/subFrame)
        
        
        hou.node(ropNode.path()).parm(cacheProperty[2]).set(os.path.join(cachePath, n.name() + cacheProperty[3]))
        
        
        hou.node(ropNode.path()).parm(cacheProperty[4]).set(n.path())

        submitButton = ropNode.parm("execute")
        hou.Parm.pressButton(submitButton)

    hou.ui.displayMessage(message)
    ropnet.destroy()
