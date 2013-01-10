import hou
import toolutils
import doptoolutils



def updateSourcesButton():
    import hou
    resize=hou.node("/obj/fluid_resize_container").evalParm("source_folder")
    merge_source = hou.node("/obj/fluid_resize_container/merge_source")

    # Delete multuparm parameters inside of the network and create them again
    merge_source.setParmExpressions({"numobj": ""})
    merge_source.setParmExpressions({"numobj": "ch(\"../source_folder\")"})

    # Set references for multiparm parameters 
    for n in range(1,resize+1):
        merge_source.setParmExpressions({"enable"+str(n): "ch(\"../source_activation"+str(n)+"\")"})
        merge_source.parm("objpath"+str(n)).set("`chsop(\"../objpath"+str(n)+"\")`")
        merge_source.parm("group"+str(n)).set("`chs(\"../group"+str(n)+"\")`")



def resizeFluidToMatchSops(fluidnode, matchobject):
    """ Resizes the fluid dynamic object fluidobject according
        to match object.
    """
    dopnet = doptoolutils.getCurrentDopNetwork()
    movenodes = []

    fluidtype = doptoolutils.nodeFluidType(fluidnode)
    solvernode = doptoolutils.nodeFluidSolverNode(fluidnode)
    merge = doptoolutils.findOrCreateNamedMerge(solvernode, 'post')
    resize = toolutils.findInputNodeOfType(merge, "gasresizefluid")
    if resize is None:
        resize = dopnet.createNode("gasresizefluid", "resizefluid")
        movenodes.append(resize)
        merge.setNextInput(resize)

        # Have resize link to the original smoke object to 
        # make it more straightforward to delete.
        for channame in [ "tx", "ty", "tz", "sizex", "sizey", "sizez" ]:
            resize.parm(channame).set(fluidnode.parm(channame))

    # Instrument our resize..
    if fluidtype.startswith('upres'):
        fluidtype = fluidtype[len('upres'):]

    if fluidtype == 'pyro':
        fluidtype = 'smoke'
    
    # Set gasresizefluid parameters
    resize.parm("fluidtype").set(fluidtype)
    resize.parm("refobject").set("")
    resize.parm("reffield").set("")
    resize.parm("refobjpath").set(matchobject.path()+"/OUT")
    
    toolutils.moveNodesToGoodPosition(movenodes)

    return resize


        
