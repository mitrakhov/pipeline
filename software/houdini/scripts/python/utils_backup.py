import hou
import os
import filesys
import massive_cdl as mc
reload(mc)

def _checkHip():
	hip = hou.hipFile.name()
	if os.path.exists(hip + '.info'): return True
	return False

def startRenderPyroCache():
	if not _checkHip(): return
	curNodeLs = hou.pwd()
	curParm = curNodeLs.parm("sopoutput").eval()
	pyroNode = hou.node(curNodeLs.path().rsplit('/',1)[0])
	if not curParm == "PIPECACHE":	return
	hip = hou.hipFile.name()
	name = hip.split(os.sep)[-1].split('.')[0]
	import pipe
	obj_asset = pipe.Projects().GetAssetByInfo(hip)
	path = os.path.join(obj_asset.GetDataPath(),'geo',name)
	dir_render, padd_dir, padd_int = filesys.get_next_version_dir(path)
	dir_render += os.sep + pyroNode.name()
	if not os.path.exists(dir_render): os.makedirs(dir_render)
	dir_render += os.sep + pyroNode.name() + '.$F4.bgeo'
	pyroNode.parm("file").set(dir_render)
	print dir_render

#Load CDL file
def loadCdl():
	#file_path = '/mnt/karramba/RnD/film/sequences/massive/shots/simple_crowd/fx/massive/agent/man_v02.17.cdl'
	 # Ask for the file name (and start with the default file).
	file_path = hou.ui.selectFile(start_directory = None,  pattern = '*.cdl',
		                          collapse_sequences = False,   multiple_select=False)
	
	if not file_path: return
	
	name_group = file_path.split(os.sep)[-1].split('.')[0] #  /path/to/namefile.cdl = namefile
	CDL = mc.MassiveCDL()
	CDL.open(file_path)
	
	nodeGroup = hou.node("/obj/"+name_group)
	
	if not nodeGroup:
		nodeGroup = hou.node("/obj").createNode("subnet",name_group)
		nodeGroup.moveToGoodPosition()
	child_nodes = []
	shaders = {}
	#Create materials
	
	filtered_variables = []
	vkeys = CDL.variables.keys() # In addition it needs variable keys to search ones in string values and put it into variable class tag
	
	shopNode = nodeGroup.node("materials")
	if not shopNode:
		shopNode = nodeGroup.createNode("shopnet","materials")
		shopNode.moveToGoodPosition()
	
	for key in CDL.materials.keys():
		materialName =key.split(' ',1)[-1] 
		name = materialName.replace(" ", "_")
		id = str(CDL.materials[key]['id']).split("id ")[-1]
		
		surfaceNode = shopNode.node(name)
		
		if not surfaceNode:
			surfaceNode = shopNode.createNode("d_warunit",name)
			surfaceNode.moveToGoodPosition()
		ff = [x for x in surfaceNode.parmTuples() if x.name()[-3:] == 'Var']
		map(lambda x: x.set(("",)), ff)
		if 'shader' in CDL.materials[key].keys():
			#print 'option "shader" not found in material statement: ', CDL.materials[key]
			overrades = CDL.materials[key]['shader'].overrades
			parms = map(lambda x: x.name(), surfaceNode.parmTuples())
			for pkey in overrades.keys():
				_type, _name = pkey.split(" ")
				if not _name in parms: continue
				# Clean up values and assemble ones 
				values = map(lambda x: x.replace('"',''), overrades[pkey].split(" "))
				# Find value like this /mnt/karramba/RnD/film/sequences/massive/assets/textures/man02/man_02_color_0'colormap'.tdl
				if _type == 'string':
					vkey = [x for x in vkeys if str("'"+x+"'") in values[0]]
					if vkey:
						# Find VAR attribute: if _name == 'colorMap' it needs attribute named 'colorMapVar'
						try:
							surfaceNode.parm(_name + 'Var').set(vkey[0])
							filtered_variables.append(vkey[0])
							values[0] = values[0].replace("'" + vkey[0] + "'", "1")
						except:
							print _name, values
							raise Exception("Suitable attribute not found! Expected " + _name + 'Var')
				if not values: continue
				if _name[-3:] == 'Var': continue
				if _name == 'label': continue
				try:
					surfaceNode.parmTuple(_name).set(values)
				except:
					print _name, values
		
		p = surfaceNode.parm('label')
		if not p:
			pt = hou.StringParmTemplate('label','Label',1)
			surfaceNode.addSpareParmTuple(pt)	
			p = surfaceNode.parm('label')
			p.set(materialName)
			p.lock(1)
		
		p = surfaceNode.parmTuple("ogl_numtex")
		p.set((1,))
		
		#t = p.parmTemplate()
		#s = t.parmTemplates()[0] #
		#findparm = s.name().replace('#',1)
		#c = surfaceNode.parmTuple(findparm)
		#c.setExpression('chs("colorMap")')
		p = surfaceNode.parm("cdlFile")
		if not p:
			pt = hou.StringParmTemplate('cdlFile','cdlFile',1)
			surfaceNode.addSpareParmTuple(pt)
			p = surfaceNode.parm("cdlFile")
			p.set(file_path)
			p.lock(1)
		shaders[id] = surfaceNode
		child_nodes.append(surfaceNode)
		
	#Create variables node
	p = shopNode.parmTuple("variables")
	if not p:
		ps = hou.StringParmTemplate('name','Name',1)
		pf = hou.FloatParmTemplate('default','Default',1,(0,),0.0,100)
		pn = hou.FloatParmTemplate('min','Min',1,(0,),0.0,100)
		pm = hou.FloatParmTemplate('max','Max',1,(0,),0.0,100)
		p = hou.FolderParmTemplate('variables','Variables', parm_templates=(ps,pf,pn,pm,), folder_type=hou.folderType.MultiparmBlock)
		shopNode.addSpareParmTuple(p)
	
	p = shopNode.parmTuple("variables")
	filtered_variables = list(set(filtered_variables))
	keys_len = len(filtered_variables)
	p.set((keys_len,))

	for i, key in zip(xrange(1,keys_len+1), filtered_variables):
		v = CDL.variables[key]
		p = shopNode.parm('default%s'%i)
		p.lock(0)
		p.set(v.getDefault())
		p.lock(1)
		p = shopNode.parm('min%s'%i)
		p.lock(0)
		p.set(v.getMin())
		p.lock(1)
		p = shopNode.parm('max%s'%i)
		p.lock(0)
		p.set(v.getMax())
		p.lock(1)
		p = shopNode.parm('name%s'%i)
		p.lock(0)
		p.set(key)
		p.lock(1)
		
	#Create layout
	nb = shopNode.findNetworkBox(name_group)
	if not nb:
		nb = shopNode.createNetworkBox(name_group)
		shopNode.layoutChildren(child_nodes)
		map(lambda x: nb.addNode(x), child_nodes)
		nb.fitAroundContents()
		
	nodeGroupPath = nodeGroup.path()
	#Create geometries
	for key in CDL.geometries.keys():
		name = key.split(' ',1)[-1].replace(" ", "_")
		nodeGeo = hou.node(nodeGroupPath + "/"+ name)
		if not nodeGeo:
			nodeGeo = nodeGroup.createNode("geo",name)
			nodeGeo.moveToGoodPosition()
			pt = hou.StringParmTemplate('label','Label',1)
			nodeGeo.addSpareParmTuple(pt)
		p = nodeGeo.parm('label')
		p.lock(0)
		p.set(key.replace('geometry ',''))
		p.lock(1)
		nodeFile = hou.node(nodeGeo.path() + '/file1')
		if 'file' in CDL.geometries[key].keys():
			file_path = CDL.geometries[key]['file']
			nodeFile.parm("file").set(str(file_path).split("file ")[-1])
			nodeFile.setDisplayFlag(1)
			nodeFile.setRenderFlag(0)
			nodeMaterial = nodeGeo.createNode("texture",'m1')
			nodeMaterial.moveToGoodPosition()
			nodeMaterial.parm('sv').set(-1)
			nodeMaterial.parm('offsetv').set(1)
			nodeMaterial.parm('type').set(5)
			nodeMaterial.setDisplayFlag(0)
			nodeMaterial.setRenderFlag(1)
			nodeMaterial.setFirstInput(nodeFile)
			# Connect geo -> shader 
		if not 'material' in CDL.geometries[key].keys():
			print 'option "material" not found in geometry statement: ', CDL.geometries[key]
			continue
		id_material = str(CDL.geometries[key]['material']).split("material ")[-1]
		nodeGeo.parm('shop_materialpath').set(shaders[id_material].path())
	
	#Create clothes
	for key in CDL.clothes.keys():
		name = key.split(' ',1)[-1].replace(" ", "_")
		nodeGeo = hou.node(nodeGroupPath + "/"+ name)
		if not nodeGeo:
			nodeGeo = nodeGroup.createNode("geo",name)
			nodeGeo.moveToGoodPosition()
			pt = hou.StringParmTemplate('label','Label',1)
			nodeGeo.addSpareParmTuple(pt)
		p = nodeGeo.parm('label')
		p.lock(0)
		p.set(key.replace('cloth ',''))
		p.lock(1)
		nodeFile = hou.node(nodeGeo.path() + '/file1')
		if 'geo' in CDL.clothes[key].keys():
			file_path = CDL.clothes[key]['geo']
			nodeFile.parm("file").set(str(file_path).split("geo ")[-1])
		# Connect geo -> shader
		if not 'material' in CDL.clothes[key].keys():
			print 'option "material" not found in cloth statement: ', CDL.clothes[key]
			continue
		id_material = str(CDL.clothes[key]['material']).split("material ")[-1]
		nodeGeo.parm('shop_materialpath').set(shaders[id_material].path())
	
	nodeGroup.layoutChildren()

