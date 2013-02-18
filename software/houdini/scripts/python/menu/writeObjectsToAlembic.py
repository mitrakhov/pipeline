import utils
reload(utils)
i, buff = hou.ui.readMultiInput("Input framerange", ("Start","End"),title="Bake object to world") 
utils.bakeObjectToWorld(int(buff[0]),int(buff[1]))