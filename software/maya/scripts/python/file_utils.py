from pymel.core import *
import os

def exportSelectedToObj():
    path = sceneName()

    if path:
        workDir = path.rsplit('/', 1)[0]
        sceneLabel = path.rsplit('/', 1)[1]
        exportPath = os.path.join(workDir, sceneLabel.rsplit('.mb', 1)[0])

    if not os.path.exists(exportPath):
        os.mkdir(exportPath)
        
    print exportPath

    objects = selected()
    for n in objects:
        select(n)
        exportSelected(exportPath + "/" + n + ".obj", type = "OBJexport", options = "groups=1; ptgroups=0; materials=0; smoothing=1; normals=1")
