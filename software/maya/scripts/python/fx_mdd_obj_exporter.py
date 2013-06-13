
'''
Author: Alex Manita
Description: This tool designed primarily for export meshes and particles out of maya,
so they could be imported later into Houdini and other packages
Usage: 

import fx_mdd_obj_exporter
fx_mdd_obj_exporter.runUI()

License: You can use it everywhere and modify but you cant sell it.
Use and Modify it at your own risk with absolutelly no warranties.

'''


from struct import pack
import maya.OpenMaya as OpenMaya
import maya.cmds as cmds
import os,re

	
def zero_file(filepath):
	'''
	If a file fails, this replaces it with 1 char, better not remove it?
	'''
	file = open(filepath, 'w')
	file.write('\n') # aparently macosx needs some data in a blank file?
	file.close()


def check_vertcount(exportedObjects,vertcount,mddFile):
	'''
	check and make sure the vertcount is consistent throghout the frame range
	'''
	totalCount = 0
	for each in exportedObjects:
		currentObject = nameToNode(each[1])
		
		iteratorObject = OpenMaya.MItMeshVertex(currentObject)
		totalCount += iteratorObject.count()
	if totalCount != vertcount:
		print 'Error number of verts has changed during animation cannot export'
		mddFile.close()
		zero_file(filepath)
		return
	
def getVertexCount(objects):
	numverts = 0
	for object in objects:
		exportedObjectShape = object[1]
		# Convert the string name to an actual object
		mesh_orig =  nameToNode(exportedObjectShape)
		#We should get reference frame from start frame
		# Create the vertex iterator with that object
		objectSurfaceIt = OpenMaya.MItMeshVertex(mesh_orig)
		# Get number of vertices	
		numverts += objectSurfaceIt.count()	
	return numverts
	
def nameToNode( name ):
	selectionList = OpenMaya.MSelectionList()
	selectionList.add( name )
	node = OpenMaya.MObject()
	selectionList.getDependNode( 0, node )
	return node

#def getSelectedVertexPositions(currentObjectName,transformMatrix):

def getSelectedVertexPositions(exportedObjects):
	vertexPositionList = []
	for exportedObject in exportedObjects:
		transform = exportedObject[0]
		# Convert the string name to an actual object
		shape = nameToNode(exportedObject[1])
		transformMatrix = getObjectTransform(transform)
		# Create the surfaceVertex iterator with that object
		objectSurfaceIt = OpenMaya.MItMeshVertex(shape)
		# Use that iterator for something - here it's returning a list of CV positions
		while not objectSurfaceIt.isDone():
			position = objectSurfaceIt.position() *transformMatrix # returns an object of type MPoint multiplied by transform matrix
			vertexPositionList.append(position.x)
			vertexPositionList.append(position.y)
			vertexPositionList.append(position.z)
			objectSurfaceIt.next()

        #Return the list of CV positions
	return vertexPositionList

def getObjectTransform(exportedObjectTransform):
	mat_flip = OpenMaya.MMatrix()
	mat_flip_list = [1.0, 0.0, 0.0, 0.0,0.0, 1.0, 0.0, 0.0,0.0, 0.0, 1.0, 0.0,0.0, 0.0, 0.0, 1.0]
	worldMatrixList = cmds.getAttr('%s.worldMatrix'%exportedObjectTransform)
	# Convert list to MMatrix object
	temp_mMatrix = OpenMaya.MMatrix()
	OpenMaya.MScriptUtil.createMatrixFromList(worldMatrixList, temp_mMatrix)
	transform = temp_mMatrix * mat_flip	
	return transform

def isExportableObjects(exportedObjects,mode):
	failCount = 0
	if mode == "mdd":
		for each in exportedObjects:
			if cmds.objectType( each[1] ) != "mesh":
				failCount+=1
	if mode == "particle":
		if cmds.objectType( exportedObjects[1] ) != "nParticle" and cmds.objectType( exportedObjects[1] ) != "particle":
			print exportedObjects[1]
			failCount+=1
		else:
			pass
	if failCount:
		return 0
	else:
		return 1
	