# Update massive CDL file
# Usage preRenderUpdateCdl('/obj/man_v02',...)
def preRenderUpdateCdl(*args):
	for x in args:
		agentNode = hou.node(x)
		agentMaterialNode = agentNode.node('materials')
		for n in agentMaterialNode.children():
			_updateCdl(agentMaterialNode,n)
	pass

#Update massive CDL file
def updateCdl():
	cdl_parm_name = 'cdlFile'
	nodes=hou.selectedNodes()
	if not nodes: raise Exception('It needs selected shop node. Please select node and try again')
	
	for n in nodes:
		nv = hou.node('/shop/__VARIABLES__')
		if not nv: raise Exception('Node __VARIABLES__ not found')
		_updateCdl(nv,n)

def _updateCdl(varnode,n):
	
	if not n.type().name() == 'd_warunit':
		print n.name(), ' is not type of d_warunit' 
		return
	
	cdl_parm_name = 'cdlFile'

	parms = n.parmTuples()
	p = n.parm('label')
	name_cdl_material = p.eval()
	
	#Check for existing CDL param
	names = map(lambda x: x.name(), parms)
	if not cdl_parm_name:
		print n, 'has not "'+cdl_parm_name+ "' parameter. Skipping ...", 
		return
	file_path = n.parm(cdl_parm_name).eval()
	if not os.path.exists(file_path):
		print 'File not found: ', file_path , " . Skipping ..."
		return
	
	#Get (name, type, value) tuple 
	filtered_params = filter(lambda x: not x.name() ==  cdl_parm_name, parms)
	params = []
	for p in filtered_params:
		p_name = p.name()
		if p_name[-3:] == 'Var': continue # Skip if param like 'colorMapVar'
		p_value = None 
		p_type = None
		
		parmTemplate = p.parmTemplate()
		
		toggleRm = False
		
		try: # because of such param as parmTemplateType.FolderSet has not func defaultValue()
			val = p.eval()
			defval = parmTemplate.defaultValue()
			if p.eval() ==  parmTemplate.defaultValue():	toggleRm = True 
			if parmTemplate.type().name() == 'Toggle':
				if bool(p.eval()[0]) == defval: toggleRm = True
		except:
			print "param has not func defaultValue()"
		parmLook = parmTemplate.look()
		paramType = parmTemplate.type()
		if not 'tags' in dir(parmTemplate): continue
		paramRiType = parmTemplate.tags()
		
		if 'script_ritype' in paramRiType.keys():
			p_type = paramRiType['script_ritype'].split(' ')[-1]
			if p_type == "string":
				p_value = '"%s"'%p.eval()[0] 
			elif p_type == "float":
				p_value = p.eval()[0]
			elif p_type == "int":
				p_value = p.eval()[0]
			elif p_type == "color":	
				p_value = ' '.join([str(x) for x in p.eval()])
			elif p_type == "vector":	
				p_value = ' '.join([str(x) for x in p.eval()])
		else:
			continue
			
		if not p_type:
			"Not supported type param: ", parmTemplate, ' for ', p_name
			continue

		params.append((p_name, p_type, p_value, toggleRm))
		
	CDL = mc.MassiveCDL()
	CDL.open(file_path)
	
	if not 'material '+name_cdl_material in CDL.materials.keys():
		print 'The material name "%s" among "%s" not found in %s file'%(name_cdl_material,' '.join([x.split(" ")[1] for x in CDL.materials.keys()]),file_path)
		return

	for p_name, p_type, p_value, rmval  in params:
		#Override colorMap parameter
		if p_value == '' or p_value == None: continue
		if p_type == 'string':
			try:
				p = n.parm(p_name + 'Var')
				if p:
					v = p.eval()
					if v:
						p_value_body, p_value_ext  = p_value.split('.')
						p_value =  p_value_body[:-1] + "'"+v+"'." + p_value_ext
			except e:
				print p_name, str(e) 
				raise Exception('Error! ')
		key = '%s %s'%(p_type,p_name)
		if rmval:
			if key in CDL.materials['material '+name_cdl_material]['shader'].overrades.keys(): 
				del CDL.materials['material '+name_cdl_material]['shader'].overrades[key]
		else: 
			CDL.materials['material '+name_cdl_material]['shader'].overrades[key] = p_value
	#cpfile = filesys.file_new_version(folder, file_name)
	CDL.save()
	print file_path
		

