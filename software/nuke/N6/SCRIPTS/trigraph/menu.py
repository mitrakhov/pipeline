# Copyright 2010 by Serge Zaporozhtsev.
# TRIMenu nuke script v1.2
# -*- coding: utf-8 -*-
#

import nuke
import xml.etree.ElementTree as etree
import os.path
import posixpath
import re
    

def nukenormpath(path):
    p = posixpath.normpath(path)
    p = p.replace("\\", "/")
    return p

def tri_path_check(nodes, top=True):
    PATH = tri_path()
    LDIR = "/usr/pipeline/software/nuke/N6/SCRIPTS/trigraph"
    PENV = "[python tri_path()]"
    report = ""
    for n in nodes:
        if n.Class() == "Group":
            report += tri_path_check(n.nodes(), False)
        if 'file' in n.knobs():
            if n['file'].value().startswith(PATH) or \
               n['file'].value().startswith(LDIR) or \
               n['file'].value().startswith(PENV):
                report += " OK node: " + n.fullName() + " (..." + n['file'].value()[-30:] + ")\n"
            else:
                report += "BAD node: " + n.fullName() + " (..." + n['file'].value()[-30:] + ")\n"
    if top:
        nuke.tprint("REPORT")
        nuke.tprint(report)
        nuke.message("REPORT \n" + report)
        return None
    else:
        return rep

def tri_path():
    if 'tri_project_id' in nuke.root().knobs():
        if nuke.root()['tri_project_local_flag'].value():
            return nuke.root()['tri_project_local_path'].value()
        else:
            return nuke.root()['tri_project_path'].value()
    else:
        return ""

def tri_env2path(nodes):
    for n in nodes:
        nuke.tprint(">>", n.name(), n.Class())
        if 'triwrite_gizmo' in n.knobs():
            tri_env2path([n.node('result'), n.node('dailies')])
        else:
            if 'file' in n.knobs():
                p = n['file'].value()
                nuke.tprint("<<", "[python tri_path()]", p)
                p = p.replace("[python tri_path()]", tri_path())
                n['file'].setValue(p)

def tri_path2env(nodes):
    templ = tri_path()
    for n in nodes:
        nuke.tprint(">>", n.name(), n.Class())
        if 'triwrite_gizmo' in n.knobs():
            tri_path2env([n.node('result'), n.node('dailies')])
        else:
            if 'file' in n.knobs():
                p = n['file'].value()
                nuke.tprint(">>", p, templ)
                p = p.replace(templ, "[python tri_path()]")
                n['file'].setValue(p)


def tri_project_init():
    nuke.tprint("*START project setup")
    
    # add new Write menu shortcut
    nuke.menu('Nodes').findItem('Image').addCommand("TriWrite", "nuke.createNode(\"TriWrite\")", "", icon="Write.png")
    
    if os.getenv('TRI_PROJECT_PATH') is None or os.getenv('TRI_PROJECT_ID') is None:
        nuke.tprint(" NO project env")
        return
#    else:
#        nuke.tprint(" INIT", os.getenv('TRI_PROJECT_PATH'))
    
    if 'tri_project_id' in nuke.root().knobs():
        tri_update_setup()
    else:
        tri_new_setup()


def tri_update_setup():
    nuke.tprint(" UPDATE project setup")
    root = nuke.root()
    
    path = tri_path() + "/" + root['tri_comp'].value()                  # TRI_PATH + _cmp
    
    if 'tri_project_scene_id' in nuke.root().knobs():
        # create write dis
        pData = etree.fromstring(root['tri_project_xml_formats'].value())
        tri_create_write_path(pData.find('result'))
        tri_create_write_path(pData.find('dailies'))
        
        # add new Write menu shortcut
        nuke.menu('Nodes').findItem('Image').addCommand("TriWrite", "nuke.createNode(\"TriWrite\")", "w", icon="Write.png")
    
    # create cmp dirs
    try:
        if not os.path.exists(path):
            if nuke.ask("Dir: " + path + " not exists. Create?"):
                pass
                os.makedirs(path)
    except:
        nuke.message("Cannot create\n" + path)