# exportedObjects have format [(transformNode, objectShape),...]
def mddExport(filepath, exportedObjects, startFrame, endFrame, fps):
	(difName,basename) = getDirFromParh(filepath)
	filepath = difName+"/"+basename+".mdd"
	filepathObj = difName+"/"+basename+".obj"

	mddFile = open(filepath, 'wb') #no Errors yet:Safe to create file
	numframes = endFrame-startFrame+1
	# set reference frame time
	cmds.currentTime( startFrame, edit=True )
	cmds.file(filepathObj,op="groups=1;ptgroups=1;materials=0;smoothing=1;normals=1",typ="OBJexport",pr=1,es=1,force=1)

	# Write the header
	numverts = getVertexCount(exportedObjects)
	mddFile.write(pack(">2i", numframes, numverts))
	
	## Write the frame times, sec
	mddFile.write( pack(">%df" % (numframes), *[frame/fps for frame in xrange(numframes)]) ) # seconds	
	#checking vertex count for the model
	check_vertcount(exportedObjects,numverts,mddFile)
	
	# Use that iterator for something - here it's returning a list of vertex positions
	vertexPositionList= getSelectedVertexPositions(exportedObjects)
	# write out referece model vertex position
	mddFile.write(pack(">%df" % (numverts*3), *[v for v in vertexPositionList]))
	vertexPositionList = None
	amount = 0
	frameRange = (endFrame-startFrame)+1

	cmds.progressWindow(	title='Exporting sequence',
					progress=amount,
					status='Finished: 0%',
					isInterruptable=True ,
	                                maxValue = frameRange)
	for frame in xrange(startFrame,endFrame+1):#in order to start at desired frame
		if cmds.progressWindow( query=True, isCancelled=True ) :
			break
		cmds.currentTime( frame, edit=True )
		# Check vertex  count, its shouldnt be changed over time
		check_vertcount(exportedObjects,numverts,mddFile)
		vertexPositionList= getSelectedVertexPositions(exportedObjects)
		# Write the vertex data
		mddFile.write(pack(">%df" % (numverts*3), *[v for v in vertexPositionList]))
		if cmds.progressWindow( query=True, progress=True ) >= frameRange  :
			break
		amount += 1
		cmds.progressWindow( edit=True, progress=amount, status=('Finished: ' + `amount` + '%' ) )
	cmds.progressWindow(endProgress=1)
	vertexPositionList = None
	mddFile.close()
	
def objExport(filepath,  startFrame, endFrame, inc):
	(difName,basename) = getDirFromParh(filepath)
	# Here we dont specify "op" (option) parameter, because we want to have option to get it from maya "export Selection" dialog, so whetever is active there, will be exported using this command
	amount = 0
	frameRange = (endFrame-startFrame)+1
	cmds.progressWindow(	title='Exporting sequence',
					progress=amount,
					status='Finished: 0%',
					isInterruptable=True ,
	                                maxValue = frameRange)
	
	for frame in range(startFrame,endFrame,inc):
		if cmds.progressWindow( query=True, isCancelled=True ) :
			break
		cmds.currentTime( frame, edit=True )
		cmds.file(difName+"/"+basename+"."+str(frame).zfill(5)+".obj",op="groups=1;ptgroups=1;materials=0;smoothing=1;normals=1",typ="OBJexport",pr=1,es=1,force=1)
		if cmds.progressWindow( query=True, progress=True ) >= frameRange  :
			break
		amount += 1
		cmds.progressWindow( edit=True, progress=amount, status=('Finished: ' + `amount` + '%' ) )
	cmds.progressWindow(endProgress=1)
		
