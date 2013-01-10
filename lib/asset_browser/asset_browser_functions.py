from shotgun_api3 import Shotgun
from pprint import pprint
import os


def getAllProjects():
    
    site = 'https://chimneypot.shotgunstudio.com'    
    scriptName = 'AssetBrowser'
    scriptKey = 'c35ab5f5322d4b1e8b6488bb315c03e5f38881ea'    
    
    sg = Shotgun(site, scriptName, scriptKey)    

    fields = ['id','name','type']
    projects= sg.find("Project",[],fields)
    
    if len(projects) < 1:
        print "couldn't find any projects"
        #exit(0)
    else:
        print "Found "+str(len(projects))+" projects"
#        pprint (projects)
    
    return projects 


def getSequencesByProjId(proj_id):
    
    site = 'https://chimneypot.shotgunstudio.com'    
    scriptName = 'AssetBrowser'
    scriptKey = 'c35ab5f5322d4b1e8b6488bb315c03e5f38881ea'    
    
    sg = Shotgun(site, scriptName, scriptKey)

    fields = ['id','type','code']
    filters = [['project','is',{'type':'Project','id':proj_id}]]
    sequences= sg.find("Sequence",filters,fields)
    
    if len(sequences) < 1:
        print "couldn't find any sequences"
        #exit(0)
    else:
        None   

    return sequences


def getShotsBySeqId(seq_id):
    
    site = 'https://chimneypot.shotgunstudio.com'    
    scriptName = 'AssetBrowser'
    scriptKey = 'c35ab5f5322d4b1e8b6488bb315c03e5f38881ea'    
    
    sg = Shotgun(site, scriptName, scriptKey)

    fields = ['id','type','code']
    filters = [['sg_sequence','is',{'type':'Sequence','id':seq_id}]]
    shots= sg.find("Shot",filters,fields)
    
    if len(shots) < 1:
        print "couldn't find any shots"
        #exit(0)
    else:
        None   

    return shots


def getAssetsBySeqId(seq_id):
    
    site = 'https://chimneypot.shotgunstudio.com'    
    scriptName = 'AssetBrowser'
    scriptKey = 'c35ab5f5322d4b1e8b6488bb315c03e5f38881ea'
    
    fields = ['id', 'code', 'sg_asset_type']
    sequence_id = 2 # Sequence 100_FOO
    project_id = 4 # Demo Project
    filters = [
    ['project','is',{'type':'Project','id':project_id}],
    ['sg_asset_type','is', 'Character'],
    ['sequences', 'is', {'type':'Sequence','id':sequence_id}]
    ]
    assets= sg.find("Asset",filters,fields)
    if len(assets) < 1:
        print "couldn't find any assets"
        #exit(0)
    else:
        print "Found "+str(len(assets))+" assets"
        pprint (assets)


def createJobLocalDir():
    
    site = 'https://chimneypot.shotgunstudio.com'    
    scriptName = 'AssetBrowser'
    scriptKey = 'c35ab5f5322d4b1e8b6488bb315c03e5f38881ea'
    
    job_local = os.path.expanduser("~") + os.sep + 'job.local'
    print job_local
            
    if not os.path.exists(job_local):
        os.mkdir(job_local)