def tri_new_setup():
    nuke.tprint(" NEW project setup")
    
    projectId = os.getenv('TRI_PROJECT_ID')
    projectPath = os.getenv('TRI_PROJECT_PATH')
    projectLocalPath = os.getenv('TRI_PROJECT_LOCAL_PATH', "~")
    projectLocalFlag = os.getenv('TRI_PROJECT_LOCAL_FLAG', "0")
    
    path = projectLocalPath if projectLocalFlag == "1" else projectPath
    path = path + "/" + projectId + ".xml"
    
    try:
        if not os.path.exists(path):
            nuke.message("Path not found\n" + path)
            return
        projectPath = os.path.normpath(path)
        pData = etree.parse(path)
    except:
        nuke.message("Incorrect project setup\n" + path)
        nuke.tprint(" NEW incorrect project setup\n" + path)
        return
    
    root = nuke.root()
    if projectId != pData.getroot().get("id"):
        nuke.message("Incorrect project ID: " + projectId)
        nuke.tprint(" NEW incorrect project ID" + projectId)
        return
    
    root.addKnob(nuke.Tab_Knob('tri_panel', 'TRIGRAPH'))
    root.addKnob(nuke.String_Knob('tri_project_id', 'Project ID', pData.getroot().get("id")))
    root.addKnob(nuke.Boolean_Knob('tri_project_stereo', 'Stereo3D', False))
    root.addKnob(nuke.String_Knob('tri_project_artist', 'Artist', artistName()))
    root['tri_project_stereo'].clearFlag(nuke.STARTLINE)
    root.addKnob(nuke.String_Knob('tri_project_name', 'Project Name', pData.findtext("fullname", "")))
    root.addKnob(nuke.String_Knob('tri_project_path', 'Project Path', nukenormpath(pData.findtext("path", ""))))
    root.addKnob(nuke.String_Knob('tri_project_local_path', 'Local Path', nukenormpath(projectLocalPath)))
    root.addKnob(nuke.Boolean_Knob('tri_project_local_flag', 'work locally', True if projectLocalFlag == "1" else False))
    root.addKnob(nuke.String_Knob('tri_comp', 'comps', "_cmp/" + root['tri_project_id'].value()))
    root.addKnob(nuke.String_Knob('tri_result', 'result', "_res/" + root['tri_project_id'].value()))
    root['tri_result'].clearFlag(nuke.STARTLINE)
    root.addKnob(nuke.String_Knob('tri_dailies', 'dailies', "_dailies/_TODAY"))
    root['tri_dailies'].clearFlag(nuke.STARTLINE)
    
    formats = pData.find("formats")
    output_xml = ''.join([line.strip() for line in etree.tostring(formats).splitlines()])
    root.addKnob(nuke.String_Knob('tri_project_xml_formats', '', output_xml))
    root['tri_project_xml_formats'].setVisible(False)
    root['fps'].setValue([formats.findtext("fps")])
    
    # add new Result and Dailies formats
    size = formats.find("result").find("size")
    nuke.addFormat(size.get('width') + " " + size.get('height') + " " + size.get('aspect') + projectId + " RESULT")
    size = formats.find("dailies").find("size")
    nuke.addFormat(size.get('width') + " " + size.get('height') + " " + size.get('aspect') + projectId + " DAILIES")
    root['format'].setValue(projectId + " RESULT")
    
    # setup stereo flag
    if formats.findtext("stereo") == "true":
        if nuke.ask("Init for stereo view?") is True:
            root['setlr'].execute()
            root['tri_project_stereo'].setValue(True)
    
    # setup additional luts
    #S-Log LUT
    #root['luts'].addCurve("S-Log1", "{pow(10.0, ((t - 0.616596 - 0.03) /0.432699)) - 0.037584}")
    #root['luts'].addCurve("S-Log2", "{pow(10.0,  (x - 0.615971) * 2.698893) - 0.037584}")
    
    # setup project Scene Id and Shot #
    pSceneId = ""
    pShotNumber = ""
    p = nuke.Panel("PROJECT " + root['tri_project_id'].value())
    p.addSingleLineInput("SCENE ID", pSceneId)
    p.addSingleLineInput("SHOT #", pShotNumber)
    p.addButton("Cancel")
    p.addButton("OK")
    if p.show() == 1:
        pSceneId = p.value("SCENE ID").upper()
        pShotNumber = p.value("SHOT #")
        
        scene_name = root['tri_project_id'].value() + "-" + pSceneId           # GP-AZA
        shot_name = pSceneId + "-" + pShotNumber                               #    AZA-010
        root.addKnob(nuke.String_Knob('tri_project_scene_id', 'Scene ID', pSceneId))
        root.addKnob(nuke.String_Knob('tri_project_shot_num', 'Shot #', pShotNumber))
        root['tri_project_shot_num'].clearFlag(nuke.STARTLINE)
        root['tri_comp'].setValue("_cmp/" + scene_name + "/" + shot_name)      # _cmp/GP-AZA/AZA-010
        root['tri_result'].setValue("_res/" + scene_name  + "/" + shot_name)   # _res/GP-AZA/AZA-010
        
        #-- setup scripts name
        mainpath = tri_path() + "/" + root['tri_comp'].value()                 # TRI_PATH + _cmp/GP-AZA/AZA-010
        name = root['tri_project_id'].value() + "-" + shot_name + "_v01.nk"    # GP-AZA-010 + _v01.nk
        
        root['name'].setValue(nukenormpath(mainpath + "/" + name))             # TRI_PATH/_cmp/GP-AZA/AZA-010 + / + GP-AZA-010_v01.nk
        
        # add new Write menu shortcut
        nuke.menu('Nodes').findItem('Image').addCommand("TriWrite", "nuke.createNode(\"TriWrite\")", "w", icon="Write.png")
    
    # add path utilities
    nuke.tcl('addUserKnob {26 "" +STARTLINE}')
    root.addKnob(nuke.PyScript_Knob('tri_env2path', " expand filenames "))
    root['tri_env2path'].setValue("nodes = nuke.selectedNodes()\nif len(nodes) > 0:\n  tri_env2path(nodes)\nelse:\n  nodes = nuke.allNodes()\n  tri_env2path(nodes)\n")
    root['tri_env2path'].setFlag(nuke.STARTLINE)
    root.addKnob(nuke.PyScript_Knob('tri_path2env', " collapse filenames "))
    root['tri_path2env'].setValue("nodes = nuke.selectedNodes()\nif len(nodes) > 0:\n  tri_path2env(nodes)\nelse:\n  nodes = nuke.allNodes()\n  tri_path2env(nodes)\n")
    root.addKnob(nuke.PyScript_Knob('tri_path_check', " check filenames "))
    root['tri_path_check'].setValue("nodes = nuke.selectedNodes()\nif len(nodes) > 0:\n  tri_path_check(nodes)\nelse:\n  nodes = nuke.allNodes()\n  tri_path_check(nodes)\n")
    nuke.tcl('addUserKnob {26 "" +STARTLINE}')
    
    path = tri_path() + "/" + root['tri_comp'].value()                         # TRI_PATH + / + _cmp/GP-AZA/AZA-010
    
    try:
        if not os.path.exists(path):
            if nuke.ask("Dir: " + path + " not exists. Create?"):
                pass
                os.makedirs(path)
    except:
        nuke.message("Cannot create\n" + path)
    
    pData = None