def particleExport(filepath,  startFrame, endFrame, inc,particleTuple, userveca="",uservecb="",userfloa="",userflob=""):
	pTransform = particleTuple[0]
	pshape = particleTuple[1]
	if cmds.objectType( pshape ) == "particle" or cmds.objectType( pshape ) == "nParticle":
		cmds.runup( maxFrame=startFrame)

		arad=1 if cmds.objExists(pshape+".radiusPP") else 0
		arot=1 if cmds.objExists(pshape+".rot") else 0
		avel=1 if cmds.objExists(pshape+".velocity") else 0
		aid=1 if cmds.objExists(pshape+".id") else 0
		alife=1 if cmds.objExists(pshape+".lifespanPP") else 0
		aage=1 if cmds.objExists(pshape+".age") else 0
		argb=1 if cmds.objExists(pshape+".rgbPP") else 0
		aopacity=1 if cmds.objExists(pshape+".opacityPP") else 0
		amass=1 if cmds.objExists(pshape+".mass") else 0
		auserveca=1 if cmds.objExists(pshape+"."+userveca) else 0
		auservecb=1 if cmds.objExists(pshape+"."+uservecb) else 0
		auserfloa=1 if cmds.objExists(pshape+"."+userfloa) else 0
		auserflob=1 if cmds.objExists(pshape+"."+userflob) else 0
		attrNum = arad + arot + avel + aid + alife + aage + argb + aopacity + amass + auserveca + auservecb + auserfloa + auserflob;
		
		svel = "v 3 vector 0 0 0 \n" if avel else ""
		srad = "pscale 1 float 1 \n" if arad else ""
		srot = "rot 3 vector 0 0 0 \n" if arot else ""
		sid = "id 1 float 1 \n" if aid else ""
		slife  = "life 1 float 1 \n" if alife else ""
		sage = "age 1 float 1 \n" if aage else ""
		srgb = "Cd 3 vector 0 0 0 \n" if argb else ""
		sopacity = "opacity 1 float 1 \n" if aopacity else ""
		smass = "mass 1 float 1 \n" if amass else ""
		suserveca = (userveca +" 3 vector 0 0 0 \n") if auserveca else ""
		suservecb = (uservecb +" 3 vector 0 0 0 \n") if auservecb else ""
		suserfloa = (userfloa +" 1 float 1 \n") if auserfloa else ""
		suserflob = (userflob +" 1 float 1 \n") if auserflob else ""
		(difName,basename) = getDirFromParh(filepath)	
		particleCount = cmds.particle(pTransform,q=1, count=1)
		
		for frame in xrange(startFrame,endFrame+1):#in order to start at desired frame
			cmds.currentTime( frame, edit=True )
			finalFilePath = difName+"/"+basename+"."+str(frame).zfill(5)+".geo"
			particleFile  = open(finalFilePath, 'w')
	
			particleFile.write("PGEOMETRY V5 \nNPoints " + str(cmds.particle(pTransform,q=1, count=1)) + " NPrims 0 \nNPointGroups 0 NPrimGroups 0 \nNPointAttrib "+str(attrNum)+" NVertexAttrib 0 NPrimAttrib 0 NAttrib 1 \nPointAttrib \n"+svel+srad+srot+sid+slife+sage+srgb+sopacity+smass+suserveca+suservecb+suserfloa+suserflob);
	
			for fr in range(cmds.particle(pTransform,q=1, count=1)) :
				
				posb = cmds.getParticleAttr(pshape+".pt"+"["+str(fr)+"]",attribute = 'worldPosition')
				if avel:velb = cmds.getParticleAttr(pshape+".pt"+"["+str(fr)+"]",attribute = 'velocity')
				if arad:scaleb = cmds.getParticleAttr(pshape+".pt"+"["+str(fr)+"]",attribute = 'radiusPP')
				if arot:rotb = cmds.getParticleAttr(pshape+".pt"+"["+str(fr)+"]",attribute = 'rot')
				if aid:idb = cmds.getParticleAttr(pshape+".pt"+"["+str(fr)+"]",attribute = 'id')
				if alife:lifeb = cmds.getParticleAttr(pshape+".pt"+"["+str(fr)+"]",attribute = 'lifespanPP')
				if aage:ageb = cmds.getParticleAttr(pshape+".pt"+"["+str(fr)+"]",attribute = 'age')
				if argb:rgbb = cmds.getParticleAttr(pshape+".pt"+"["+str(fr)+"]",attribute = 'rgbPP')
				if aopacity:opacityb = cmds.getParticleAttr(pshape+".pt"+"["+str(fr)+"]",attribute = 'opacityPP')
				if amass:massb = cmds.getParticleAttr(pshape+".pt"+"["+str(fr)+"]",attribute = 'mass')
				if auserveca:uservecab = cmds.getParticleAttr(pshape+".pt"+"["+str(fr)+"]",attribute = userveca)
				if auservecb:uservecbb = cmds.getParticleAttr(pshape+".pt"+"["+str(fr)+"]",attribute = uservecb)
				if auserfloa:userfloab = cmds.getParticleAttr(pshape+".pt"+"["+str(fr)+"]",attribute = userfloa)
				if auserflob:userflobb = cmds.getParticleAttr(pshape+".pt"+"["+str(fr)+"]",attribute = userflob)
				
				fvel = str(velb[0]) +" "+ str(velb[1])+" "+str(velb[2])+" " if avel else ""
				frad = str(scaleb[0])+" " if arad else ""
	
				frot = str(rotb[0]) +" "+ str(rotb[1])+" "+str(rotb[2])+" " if arot else ""
				fid = str(idb[0])+" " if aid else ""
				flife = str(lifeb[0])+" " if alife else ""
				fage = str(ageb[0])+" " if aage else ""
				frgb = str(rgbb[0]) +" "+ str(rgbb[1])+" "+str(rgbb[2])+" " if argb else ""
				fopacity = str(opacityb[0])+" " if aopacity else ""
				fmass = str(massb[0])+" " if amass else ""
				fuserveca = str(uservecab[0]) +" "+ str(uservecab[1])+" "+str(uservecab[2])+" " if auserveca else ""
				fuservecb = str(uservecbb[0]) +" "+ str(uservecbb[1])+" "+str(uservecbb[2])+" " if auservecb else ""
				fuserfloa = str(userfloab[0])+" " if auserfloa else ""
				fuserflob = str(userflobb[0])+" " if auserflob else ""
				
	
			
				if cmds.particle(pTransform,q=1, count=1) != 0:
					particleFile.write(str(posb[0]) + " " + str(posb[1]) + " " + str(posb[2]) + " 1 (" + fvel + frad + frot + fid + flife + fage + frgb + fopacity + fmass + fuserveca + fuservecb + fuserfloa + fuserflob +") \n")
			      
			particleFile.write("DetailAttrib \nvarmap 1 index 1 \"v -> v\"  \n (0) \nbeginExtra \nendExtra")
			particleFile.close()			
	else:
		print "Select particles first...."
	
