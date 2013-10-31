from pymel.core import *
import common_utils

def bakeObjectAnimToWorldGui():
	try:
		window(bakeObjectAnimToWorldWin, exists = True)
	except NameError:
		bakeObjectAnimToWorldWin = window(title = 'Bake Object Animation', widthHeight = (300, 100))

	if window(bakeObjectAnimToWorldWin, exists = True):
	    deleteUI(bakeObjectAnimToWorldWin)
	        
	bakeObjectAnimToWorldWin = window(title = 'Bake Object Animation', widthHeight = (300, 100))
	columnLayout(adjustableColumn = True)
	startFrameFF = floatField(ann = 'Start Frame', precision = 0, step = 1, value = playbackOptions(query = True, minTime = True), width = 20)
	endFrameFF = floatField(ann = 'End Frame', precision = 0, step = 1, value = playbackOptions(query = True, maxTime = True), width = 20)

	button(label = 'Bake',command = ('common_utils.bakeObjectAnimToWorld(selected(), startFrameFF.getValue(), endFrameFF.getValue())') )

	setParent('..')
	showWindow(bakeObjectAnimToWorldWin)