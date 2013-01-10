import sys
sys.path.append('/usr/pipeline/lib')
import pipe
import os
import socket
from time import strftime
import shutil
import filesys, re

pat = re.compile('.v\d{1,10}.')

def PipeDailies():
    
    n = nuke.selectedNode()
    
    sObj = pipe.Projects().GetAssetByInfo(nuke.root().name())
    
    movPath = sObj.GetShot().GetOutPath() + '/dailies/'
    
    renderPath = sObj.GetDataPath() + '/render/tmp_dailies/'
    
    if not os.path.exists(renderPath):
        
        os.mkdir(renderPath)
        
    shotObject = sObj.GetShot()
    seqObject = sObj.GetSequence()
    
    sName = shotObject.name + seqObject.GetPrefix()
    
       
    if not os.listdir(movPath):
        
        vNum = '.v001'       
        
    else:
		
		q = nuke.ask('Create new version?')
		
		if q: c = 1
		else: c = 0
		
		hList = filter(lambda x: pat.search(x) , os.listdir(movPath))
		hList = [int(x.rsplit('.', 2)[-2].split('v')[-1]) for x in hList if x[:len(sName)] == sName]
		if not hList:
			vNum = '.v001'      
		else:
			vNum = '.v' + filesys.padding(max(hList) + c, 3)
    
  
    
    
    pad = len(str(int(nuke.animationEnd())))
    
    wNode = nuke.createNode('Write', inpanel=False)
    
    wNode.knob('file').setValue(renderPath+sName+ vNum + '.%0' + str(pad) + 'd.jpg')
    
    # if there are Slate render is 1 frame longer
    
    if n.Class() == 'Slate' or n.Class() == 'slate2':
        
        r = nuke.render (wNode.name(), start=int(nuke.animationStart()), end=int(nuke.animationEnd())+1, incr=1)
    
    else:
        
        r = nuke.render (wNode.name(), start=int(nuke.animationStart()), end=int(nuke.animationEnd()), incr=1)
    
    nuke.delete(wNode)


    # mov creation    
    
    # paths to djv folder
    pp = os.getenv('PROGRAM_PATH')
    djv = 'LD_LIBRARY_PATH='+ pp + '/djv/lib ' + pp + '/djv/bin/djv_convert'
    djView = 'LD_LIBRARY_PATH='+ pp + '/djv/lib ' + pp + '/djv/bin/djv_view'
    
    print djv, djView
       
   
    jpgName = sName + vNum
    
    jpgList = [x for x in os.listdir(renderPath) if x[:len(jpgName)] == jpgName]
    
    jpgList.sort()
    
    sPath = renderPath + jpgList[0].rsplit('.', 1)[0] + '-' + jpgList[-1].rsplit('.', 2)[-2] + '.jpg'

    
    djvArg = sPath + ' ' + movPath + jpgName + '.mov' 
    

    # runs convertation
    os.system(djv + ' ' + djvArg)
    os.system('chmod 777' + ' ' + movPath + jpgName + '.mov')
    
    # clears tmp jpg folder
    
    shutil.rmtree(renderPath)

    # creates copy to REPO
    
    dPath = filesys.REPO + '/' + sObj.GetProject().name + '/out/dailies/' + strftime('%y.%m.%d')
    
    if not os.path.exists(dPath):
        os.makedirs(dPath)
    
    sPath = movPath + jpgName + '.mov'
    
    os.system('cd %s && ln -sf ../../../film/sequences/%s/shots/%s/out/dailies/%s'%(dPath,shotObject.seq_name,shotObject.name,str(jpgName + '.mov')))
    #os.system('cp -f ' + sPath + ' ' + dPath)
    
    # checkIn
    
    nuke.scriptSave()
    
    # make comment
    comment = 'Dailies creation v' + vNum.split('.')[-1]
    
    # send comment to DB
    sObj.Events().Add(comment,filesys.DAILIES, extra={'file':sPath,'user':filesys.USERNAME})
    
    # 
    sObj.CheckIn(comment, True)
    
    # opens *.mov file
    os.system(djView + ' ' + movPath + jpgName + '.mov')
    
    

    
    
    
    
    
    
    
    
    