def tri_writeGizmo_init():
    nuke.tprint("  START TriWrite")
    if not 'triwrite_gizmo' in nuke.thisNode().knobs():
        return
    
    nuke.thisNode()['artist'].setValue(artistName())

    if nuke.thisNode()['notes'].value() == "":
        nuke.thisNode()['notes'].setValue(sceneComment())
    
    if not 'tri_project_xml_formats' in nuke.root().knobs():
        return
    
    nuke.tprint("  INIT ", nuke.thisNode().name(), nuke.thisNode().Class())
    
    root = nuke.root()
    pData = etree.fromstring(root['tri_project_xml_formats'].value())
    nuke.thisNode()['_dailies_format'].setValue(root['tri_project_id'].value() + " DAILIES")
    
    if 'tri_project_scene_id' in root.knobs():
        # create write dis
        tri_create_write_path(pData.find('result'))
        tri_create_write_path(pData.find('dailies'))
        # setup results/dailies params
        tri_filename_init(nuke.thisGroup().node('result'), pData.find('result'))
        tri_filename_init(nuke.thisGroup().node('dailies'), pData.find('dailies'))
        
        nuke.thisGroup()['_render'].setEnabled(True)
        nuke.thisGroup()['write_result'].setEnabled(True)
        nuke.thisGroup()['write_dailies'].setEnabled(True)
        nuke.thisGroup()['slate'].setEnabled(True)
    
    if nuke.thisGroup().inputs > 0:
        nuke.autoplace(nuke.thisGroup())
    
    pData = None