#Xray switcher for selected object
def switchXray():
    nodes=hou.selectedNodes()
    for n in nodes:
        isXray=hou.ObjNode.isUsingXray(n)
        if isXray:
            hou.ObjNode.useXray(n, 0)
        else:
            hou.ObjNode.useXray(n, 1)
            
            
            
#separate selected object into series of obj nodes and collapse into subnet
def separateObject():
    selectedNode=hou.selectedNodes()
    geoPath=hou.node(selectedNode[0].children()[0].path()).parm("file").eval()
    subnetName=selectedNode[0].name()
    out=hou.node(selectedNode[0].path()).createNode("group","out")
    hou.node(out.path()).parm("docreategrp").set(0)
    hou.node(out.path()).parm("destroyname").set("gGeo default")
    out.setFirstInput(selectedNode[0].children()[0])
    out.setDisplayFlag(1)
    
    out=hou.node(selectedNode[0].path()).displayNode()
    geo = out.geometry()
    objects = []
    

    for n in geo.primGroups():
	currentNode=hou.node("/obj").createNode("geo",n.name())
        objects.append(currentNode)
        currentNode.children()[0].destroy()
        fileNode=currentNode.createNode("file",n.name())
        hou.node(currentNode.children()[0].path()).parm("file").set(geoPath)
        facetNode=hou.node(currentNode.path()).createNode("facet","postcomputenormal")
        facetNode.setFirstInput(fileNode)
        hou.node(facetNode.path()).parm("postnml").set(1)
        deleteNode=hou.node(currentNode.path()).createNode("delete","isolate_"+str(currentNode))
        deleteNode.setFirstInput(facetNode)
        hou.node(deleteNode.path()).parm("group").set(str(currentNode))
        hou.node(deleteNode.path()).parm("negate").set(1)
        deleteNode.setDisplayFlag(1)
        deleteNode.setRenderFlag(1)
