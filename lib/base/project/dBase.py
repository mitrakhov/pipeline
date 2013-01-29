from shotgun_api3 import Shotgun

site = 'https://chimneypot.shotgunstudio.com'    
scriptName = 'createProject'
scriptKey = '90699580e396b61d3acfb71e0595adde7458dfd4'


def createProject(prName):
    sg.create('Project', {'name':prName})


        
        