def launchExport (*args):
	try:
		if cmds.pluginInfo("objExport.mll",q=1,loaded=1) ==False:
			cmds.loadPlugin("objExport.mll",quiet=1)
	except:
		print "Cannot load obj plugin..."
	startFrame  = cmds.intFieldGrp('em_rangeSlider',  q=1,value1=1)
	endFrame = cmds.intFieldGrp('em_rangeSlider',  q=1,value2=1)
	inc = cmds.intFieldGrp('em_rangeSlider',  q=1,value3=1)
	userveca = cmds.textField('userVector1',q=1,text=1)
	uservecb = cmds.textField('userVector2',q=1,text=1)
	userflota= cmds.textField('userFloat1',q=1,text=1)
	userflotb= cmds.textField('userFloat2',q=1,text=1)
	frameRate = cmds.floatFieldGrp( 'em_frate',q=1, value1=getMayaFrameRate() )
	# Mode is 1- obj, 2-mdd, 3 - particles to geo
	mode  = cmds.radioButtonGrp( 'em_modeRadio',q=1, select=1)
	filepath =  cmds.textFieldButtonGrp('em_fileName',q=1, text=1)
	if mode == 1:
		if filepath and inc:
			if endFrame > startFrame:
				objExport(filepath, startFrame, endFrame, inc)	

	if mode == 2:
		selObjects = cmds.ls(sl=True, typ='transform')
		exportedObjects = []
		for eachObject in selObjects:
			shapeObject =  cmds.listRelatives(eachObject,s=1)	
			if shapeObject:
				exportedObjects.append((eachObject,shapeObject[0]))
		if isExportableObjects(exportedObjects,'mdd'):
			if filepath and exportedObjects  and frameRate:
				if endFrame > startFrame:
					mddExport(filepath, exportedObjects, startFrame, endFrame, frameRate)	
		else:
			print "Please select only polygonal objects for  MDD export..."
	if mode == 3:
		particleTransform = cmds.ls(sl=True, typ='transform')
		particleShape =  cmds.listRelatives(particleTransform[0],s=1)
		particleTuple = (particleTransform[0],particleShape[0])
		if isExportableObjects(particleTuple,'particle'):
			particleExport(filepath,  startFrame, endFrame, inc,particleTuple, userveca,uservecb,userflota,userflotb)
		else:
			print "Please select only particle objects for  Particle export..."
		