#        deleteNode.setHardLocked(1)
        hou.node(currentNode.path()).layoutChildren()
    
    
    selectedNode[0].destroy()
    parentObjects=objects[0].parent()
    subnet=parentObjects.collapseIntoSubnet(objects,subnetName)
    hou.node(subnet.path()).layoutChildren()
    hou.setUpdateMode(hou.updateMode.AutoUpdate)
    
    
#bake object to world    
def bakeObjectToWorld(startFrame, endFrame):
    selectedNode=hou.selectedNodes()
    selectedNodeName=selectedNode[0].name()
    parent=selectedNode[0].parent()
    bakeNode=hou.copyNodesTo(selectedNode,parent)
    bakeNode[0].setName(selectedNodeName + "_bake")
    bakeNode[0].parm("keeppos").set(0)
    fetchNode=hou.node(parent.path()).createNode("fetch","fetch_"+selectedNodeName)
    hou.node(fetchNode.path()).parm("fetchobjpath").set(selectedNode[0].path())
    hou.node(fetchNode.path()).parm("useinputoffetched").set(1)
    nullNode=hou.node(parent.path()).createNode("null")
    nullNode.setFirstInput(fetchNode)
    nullNodeName=nullNode.name()
    
    
    parms=["tx","ty","tz","rx","ry","rz"]
    constant=["TX","TY","TZ","RX","RY","RZ"]
    
    
    bakeNode[0].setInput(0,None)
    
    #delete expresssion in parms and set to 0
    for p in parms:
      bakeNode[0].parm(p).deleteAllKeyframes()
      hou.hscript('objextractpretransform '+ bakeNode[0].path())
      bakeNode[0].parm(p).set(0)
    
    
    
    for p, c in zip(parms, constant):
        #bakeNode[0].parm(p).deleteAllKeyframes()
        hou.node(bakeNode[0].path()).parm(p).setExpression('origin("","../'+nullNodeName+'",'+c+')')
    
    
    
    #add dict for hou.Keyframe and values    
    key = dict([(x, hou.Keyframe()) for x in parms])
    values = dict([(x, []) for x in constant])
          
    #bake time range
    timeRange = xrange(startFrame,endFrame+1)
    
    
    #fill values dict
    for t in timeRange:
        hou.setFrame(t)
        for v, p in zip(constant,parms):
	    values[v].append(bakeNode[0].parm(p).eval())
	    
    
    for p in parms:
      bakeNode[0].parm(p).deleteAllKeyframes()
      bakeNode[0].parm(p).set(0)
    
    #set key by keyframes
    
    for t in timeRange:
	hou.setFrame(t)
	for v, p, k in zip(constant,parms,key):
	  key[k].setValue(values[v][t-startFrame])
	  bakeNode[0].parm(p).setKeyframe(key[k])
    
    fetchNode.destroy()
    nullNode.destroy()
    
    
    
