from shotgun_api3 import Shotgun
import os
import shutil

def addSrc():

    repo = '/mnt/karramba'

    shotFoldList = ['anim', 'comp', 'data', 'fx', 'light', 'out', 'src', 'tmp']
    seqFoldList = ['anim', 'comp', 'data', 'fx', 'light', 'out', 'shots']
    dataFoldList = ['cache', 'geo', 'render', 'shadowmap', 'sim', 'track', 'photonmap']
    outFoldList = ['dailies', 'hires']    
    
    site = 'https://chimneypot.shotgunstudio.com'    
    scriptName = 'addSrc'
    scriptKey = 'd7dac4e2c55faf486875dfb944ffc9d8e49a0c44'

    sg = Shotgun(site, scriptName, scriptKey)

    
    projList = sg.find('Project', [], ['name'])
    
    for i in projList:
        
        print 'id:' + str(i['id']) + ' ' + i['name']    
        
    prId = int(raw_input('Print project id:'))
    
    proj = sg.find_one('Project', [['id','is',prId]], ['name'])

    
    if not [x for x in os.listdir(repo) if x==proj['name']]:
        print "Project doesn't exist in repository"
        return
    


    s = os.sep
    
    prPath = repo + s + proj['name']
    seqPath = prPath + s + 'film' + s + 'sequences'
    seqList = os.listdir(prPath + s + 'src')
    
    for i in seqList:
        sequenceFold = prPath + s + 'film' + s + 'sequences'
        os.makedirs(sequenceFold + s + i)
        for j in seqFoldList:
            os.makedirs(sequenceFold + s + i + s + j)
        for d in dataFoldList:
            os.makedirs(sequenceFold + s + i + s + 'data' + s + d)
        for o in outFoldList:
            os.makedirs(sequenceFold + s + i + s + 'out' + s + o)
        shList = os.listdir(prPath + s + 'src' + s + i)
        for sh in shList:
            shFold = sequenceFold + s + i + s + 'shots'
            os.makedirs(shFold + s + sh)            
            for f in shotFoldList:
                os.makedirs(shFold + s + sh + s + f)
            for ds in dataFoldList:
                os.makedirs(shFold + s + sh + s + 'data' + s + ds)
            for ot in outFoldList:
                os.makedirs(shFold + s + sh + s + 'out' + s + ot)
            shutil.move(prPath + s + 'src' + s + i + s + sh, shFold + s + sh + s + 'src')
            os.system('ln -sf ' + shFold + s + sh + s + 'src ' + prPath + s + 'src' + s + i + s + sh)
                
addSrc()    