def getMayaFrameRate():
	frameRate = float(24)
	currentFps = cmds.currentUnit( query=True, time=True )
	if currentFps == 'film':
		frameRate =float(24)
	if currentFps == 'pal':
		frameRate =float(25)		
	if currentFps == 'show':
		frameRate =float(48)		
	if currentFps == 'palf':
		frameRate =float(50)
	if currentFps == 'ntscf':
		frameRate =float(60)		
	if currentFps == 'game':
		frameRate =float(15)	
	return frameRate
		
def getExportFilePathUI():
	mode  = cmds.radioButtonGrp( 'em_modeRadio',q=1, select=1)
	if mode ==1:
		filePath = cmds.fileDialog(mode=1, dm=('*.obj') )
	if mode ==2:
		filePath = cmds.fileDialog(mode=1, dm=('*.mdd') )
	if mode ==3:
		filePath = cmds.fileDialog(mode=1, dm=('*.geo') )		
	filePath = pathToWindows(filePath)
	cmds.textFieldButtonGrp('em_fileName',e=1, text=filePath)
	return filePath

def pathToWindows(path):
	"""
	Convert path separators and drive letters to windows only if the os
	is windows.
	"""
	if os.name == "nt":
		converted = re.sub(r"[\\/]+", r"\\", path)
		converted = re.sub(r"^/n", r"N:", converted)
	else:
		converted = path
	return converted

def getDirFromParh (path):
	basename = os.path.basename(path)  
	split = basename.split(".")
	difName = os.path.dirname(path)  
	return (difName,split[0])

# Mode is 1- obj, 2-mdd, 3 - particles to geo
def onRadioBtnChanged():
	mode  = cmds.radioButtonGrp( 'em_modeRadio',q=1, select=1)	
	if mode ==1:
		cmds.textFieldButtonGrp('em_fileName', e=1,text='c:/temp/foo.#.obj')
	if mode ==2:
		cmds.textFieldButtonGrp('em_fileName', e=1,text='c:/temp/foo.mdd')
	if mode ==3:
		cmds.textFieldButtonGrp('em_fileName', e=1,text='c:/temp/foo.#.geo')
def  helpWindow(*args):
	helpWindow = 'helpExporter_window'
	if cmds.window(helpWindow, exists=1):
		cmds.deleteUI( helpWindow , window=True )
	if cmds.windowPref(helpWindow, exists=1):
		cmds.windowPref( helpWindow, remove=True )
	helpWindow = cmds.window(helpWindow,title="Exporter help",  s=1, widthHeight=(700, 400) )
	layout  = cmds.columnLayout( adjustableColumn=1 )
	text = "This tools exports  animated or static polygonal geometry and Particles to houdini.\n     For geometry it uses OBJ or MDD format\n     For particles --> Houdini's ascii GEO format.\n\nOBJ EXPORT: \n    1. Select single or multiple meshes in maya\n    2.Set frame range, increment, choose OBJ in choice selector, specify path for export similar to Example.\n    3. Click \"Export\".\n\nMDD EXPORT: \n    1. Select single or multiple meshes in maya\n    2.Set frame range,  choose MDD in choice selector, specify path for export similar to Example.\n    3. Click \"Export\"\nNote that increment doesn't work .\n\nPARTICLE EXPORT:\n    1. Select your particles \n    2.Set frame range, increment, choose \"Particle\" in choice selector, specify path for export similar to Example.\n    3. Expand   \"Particle Custom Variable\" rollout and  here you can specifiy two custom vector PP variables and two float as well(or leave them blank). \n    to do it just input their names like they appear in expression editor without particleShape name.EXAMPLE: \"myCustomVecPP\"\n    4. Click \"Export\"\nNote that increment doesn't work  for particle export.\n\n\n"
	cmds.scrollField( editable=False, parent=layout, h=300,wordWrap=True, text=text)
	cmds.showWindow( helpWindow )

	
	
