from pymel.core import *
import os
# import maya.cmds as cmds
# from xml.dom.minidom import parse, getDOMImplementation, Document


def exportSelectedToObj():
    path = sceneName()

    if path:
        workDir = path.rsplit('/', 1)[0]
        sceneLabel = path.rsplit('/', 1)[1]
        exportPath = os.path.join(workDir, sceneLabel.rsplit('.v', 1)[0])

    if not os.path.exists(exportPath):
        os.mkdir(exportPath)
        
    print exportPath

    objects = selected()
    for n in objects:
        select(n)
        exportSelected(os.path.join(exportPath, n + ".obj"), type = "OBJexport", options = "groups=1;ptgroups=0;materials=0;smoothing=1;normals=1" )


def exportTexturesToXml(abc_file):
    #file_name = "/home/max/exported_data.xml"
    #file_name = fileDialog2(ff='*.xml', fm=0)[0]
    file_name = abc_file.replace(".abc", ".xml")
    print file_name

    xml = Document()
    xml.appendChild(xml.createElement("scene"))
    
    #if g=1, ignores exactType option
    allObjects = cmds.ls( sl=1, dag=1, lf=1, ap=1, l=1, st=0, g=1, exactType='mesh')
    print allObjects
    i=0
    nonmesh=0
    for obj in allObjects:
        objectNode = xml.createElement("object")
        object_name = xml.createElement("object_name")
        objectNode.appendChild(object_name)
        object_name.appendChild(xml.createTextNode(obj))
        
        shadingGrp = cmds.listConnections(obj, type='shadingEngine')
        if shadingGrp is None:
            nonmesh+=1
        else:
            shader = cmds.ls(cmds.listConnections(shadingGrp), mat=1)
            print shader
        
# find color map
#        if len(cmds.ls(cmds.listConnections(shader), type='file'))>0:
#            color_file_node = cmds.ls(cmds.listConnections(shader), type='file')[0]
#            texture_file_color = str(cmds.getAttr(color_file_node+'.ftn'))
#        else:
#            texture_file_color = " "

# find direct connections to shader
        if len(cmds.ls(cmds.listConnections(shader), type='file'))>0:
            connected_files = cmds.ls(cmds.listConnections(shader), type='file')
            print connected_files
            texture_file_color = None
            texture_file_spec = None
            for map in connected_files:
                connections = cmds.listConnections(map, p=True, c=False, d=True, s=False)
                print connections
                for con in connections:
                    if con == shader[0]+".color":
                        color_file_node = map
                        texture_file_color = str(cmds.getAttr(color_file_node+'.ftn'))
                        print texture_file_color
                    if con == shader[0]+".specularColor":
                        spec_file_node = map
                        texture_file_spec = str(cmds.getAttr(spec_file_node+'.ftn'))
                        print texture_file_spec
                if texture_file_color is None:
                    texture_file_color = " "
                if texture_file_spec is None:
                    texture_file_spec = " "
        else:
            texture_file_color = " "
            texture_file_spec = " "

# find bump map
        if len(cmds.ls(cmds.listConnections(shader), type='bump2d'))>0:
            bump2d_node = cmds.ls(cmds.listConnections(shader), type='bump2d')[0]
            bump_file_node = cmds.ls(cmds.listConnections(bump2d_node), type='file')[0]
            texture_file_bump = str(cmds.getAttr(bump_file_node+'.ftn'))
        else:
            texture_file_bump = " "

#        for tex in shaders[i]:
#            if cmds.ls(cmds.listConnections(shaders), type='file')[0] is not None:
                #file_node = cmds.ls(cmds.listConnections(shaders), type='file')[i]
                #texture_file = str(cmds.getAttr(file_node+'.ftn'))
#                texture_file = "test"
#            else:
#                texture_file = ""
            

        texture_color = xml.createElement("texture_color")
        objectNode.appendChild(texture_color)
        texture_color.appendChild(xml.createTextNode(texture_file_color))
        
        texture_spec = xml.createElement("texture_spec")
        objectNode.appendChild(texture_spec)
        texture_spec.appendChild(xml.createTextNode(texture_file_spec))

        texture_bump = xml.createElement("texture_bump")
        objectNode.appendChild(texture_bump)
        texture_bump.appendChild(xml.createTextNode(texture_file_bump))
#        objectNode.setAttribute("object_name", obj)
#        objectNode.setAttribute("texture", shaders[i])
        xml.firstChild.appendChild(objectNode)
        i=i+1
    f = open(file_name, 'w')
    xml.writexml(f)
    #f.write(xml.toprettyxml(indent="    "))
    f.close()
#    print xml.toprettyxml()
    print str(i) + " objects processed."
    print str(nonmesh) + " non-mesh objects exported without textures."



def exportGeoToAbc():
    import maya.mel as mel
    
    rootstring = ""
    selection = cmds.ls(sl=True)
    mel.eval('group; xform -os -piv 0 0 0; setAttr "group1.scaleZ" 0.01; setAttr "group1.scaleX" 0.01; setAttr "group1.scaleY" 0.01; makeIdentity -apply true -t 0 -r 0 -s 1 -n 0; ungroup;')
    for obj in selection:
        rootstring = rootstring + " -root |" + obj
    file_name = fileDialog2(ff='*.abc', fm=0, cap='Export geometry to .abc file')[0]
    print file_name
    print 'AbcExport -j "-fr 1 24 -uvWrite' + rootstring + ' -file ' + file_name + '"'
    mel.eval('AbcExport -j "-fr 1 24 -uvWrite' + rootstring + ' -file ' + file_name + '";')
    mel.eval('group; xform -os -piv 0 0 0; setAttr "group1.scaleZ" 100; setAttr "group1.scaleX" 100; setAttr "group1.scaleY" 100; makeIdentity -apply true -t 0 -r 0 -s 1 -n 0; ungroup;')
    return file_name

def exportAbcXml():

    file_name = exportGeoToAbc()
    exportTexturesToXml(file_name)
