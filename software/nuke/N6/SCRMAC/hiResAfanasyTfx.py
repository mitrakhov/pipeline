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

def CreateHiresByAfanasy():
	
	
	# check for all read nodes
	readList = [(node.knob('name').value(),node.knob('file').value()) for node in nuke.allNodes('Read')]
	rlen = len(filesys.REPO)
	suspected = [n for n in readList if n[1][:rlen] != filesys.REPO]
	if suspected: raise Exception('Error! Files in nodes below have to move into %s:\n%s'%(filesys.REPO,'\n'.join([str('%s - %s'%(n[0],n[1])) for n in suspected])))
			
	# settings variables
	
	ext = 'dpx'
	cSpace = 'sRGB'
	pad = '.%06d.'	
	
	# creating paths and HiRes name
	
	sObj = pipe.Projects().GetAssetByInfo(nuke.root().name())
	nPath = sObj.GetCurrentActualPath()
	hName = sObj.GetShot().name + pad + ext
	hFPath = sObj.GetShot().GetOutPath() + '/hires/'
	hList = os.listdir(hFPath)
	hFolder = ''

	# write node creation
	if nuke.toNode('HiRes'):
		
		nuke.message('Node HiRes already exists. Use that one, %username% :-)')
		pass
	
	else:
			
		sNode = nuke.selectedNode()
		hNode = nuke.createNode('Write', inpanel=False)
		hNode.knob('name').setValue('HiRes')
		hNode.knob('colorspace').setValue(cSpace)
		hNode.knob('channels').setValue('rgb')
		
		aNode = nuke.createNode("afanasy", inpanel=False)
		aNode.knob('hmask').setValue('tfxr.*')
		aNode.knob('jname').setValue('%s'%sObj.name)
		aNode.knob('first').setValue(nuke.root().firstFrame())
		aNode.knob('last').setValue(nuke.root().lastFrame())
		
		# Hires folder is empty
		if not hList:
			hFolder = hFPath + str(filesys.padding(1, 2))
			os.mkdir(hFolder)
			hNode.knob('file').setValue(hFolder + os.sep + hName)
		# Hires folder is not empty
		else:
			hList = filter(lambda x: pat.search(x) , hList)
			hFolder = hFPath + str(filesys.padding(max([(int(f)) for f in hList]), 2))
			hNode.knob('file').setValue(hFolder + os.sep + hName)
	
	#Make link into out/hires folder
	shotObject = sObj.GetShot()
	sName = shotObject.name
	seqObject = sObj.GetSequence()
	
	dPath = os.path.join(filesys.REPO, sObj.GetProject().name, filesys.OUT,'hires',shotObject.seq_name, sName + seqObject.GetPrefix())
	if not os.path.exists(dPath):	filesys.mkdirs(dPath)
	num_folder = hFolder.split(os.sep)[-1]
	
	os.system('cd %s && ln -sf ../../../../film/sequences/%s/shots/%s/out/hires/%s'%(dPath,shotObject.seq_name,sName, num_folder ))

			
	