#bake transform animation to external chan fileNode
def writeChop(dopImportNode, startFrame, endFrame):
        
    dopImportNode[0].parm("importstyle").set(3)
    objNode=dopImportNode[0].parent()
    computeTransformationNode=objNode.createNode("copyobjects","computetransformation")
    computeTransformationNode.parm("mode").set(1)
    computeTransformationNode.parm("computeTRS").set(1)
    computeTransformationNode.setInput(1,dopImportNode[0])
    tracksNum=len(computeTransformationNode.geometry().points())

    objNodeName=objNode.name()

    chopNet=hou.node("/ch").createNode("ch","chop_"+objNodeName)
    atributes=['translate','rotate']
    renameScope=['tx ty tz','rx ry rz']
    nodes = {}
    for n,k in zip(atributes,renameScope):
        nodes['geometryChopNode_'+n]=chopNet.createNode("geometry",objNodeName+'_'+n)
        nodes['geometryChopNode_'+n].parm("soppath").set(computeTransformationNode.path())
        nodes['geometryChopNode_'+n].parm("method").set(1)
        nodes['geometryChopNode_'+n].parm("attribscope").set(n)
        nodes['geometryChopNode_'+n].parm("renamescope").set(k)      
        nodes['geometryChopNode_'+n].parm("start").set(startFrame/hou.fps())      
        nodes['geometryChopNode_'+n].parm("end").set(endFrame/hou.fps())
    mergeChopNode=chopNet.createNode("merge")
    mergeChopNode.setFirstInput(nodes['geometryChopNode_'+atributes[0]])
    mergeChopNode.setNextInput(nodes['geometryChopNode_'+atributes[1]])

    tracks=mergeChopNode.tracks()
    tracksSort=[]
    for i in xrange(tracksNum):
        temp=[]
        for n in tracks[i::tracksNum]:
            temp.append(n)
        tracksSort.append(temp)
    
    
    for j in xrange(tracksNum):
      buffer=""
      for n in xrange(startFrame, endFrame+1):
	for m in tracksSort[j]:
	  buffer+="%s %f" % (str(n), m.evalAtFrame(n))
	buffer+="\n"
      fl = open("/home/tfx/"+objNodeName+"."+str(j)+".chan","w")
      fl.write(buffer)
      fl.close()
      del buffer
    
    computeTransformationNode.destroy()
    chopNet.destroy()


