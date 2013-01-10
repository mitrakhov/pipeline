''' Creates ProjectionCam setup from selected camera
    for Nuke5.1vx 
    written by Anton Mitrakhov   '''


def ProjectionCam():
  
  try:
    cam = nuke.selectedNode()
  
  # returns if nothing selected
  
  except ValueError: 
    nuke.message('Select a camera node to project from')
    return
  
  # returns if selected node isn't a camera
  
  if cam.Class() not in ['Camera','Camera2']:
    nuke.message('Not a camera node')
    return
  
  # checking the script for existing ProjectionCam nodes, to put a proper name
  
  input = nuke.allNodes()
  y = "ProjectionCam"
  list = [int(x.name().split(y)[-1]) for x in input if x.name()[:len(y)] == y]

  n = 1
  
  if list != []:
    n = max(list) + 1

  # creates a ProjCam node
     
  cam.knob('selected').setValue(False)
  prcam = nuke.createNode('Camera')
  prcam.addKnob(nuke.Tab_Knob('RefTab', 'ProjectionFrame'))
  prcam.addKnob(nuke.Int_Knob('RefFrame', 'ReferenceFrame'))
  prcam.knob('name').setValue("ProjectionCam%s"%n)
  prcam.knob('label').setValue('On frame:\n[value RefFrame]')
  prcam.knob('RefFrame').setValue(nuke.frame())
  
  # setting values for translate, rotation and scaling
  
  tr = (('{' + cam.knob('name').value() + '.' + 'translate' + '(RefFrame)' + '}' + ' ')*3).rstrip(' ')
  prcam.knob('translate').fromScript(tr)
  rt = (('{' + cam.knob('name').value() + '.' + 'rotate' + '(RefFrame)' + '}' + ' ')*3).rstrip(' ')
  prcam.knob('rotate').fromScript(rt)
  sc = (('{' + cam.knob('name').value() + '.' + 'scaling' + '(RefFrame)' + '}' + ' ')*3).rstrip(' ')
  prcam.knob('scaling').fromScript(sc)  
  
  # values for focal length and apertures 
  
  prcam.knob('focal').fromScript(cam.knob('name').value() + '.' + 'focal' + '(RefFrame)')
  prcam.knob('haperture').setValue(cam.knob('haperture').value())
  prcam.knob('vaperture').setValue(cam.knob('vaperture').value())  

  # rot and tr orders
  
  prcam.knob('xform_order').setValue(cam.knob('xform_order').value())
  prcam.knob('rot_order').setValue(cam.knob('rot_order').value()) 
  
  # creates a Project3D node  
  proj = nuke.createNode('Project3D')
  proj.knob('ypos').setValue(prcam.knob('ypos').value())
  proj.knob('xpos').setValue(prcam.knob('xpos').value() + 120)

  prcam.setInput(0, None)
