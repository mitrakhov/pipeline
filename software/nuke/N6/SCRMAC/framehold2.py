def FrameHold(): 
  n = nuke.createNode('FrameHold')
  n.knob('first_frame').setValue(nuke.frame())
#  n.addKnob(nuke.PyScript_Knob("sf", "Set to current frame"))
#  n.knob('sf').setCommand("nuke.selectedNode().knob('RefFrame').setValue(nuke.frame())")
  
  