def resizeFluidSops(kwargs):
    
    """ Select fluid and set it up to be resizeable.
    """
    sceneviewer = toolutils.activePane(kwargs)
    if not isinstance(sceneviewer, hou.SceneViewer):
        raise hou.Error("Invalid pane type for this operation.")

    # Select the target fluid box.
    fluidobjects = sceneviewer.selectDynamics(
                        prompt="Select fluid box to resize.  Press Enter to complete.",
                        allow_multisel=False)
    if len(fluidobjects) < 1:
        raise hou.Error("No fluid container selected to set initial conditions.")
    fluidobject = fluidobjects[0]

    fluidnode = doptoolutils.getDopObjectCreator(fluidobject)
    if fluidnode is None:
        raise hou.Error("No fluid object node found.")

    """ Create and configure the reference container for resizing.
    """

    dopnet = doptoolutils.getCurrentDopNetwork()
    refobject = fluidnode.parent().parent().createNode("geo","fluid_resize_container", run_init_scripts=False)
    fluidfields = refobject.createNode("dopio","fluidfields")
    fluidfields.parm("doppath").set(dopnet.path())
    fluidfields.setParmExpressions({"defobj": "chs(\""+fluidnode.path()+"/object_name\")"})
    fluidfields.parm("fields").set(2)
    fluidfields.parm("fieldname1").set("density")
    fluidfields.parm("fieldname2").set("vel")
    parms = refobject.parmTemplateGroup()
    parms.hideFolder("Transform", True)
    parms.hideFolder("Material", True)
    parms.hideFolder("Render", True)
    parms.hideFolder("Misc", True)
    ref_folder = hou.FolderParmTemplate("ref_folder","Resize Container")
    ref_folder.addParmTemplate(hou.IntParmTemplate("nptsperarea", "Scatter per Area", 1, default_value=([5000]), min=1000, max=20000, help="Scatter points on simulated density to calculate bounds"))
    ref_folder.addParmTemplate(hou.FloatParmTemplate("treshold", "Density Treshold", 1, default_value=([0]), min=0, max=1, help="Delete density below this value prior to scattering points"))                            
    ref_folder.addParmTemplate(hou.SeparatorParmTemplate("sep1"))
    ref_folder.addParmTemplate(hou.LabelParmTemplate("merge_source", "Merge Sources"))
    ref_folder.addParmTemplate(hou.ButtonParmTemplate("update", "Update sources", help="Push this to update ObjectMerge node inside", tags={"script_callback": "import adddoputils; adddoputils.updateSourcesButton()", "script_callback_language": "python"}))
    ref_folder.addParmTemplate(hou.IntParmTemplate("source_activation", "All Sources Activation", 1, default_value=([1]), min=0, max=1, min_is_strict=True, max_is_strict=True, help="Activation of merging all of the listed sources and additional objects"))
    ref_folder.addParmTemplate(hou.MenuParmTemplate("xformtype", "Transform", "012", ("None", "Into This Object", "Into Specified Object"), 1))
    ref_folder.addParmTemplate(hou.StringParmTemplate("xformpath", "Transform object", 1, "", hou.parmNamingScheme.Base1, hou.stringParmType.NodeReference, disable_when=("{ xformtype != 2 }")))
    
    sources_folder=hou.FolderParmTemplate("source_folder","Sources to Merge",folder_type=hou.folderType.MultiparmBlock)
    sources_folder.addParmTemplate(hou.ToggleParmTemplate("source_activation#", "Source # Activation", default_value=True ))
    sources_folder.addParmTemplate(hou.StringParmTemplate("objpath#", "Object #", 1, "", hou.parmNamingScheme.Base1,hou.stringParmType.NodeReference))
    sources_folder.addParmTemplate(hou.StringParmTemplate("group#", "Group #", 1, "", hou.parmNamingScheme.Base1,hou.stringParmType.Regular))
    
    ref_folder.addParmTemplate(sources_folder) 
    parms.append(ref_folder)
    refobject.setParmTemplateGroup(parms)
    
    keep_density = refobject.createNode("blast","keep_density")
    keep_density.setFirstInput(fluidfields)
    keep_density.parm("group").set("@name==vel*")
    
    keep_vel = refobject.createNode("blast","keep_vel")
    keep_vel.setFirstInput(fluidfields)
    keep_vel.parm("group").set("@name==density")
    
    # VOLUME VOP clamping density field below given treshold
    density_treshold = keep_density.createOutputNode("volumevop","density_treshold")
    
    vopglobals = density_treshold.node("volumevopglobal1")
    
    treshold = density_treshold.createNode("parameter", "treshold")
    treshold.parm("parmname").set("treshold")
    treshold.parm("parmlabel").set("Treshold")
    
    compare_density = density_treshold.createNode("compare", "compare_density")
    compare_density.parm("cmp").set("gte")
    compare_density.setInput(0, vopglobals, 1)
    compare_density.setInput(1, treshold, 0)        

    twoway = compare_density.createOutputNode("twoway","switch_density")
    twoway.setInput(1, vopglobals, 1)
    
    vop_output = density_treshold.node("volumevopoutput1")
    vop_output.setFirstInput(twoway, 0)
    density_treshold.setParmExpressions({"treshold": "ch(\"../treshold\")"})
    # End of VOLUME VOP
    
    scatter = refobject.createNode("scatter","scatter")
    scatter.setFirstInput(density_treshold)
    scatter.parm("ptsperarea").set(1)
    scatter.setParmExpressions({"nptsperarea": "ch(\"../nptsperarea\")"})
    
    add_particles = scatter.createOutputNode("add","add_particles")
    add_particles.parm("addparticlesystem").set(1)
    
    # VOP SOP adding velocity field to density-based pointcloud
    add_vel = refobject.createNode("vopsop","add_vel")
    add_vel.parm("vex_numthreads").set(1)
    add_vel.setFirstInput(add_particles)
    add_vel.setInput(1, keep_vel, 0)
    
    globals = add_vel.node("global1")
    volumesamplex = add_vel.createNode("volumesample", "volumesample_x")
    volumesamplex.setInput(2, globals, 0)
    volumesamplex.parm("input_index").set(1)
    volumesamplex.parm("primnum").set(0)
    
    volumesampley = add_vel.createNode("volumesample", "volumesample_y")
    volumesampley.setInput(2, globals, 0)
    volumesampley.parm("input_index").set(1)
    volumesampley.parm("primnum").set(1)
    
    volumesamplez = add_vel.createNode("volumesample", "volumesample_z")
    volumesamplez.setInput(2, globals, 0)
    volumesamplez.parm("input_index").set(1)
    volumesamplez.parm("primnum").set(2)
       
    vel = volumesamplex.createOutputNode("floattovec", "vel")
    vel.setInput(1, volumesampley, 0)
    vel.setInput(2, volumesamplez, 0)
    
    vel_by_fps = vel.createOutputNode("divconst", "vel_by_fps")
    vel_by_fps.setParmExpressions({"divconst": "$FPS"})
    
    add_vector = globals.createOutputNode("add", "add_vector")
    add_vector.setNextInput(vel_by_fps, 0)
    
    vex_output = add_vel.node("output1")
    vex_output.setFirstInput(add_vector, 0)
    # End of VOP SOP
    
    merge1 = refobject.createNode("merge","merge1")
    merge1.setFirstInput(add_particles)
    merge1.setInput(1, add_vel, 0)
    
    bound = merge1.createOutputNode("bound", "bound")
    
    # Box to switch from after first simulation frame
    initial_box = refobject.createNode("box", "initial_box")
    initial_box.setParmExpressions({"sizex": "ch(\""+initial_box.relativePathTo(fluidnode)+"/sizex\")", "sizey": "ch(\""+initial_box.relativePathTo(fluidnode)+"/sizey\")","sizez": "ch(\""+initial_box.relativePathTo(fluidnode)+"/sizez\")"})
    initial_box.setParmExpressions({"tx": "ch(\""+initial_box.relativePathTo(fluidnode)+"/tx\")", "ty": "ch(\""+initial_box.relativePathTo(fluidnode)+"/ty\")","tz": "ch(\""+initial_box.relativePathTo(fluidnode)+"/tz\")"})
    
    initial_switch = initial_box.createOutputNode("switch", "initial_switch")
    initial_switch.setParmExpressions({"input": "$F>ch(\""+initial_switch.relativePathTo(fluidnode)+"/createframe\")", })
    initial_switch.setInput(1, bound, 0)

    # Null to switch to if merging of simulation sources is disabled
    no_active_source =  refobject.createNode("null", "no_active_source")
    
    merge_source =  refobject.createNode("object_merge", "merge_source")
    merge_source.setParmExpressions({"numobj": "ch(\"../source_folder\")", "xformtype": "ch(\"../xformtype\")"})
    merge_source.parm("xformpath").set("`chsop(\"../xformpath\")`")
    numobj = merge_source.parm("numobj").eval()
    
    source_switch = no_active_source.createOutputNode("switch", "source_switch")
    source_switch.setParmExpressions({"input": "ch(\"../source_activation\")"})
    source_switch.setInput(1, merge_source, 0)
    
    merge2 =  initial_switch.createOutputNode("merge","merge2")
    merge2.setInput(1, source_switch, 0)
    
    bound = merge2.createOutputNode("bound", "bound")
    
    unroll_edges = bound.createOutputNode("ends", "unroll_edges")
    unroll_edges.parm("closeu").set(4)
    
    out = unroll_edges.createOutputNode("null", "OUT")
    
    density_treshold.layoutChildren()
    add_vel.layoutChildren()
    refobject.layoutChildren()
    
    out.setDisplayFlag(True)
    out.setRenderFlag(True)
    
    resize = resizeFluidToMatchSops(fluidnode, refobject)
    resize.setCurrent(True, True)
    sceneviewer.enterCurrentNodeState() 

"""
    
    sel = hou.selectedNodes()
    m = sel[0]
    m.parm("objpath`{ id = #; return string(id); }`").set("0")

#    for n in range(1,numobj+1):
#        merge_source.setParmExpressions({"enable"+str(n): "ch(\"../source_activation"+str(n)+"\")"})
#        merge_source.parm("objpath"+str(n)).set("`chsop(\"../objpath"+str(n)+"\")`")
#        merge_source.parm("group"+str(n)).set("`chs(\"../group"+str(n)+"\")`")


fluid object name in expressions beeing read from asset interface for possible changes???
sources - points, not prims 

"""