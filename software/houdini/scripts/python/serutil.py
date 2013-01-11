import hou
def keyRight(path):
    for node in hou.selectedNodes():
        m=None
        m=node.parm("Master")
        if m!=None:
            if m.eval()==path: return 1
    return 0
def trAutoShow():
    if hou.node("/obj/Trajectories")!=None:
	hou.hscript("undoctrl off")	
        if len(hou.selectedNodes())>0:
            for obj in hou.node("/obj/Trajectories").children():
		#t=None
		t=obj.parm("Object_Trajectory")
		if (hou.node(t.eval()).isSelected()==1) or (keyRight(t.eval())==1):
                    if obj.isDisplayFlagSet()==0: obj.setDisplayFlag(1)
                    dcolor=hou.node(obj.parm("Object_Trajectory").eval()).parmTuple("dcolor").eval()
                    if dcolor!=obj.parmTuple("Trajectory_Color").eval():
                        obj.setParms({"Trajectory_Colorr":dcolor[0],"Trajectory_Colorg":dcolor[1],"Trajectory_Colorb":dcolor[2]})
                else: 
                    if obj.isDisplayFlagSet()==1: obj.setDisplayFlag(0)
        else: 
            for obj in hou.node("/obj/Trajectories").children(): 
                if obj.isDisplayFlagSet()==1: obj.setDisplayFlag(0)
	hou.hscript("undoctrl on")
def autobacker():
    import hou, shutil, time
    locTime=time.localtime()
    if (time.time()%60<0.6) and (hou.hipFile.hasUnsavedChanges()==True):
        path=hou.hipFile.path()
        if path[len(path)-11:len(path)]!='_backup.hip':
            nPath=(path[0:(len(path)-4)]+"_backup.hip")
        else: nPath=path
        hou.hipFile.save(nPath,False)
        endSl=nPath.rfind("/")+1
        min=str(locTime[4])
        if len(min)==1: min="0"+min
        fName=nPath[endSl:len(nPath)-4]+"_"+str(locTime[7])+"_day"+"_"+str(locTime[3])+"."+min+"m.hip"
        shutil.copy(nPath,"C:/Users/cg15/Documents/houdini11.0/backup/"+fName)