def tri_create_write_path(fileData):
    root = nuke.root()
    resolution = fileData.find('size').get('width') + "x" + fileData.find('size').get('height')
    
    path = tri_path() + "/" + root['tri_' + fileData.tag].value()
    if fileData.tag == "result":
        path = path + "/" + resolution
    
    try:
        if not os.path.exists(path):
            if nuke.ask("Dir: " + path + "/ not exists. Create?"):
                pass
                os.makedirs(path)
    except:
        nuke.message("Cannot create PROJ_PATH/" + root['tri_' + fileData.tag].value() + "/" \
            + root['tri_project_scene_id'].value() + "/" + resolution)

def tri_filename_init(writeNode, fileData):
    root = nuke.root()
    (pName, pExt) = os.path.splitext(os.path.basename(root['name'].value()))
    
    filename = pName + fileData.find('file').get('numbers') + fileData.find('file').get('file_type')
    filename = nukenormpath(filename)
    resolution = fileData.find('size').get('width') + "x" + fileData.find('size').get('height')
        
    writeNode['file'].setValue("[python tri_path()]/" + root['tri_' + fileData.tag].value() + "/" \
        + root['tri_project_scene_id'].value() + "/" + resolution + "/" + filename)
    
    writeNode['file_type'].setValue(fileData.find('file').get('file_type'))
    for (key, value) in fileData.find('file').items():
        if key in ["datatype", "colorspace", "compression", "quality"]:
            #nuke.tprint("dailies ==", key, value)
            if key in writeNode.knobs():
                writeNode[key].setValue(value)
    
    nukeSettings = fileData.find('file').findall('nuke')
    if nukeSettings <> None:
        for param in nukeSettings:
            writeNode[param.get('id')].setValue(param.text)

def tri_writeGizmo_update():
    root = nuke.root()
    if 'tri_project_scene_id' not in root.knobs():
        return
    if 'tri_project_xml_formats' not in root.knobs():
        return
    
    (pName, pExt) = os.path.splitext(os.path.basename(root['name'].value()))
    
    pData = etree.fromstring(root['tri_project_xml_formats'].value())
    for group in nuke.allNodes("Group", nuke.root()):
        if 'triwrite_gizmo' not in group.knobs():
            continue
        resultNode = group.node('result')
        dailiesNode = group.node('dailies')
        
        #--- update results params
        
        filename = pName + pData.find('result').find('file').get('numbers') + pData.find('result').find('file').get('file_type')
        filename = nukenormpath(filename)
        oldfilename = os.path.basename(resultNode['file'].value())
        resultNode['file'].setValue(resultNode['file'].value().replace(oldfilename, filename))
        
        #--- update dailies params
        
        filename = pName + pData.find('dailies').find('file').get('numbers') + pData.find('dailies').find('file').get('file_type')
        filename = nukenormpath(filename)
        oldfilename = os.path.basename(dailiesNode['file'].value())
        dailiesNode['file'].setValue(dailiesNode['file'].value().replace(oldfilename, filename))
    
    pData = None


nuke.addOnUserCreate(tri_project_init, nodeClass="Root")
nuke.addOnUserCreate(tri_writeGizmo_init, nodeClass="Group")
nuke.addOnScriptSave(tri_writeGizmo_update, nodeClass="Root")
nuke.addOnScriptLoad(tri_project_init, nodeClass="Root")