# Import textures from XML file on disk to Alembic Archive
import hou
import toolutils
import re
from xml.dom.minidom import parse, getDOMImplementation
import os.path

def lastSelectedNode():
    '''Return the last selected node, or None if there isn't one.'''
    selected_nodes = hou.selectedNodes()
    return (selected_nodes[-1] if len(selected_nodes) > 0 else None)

def importDataFromXmlToAbc():
# select Alembic archive #    
    abc = lastSelectedNode()
    if abc is None:
	hou.ui.setStatusMessage("Select one root Alembic Archive node.")
	hou.ui.displayMessage("No root Alembic Archive node has been selected. Select one.", title="Attention, monsieur!")
	return None
    if abc.type() == hou.nodeType(hou.objNodeTypeCategory(), 'alembicarchive'):
	print "Alembic Archive found"
    else:
	print "No Alembic Archive selected"

# XML stuff #
    #file_name = "/home/max/exported_data.xml"
    hou.ui.setStatusMessage("Choose XML file to import textures from.")
    file_name = hou.ui.selectFile(start_directory="/mnt/karramba/", title="Choose XML", pattern="*.xml")
    if file_name == "":
	return None
    file_name = os.path.expandvars(file_name)
    xml = parse(file_name)
    xmlobjects = xml.getElementsByTagName("object")
    
# parse and assign textures #	
    stat_assigned = 0
    stat_noshader = 0
    for obj in xmlobjects:
        object_name = obj.getElementsByTagName("object_name")[0]
        object_path = object_name.childNodes[0].data
        print object_path
	object_path = object_path.replace('|', '/')
	print object_path
        object_fullpath = abc.path() + object_path
        print object_fullpath
	
	object_texture_color = obj.getElementsByTagName("texture_color")[0]
	texture_path_color = object_texture_color.childNodes[0].data
	
	object_texture_spec = obj.getElementsByTagName("texture_spec")[0]
	texture_path_spec = object_texture_spec.childNodes[0].data
	
	object_texture_bump = obj.getElementsByTagName("texture_bump")[0]
	texture_path_bump = object_texture_bump.childNodes[0].data

        if hou.parm(str(object_fullpath) + "/shop_materialpath") is not None:
	    object_shader = hou.parm(str(object_fullpath) + "/shop_materialpath").evalAsString()
	    #object_shader = hou.node(str(object_fullpath)).evalParm("shop_materialpath")
	    if hou.node(object_shader) is not None:
		hou.node(object_shader).parm("baseColorMap").set(str(texture_path_color))
#		if hou.node(object_shader).parm("baseSpecMap") is not None:
#		    hou.node(object_shader).parm("baseSpecMap").set(str(texture_path_color))
#		else:
#		    continue
#		if hou.node(object_shader).parm("baseDispMap") is not None:
#		    hou.node(object_shader).parm("baseDispMap").set(str(texture_path_bump))
#		else:
#		    continue
		stat_assigned = stat_assigned + 1
	    else:
		print object_fullpath + ": No shader found. Could not assign the texture."
		stat_noshader = stat_noshader + 1
	else:
	    #print "Could not find assigned shader on " + object_fullpath
	    continue

    print str(stat_assigned) + " textures assigned successfully."
    print str(stat_noshader) + " destination shaders not found."