def  runUI ():

	# Make a new window
	mddExporterWindow = 'mddExporter_window'
	if cmds.window(mddExporterWindow, exists=1):
		cmds.deleteUI( mddExporterWindow , window=True )
	if cmds.windowPref(mddExporterWindow, exists=1):
		cmds.windowPref( mddExporterWindow, remove=True )
	mddExporterWindow = cmds.window(mddExporterWindow,menuBar=True, title="Maya OBJ/MDD/Particle Sequence Exporter to Houdini", iconName='Short Name', s=0, widthHeight=(400, 310) )
	cmds.menu( label='Help', helpMenu=True )
	cmds.menuItem( label='Short Help' ,command = helpWindow)

	startFrame  = cmds.playbackOptions(q=1, minTime=1 )
	endFrame = cmds.playbackOptions(q=1, maxTime=1 )	
	cmds.columnLayout( adjustableColumn=True )
	cmds.text( label='*** Select Objects in the Viewport First *** ',align='center' )
	cmds.separator()
	rangeSlider = cmds.intFieldGrp('em_rangeSlider', numberOfFields=3,columnAlign =[1,'left'], label='Frame Range',columnWidth5=(82,62,62,40, 40), extraLabel='inc', value1=startFrame  , value2=endFrame, value3=1)
	cmds.separator()
	mddFpsOptionMenu = cmds.floatFieldGrp( 'em_frate',numberOfFields=1, label='Frame Rate', extraLabel='fps', value1=getMayaFrameRate(),columnWidth3=(82,40, 40) )
	cmds.separator()
	radioButtons = cmds.radioButtonGrp( 'em_modeRadio',label='Export To :  ', labelArray3=['OBJ', 'MDD', 'Particle Geo'],select = 2,adjustableColumn=1,columnAlign =[1,'left'], numberOfRadioButtons=3,changeCommand = 'fx_mdd_obj_exporter.onRadioBtnChanged()')
	cmds.separator()
	cmds.textFieldButtonGrp('em_fileName', label='FileName', text='c:/temp/foo.mdd',columnWidth3=(82,265, 40),columnAlign =[1,'left'], buttonLabel='Open' ,buttonCommand = getExportFilePathUI)
	cmds.separator()
	cmds.button( label='EXPORT', command=launchExport )

	cmds.frameLayout( label='Particles Custom Variable to Export' ,borderStyle='etchedOut',collapsable=1,collapse=1 )
	cmds.columnLayout()
	cmds.rowColumnLayout( numberOfColumns=2, columnAttach=(1, 'right', 0), columnWidth=[(1, 100), (2, 250)] )
	cmds.text( label='UserVector 1' )
	cmds.textField('userVector1')
	cmds.text( label='UserVector 2' )
	cmds.textField('userVector2')
	cmds.setParent( '..' )

	cmds.rowColumnLayout( numberOfColumns=2, columnAttach=(1, 'right', 0), columnWidth=[(1, 100), (2, 250)] )
	cmds.text( label='UserFloat 1' )
	cmds.textField('userFloat1')
	cmds.text( label='UserFloat 2' )
	cmds.textField('userFloat2')
	cmds.setParent( '..' )
	
	
	cmds.setParent( '..' )
	cmds.setParent( '..' )	
	
	
	cmds.separator()


	
	
	
	cmds.setParent( '..' )
	cmds.showWindow( mddExporterWindow )



	
if __name__=='__main__':
	runUI()
	
	

