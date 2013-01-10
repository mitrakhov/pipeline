# -*- coding: utf-8 -*-

import nuke
import os
import shutil

def findHighestRead():
	
	n = nuke.allNodes('Read')
	dic = {}
	for x in n:
		dic[x.ypos()]=x.name()
	minVal =  min(dic.keys())
	return dic[minVal]

def reloadAllReads():
	
	for read in nuke.allNodes('Read'):
		read.knob('reload').execute()


def switchStatus():
	
	if int(nuke.toNode('locController').knob('location').value()) == 0:
		nuke.toNode('status').knob('label').setValue('LOCAL')
	
	else:
		nuke.toNode('status').knob('label').setValue('NETWORK')



def setLocal():
	
# path variables

	repo = '/mnt/karramba'
	home = '/home/tfx/job.local'
	
# clears the selection if smth was selected	
	for node in nuke.allNodes():
		node.setSelected(False)

# copies footage to local machine

	readList = [node.knob('file').value() for node in nuke.allNodes('Read')]
	

	for path in readList:
		
		fileDirList =[path.rsplit(os.sep,1)[0] + os.sep + img for img in os.listdir(path.rsplit(os.sep,1)[0]) if img[:len(path.rsplit(os.sep,1)[1].split('%')[0])] == path.rsplit(os.sep,1)[1].split('%')[0]]
		newPath = home + path.rsplit(os.sep, 1)[0].split(repo)[-1] + os.sep
		
		if not os.path.exists(newPath):
			os.makedirs(newPath)
		
		for img in fileDirList:
			if not os.path.isdir(img):
				shutil.copy(img, newPath)

#creates new read nodes and controller to switch controller between local and network
			
	for node in nuke.allNodes('Read'):
		
		node.setSelected(True)
		
		sw = nuke.createNode('Switch', inpanel=False)
		sw.setSelected(False)
		sw.knob('which').setExpression('locController.location')
		node.setSelected(True)
		nuke.nodeCopy('%context%')
		c = nuke.nodePaste('%context%')
		
		sw.setInput(0, c)
		sw.setInput(1, node)
		
		node.setYpos(node.ypos()-90)
		c.setYpos(node.ypos())
		c.setXpos(node.xpos()-150)
		
		c.setName(c.name() + 'Local')
		node.setName(node.name() + 'Network')
		
		c.knob('file').setValue(home + node.knob('file').value().split(repo)[-1])
		
		node.setSelected(False)
		c.setSelected(False)

	n =	nuke.createNode('NoOp')
	n.setName('locController')
	k = nuke.Double_Knob('location', 'location')
	k.setRange(0, 1)
	n.addKnob(k)
	n.knob('hide_input').setValue(True)
	n.setXpos(nuke.toNode(findHighestRead()).xpos() + 500)
	n.setYpos(nuke.toNode(findHighestRead()).ypos())
	n.setSelected(False)
	
	st = nuke.createNode('StickyNote', inpanel=False)
	st.setName('status')
	st.setXpos(n.xpos())
	st.setYpos(n.ypos()-50)
	st.knob('label').setValue('LOCAL')
	st.knob('note_font_size').setValue(35)

	nuke.addKnobChanged(switchStatus, nodeClass='NoOp')

				

			
			
def addLocal():
	
	# path variables

	repo = '/mnt/karramba'
	home = '/home/tfx/job.local'
	

# copies footage to local machine

	readList = [node.knob('file').value() for node in nuke.selectedNodes('Read')]
	

	for path in readList:
		
		fileDirList =[path.rsplit(os.sep,1)[0] + os.sep + img for img in os.listdir(path.rsplit(os.sep,1)[0]) if img[:len(path.rsplit(os.sep,1)[1].split('%')[0])] == path.rsplit(os.sep,1)[1].split('%')[0]]
		
		for img in fileDirList:
			
			newPath = home + img.rsplit(os.sep, 1)[0].split(repo)[-1] + os.sep
			if not os.path.exists(newPath):
				os.makedirs(newPath)
			shutil.copy(img, newPath)

#creates new read nodes and controller to switch controller between local and network
			
	for node in nuke.selectedNodes('Read'):
		
		node.setSelected(True)
		
		sw = nuke.createNode('Switch', inpanel=False)
		sw.setSelected(False)
		sw.knob('which').setExpression('locController.location')
		node.setSelected(True)
		nuke.nodeCopy('%context%')
		c = nuke.nodePaste('%context%')
		
		sw.setInput(0, c)
		sw.setInput(1, node)
		
		node.setYpos(node.ypos()-90)
		c.setYpos(node.ypos())
		c.setXpos(node.xpos()-150)
		
		c.setName(c.name() + 'Local')
		node.setName(node.name() + 'Network')
		
		c.knob('file').setValue(home + node.knob('file').value().split(repo)[-1])
		
		node.setSelected(False)
		c.setSelected(False)
