import sys
sys.path.append('/usr/pipeline/lib')
import pipe
import os
import filesys
import re

'''Script for creation HiRes 
for TCP internal use
Anton Mitrakhov'''

pat = re.compile('^\d{1,10}')

def CreateHires():

	# settings variables
	
	ext = 'dpx'
	cSpace = 'Cineon'
	pad = '.%06d.'	
	
	# creating paths and HiRes name
	
	sObj = pipe.Projects().GetAssetByInfo(nuke.root().name())
	nPath = sObj.GetCurrentActualPath()
	hName = sObj.GetShot().name + pad + ext
	hFPath = sObj.GetShot().GetOutPath() + '/hires/'
	hList = os.listdir(hFPath)
	

	# write node creation
	if nuke.toNode('HiRes'):
		
		nuke.message('Node HiRes already exists. Use that one, %username% :-)')
		pass
	
	else:
			
		sNode = nuke.selectedNode()
		hNode = nuke.createNode('Write', inpanel=False)
		hNode.knob('name').setValue('HiRes')
		hNode.knob('beforeRender').setValue('newRender()')
		hNode.knob('afterRender').setValue('getHiresSQ()')	
		hNode.knob('colorspace').setValue(cSpace)
		hNode.knob('channels').setValue('rgb')
		
		# Hires folder is empty
	
	
		if not hList:
			
			hFolder = hFPath + str(filesys.padding(1, 2))
		
			os.mkdir(hFolder)
		
			hNode.knob('file').setValue(hFolder + os.sep + hName)
			
			rq = nuke.ask('Render now?')
			
			if rq:
				
				hNode.knob('Render').execute()
			
	
		# Hires folder is not empty
	
		else:
			hList = filter(lambda x: pat.search(x) , hList)
			if hList:
				hFolder = hFPath + str(filesys.padding(max([(int(f)) for f in hList]), 2))
			else:
				hFolder = hFPath + '01'
	
			hNode.knob('file').setValue(hFolder + os.sep + hName)
			
			rq = nuke.ask('Render now?')
	
			if rq:
				
				hNode.knob('Render').execute()



# callback function on the beforeRender knob

def newRender():
	pat = re.compile('^\d{1,10}')
	n = nuke.selectedNode()
	fPath = n.knob('file').value()
	curHList = os.listdir(fPath.rsplit(os.sep, 1)[0])
	hFolder = fPath.rsplit(os.sep, 2)[0]
	hName = fPath.rsplit(os.sep, 1)[-1]
	lPath = nuke.root().name()
	
	if curHList:
		
		q = nuke.ask('Create new version?')
		
		if q:
			vDirs = os.listdir(hFolder)
			#raise Exception( vDirs)
			vDirs = filter(lambda x: pat.search(x) , vDirs)
			#raise Exception( vDirs)
			if vDirs:
				hFPath = hFolder + os.sep + str(filesys.padding(max([(int(f)) for f in vDirs]) + 1, 2))
			else:
				hFPath =hFolder + os.sep + str(filesys.padding(1, 2))
			#hFPath = hFolder + os.sep + str(filesys.padding(max([(int(f)) for f in vDirs]) + 1, 2))
			os.mkdir(hFPath)
			
			pipe.Projects().GetAssetByInfo(lPath).CheckIn('HiRes creation\n' + hFPath + os.sep + hName, True)
			
			n.knob('file').setValue(hFPath + os.sep + hName)
			
		else:
			
			nuke.scriptSave()
			pipe.Projects().GetAssetByInfo(lPath).CheckIn('HiRes creation v' + fPath.rsplit('/',2)[-2], True)

	else:
		
		nuke.scriptSave()
		pipe.Projects().GetAssetByInfo(lPath).CheckIn('HiRes creation v' + fPath.rsplit('/',2)[-2], True)
		
		
# callback function on the afterRender knob		

def getHiresSQ():
	pat = re.compile('^\d{1,10}')
	n = nuke.toNode('HiRes')
	xpos = n.knob('xpos').value()
	ypos = n.knob('ypos').value()
	
	sObj = pipe.Projects().GetAssetByInfo(nuke.root().name())
	hPath = sObj.GetShot().GetOutPath() + '/hires/'
	
	os.system('chmod 777 -R ' + hPath)
	
	vDirs = filter(lambda x: pat.search(x) , os.listdir(hPath))
	
	sName = sObj.GetShot().name	
	sqName = sObj.GetShot().seq_name
	seqObject = sObj.GetSequence()
	
	if vDirs:
		cPath = os.path.join(hPath,str(filesys.padding(max([(int(f)) for f in vDirs]),2)))
	else:
		cPath = os.path.join(hPath,str(filesys.padding(1,2)))
	hList = os.listdir(cPath)
	hList.sort()
	fUText = cPath + os.sep + hList[-1].rsplit('.',2)[0] + '.%0' + str(len(max(hList).rsplit('.', 2)[-2])) + 'd.' + hList[-1].split('.')[-1] + ' ' + str(int(hList[0].rsplit('.', 2)[-2])) + '-' + str(int(hList[-1].rsplit('.', 2)[-2]))
	
	dPath = os.path.join(filesys.REPO, sObj.GetProject().name, filesys.OUT,'hires',sqName, sName + seqObject.GetPrefix())
	
	if not os.path.exists(dPath):	filesys.mkdirs(dPath)

	shotObject = sObj.GetShot()
	sName = shotObject.name
	num_folder = cPath.split(os.sep)[-1]
	
	os.system('cd %s && ln -sf ../../../../film/sequences/%s/shots/%s/out/hires/%s'%(dPath,shotObject.seq_name,sName, num_folder ))
	
	r = nuke.createNode('Read')
	r.knob('name').setValue('Hires')
	r.knob('file').fromUserText(fUText)
	r.knob('xpos').setValue(xpos + 100)
	r.knob('ypos').setValue(ypos)

