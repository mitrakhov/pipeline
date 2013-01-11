def IBKAuto ():
  selNode = nuke.selectedNode()
  ibkCol = nuke.nodes.IBKColourV3()
  ibkGiz = nuke.nodes.IBKGizmoV3()
  ibkGiz.setInput(0,selNode)
  ibkGiz.setInput(1,ibkCol)
  ibkCol.knob('ypos').setValue(ibkCol.knob('ypos').value())
  ibkCol.knob('xpos').setValue(ibkCol.knob('xpos').value() - 150)
   
nuke.menu("Nodes").addCommand("Keyer/IBKAuto", "IBKAuto()", icon="IBKGizmo.png")