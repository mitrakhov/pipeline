from shotgun_api3 import Shotgun
import os

def createProject():
    
    site = 'https://chimneypot.shotgunstudio.com'    
    scriptName = 'createProject'
    scriptKey = '90699580e396b61d3acfb71e0595adde7458dfd4'    
    
    repo = '/mnt/karramba/'    
        
    rootList = ['film', 'out', 'ref', 'src', 'temp']
    filmList = ['assets', 'sequences']    
    assetList = ['light', 'material', 'mattepaint', 'model', 'rig', 'shader', 'textures']
    shotList = ['anim', 'comp', 'data', 'fx', 'light', 'out', 'src', 'tmp']
    sqList = ['anim', 'comp', 'data', 'fx', 'light', 'out', 'shots']
    dataList = ['cache', 'geo', 'render', 'shadowmap', 'sim', 'track', 'photonmap']
    outList = ['dailies', 'hires']

    prName = raw_input('Print project name:')
    
    prPath = repo + prName     
    
    if not os.path.exists(prPath):
        os.mkdir(prPath)
        for i in rootList:
            os.makedirs(prPath + os.sep + i)
        for i in filmList:
            os.makedirs(prPath + os.sep + 'film' + os.sep + i)    
        for i in assetList:
            os.makedirs(prPath + os.sep + 'film' + os.sep + 'assets' + os.sep + i)
        for i in outList:
            os.makedirs(prPath + os.sep + 'out' + os.sep + i)

    sg = Shotgun(site, scriptName, scriptKey)
    sg.create('Project', {'name':prName})    
    
createProject()
