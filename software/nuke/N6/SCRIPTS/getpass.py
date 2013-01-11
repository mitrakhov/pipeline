'''Script for getting Vray passes from exr
written by Anton Mitrakhov
TCP 2009
'''


def GetPass():
	
	n = nuke.selectedNode()
	inp = nuke.getInput('Print "GI" to get VRayGlobalIllumination \n \
"Refl" for Reflection \n \
"Light" for Lighting \n \
"Sh" for Shadows')
	
	if inp == 'GI':
	  rp = 'VRayGlobalIllumination'
	  s = nuke.createNode('Shuffle', inpanel=False)
	  s.knob('in').setValue(rp)
	  c = nuke.createNode('Copy', inpanel=False)
	  c.setInput(0, n)
	  c.setInput(1, s)
	  c.knob('to0').setValue(rp + '.red')
	  c.knob('to1').setValue(rp + '.green')
	  c.knob('to2').setValue(rp + '.blue')
	  c.knob('from0').setValue('rgba.red')
	  c.knob('from1').setValue('rgba.green')
	  c.knob('from2').setValue('rgba.blue')
	  nuke.autoplace(s)
	  nuke.autoplace(c)	
	
	elif inp == 'Refl':
	  rp = 'VRayReflection'
	  s = nuke.createNode('Shuffle', inpanel=False)
	  s.knob('in').setValue(rp)
	  c = nuke.createNode('Copy', inpanel=False)
	  c.setInput(0, n)
	  c.setInput(1, s)
	  c.knob('to0').setValue(rp + '.red')
	  c.knob('to1').setValue(rp + '.green')
	  c.knob('to2').setValue(rp + '.blue')
	  c.knob('from0').setValue('rgba.red')
	  c.knob('from1').setValue('rgba.green')
	  c.knob('from2').setValue('rgba.blue')
	  nuke.autoplace(s)
	  nuke.autoplace(c)
	
	elif inp == 'Light':
	  rp = 'VRayLighting'
	  s = nuke.createNode('Shuffle', inpanel=False)
	  s.knob('in').setValue(rp)
	  c = nuke.createNode('Copy', inpanel=False)
	  c.setInput(0, n)
	  c.setInput(1, s)
	  c.knob('to0').setValue(rp + '.red')
	  c.knob('to1').setValue(rp + '.green')
	  c.knob('to2').setValue(rp + '.blue')
	  c.knob('from0').setValue('rgba.red')
	  c.knob('from1').setValue('rgba.green')
	  c.knob('from2').setValue('rgba.blue')
	  nuke.autoplace(s)
	  nuke.autoplace(c)	 
	
	elif inp == 'Sh':
	  rp = 'VRayShadows'
	  s = nuke.createNode('Shuffle', inpanel=False)
	  s.knob('in').setValue(rp)
	  c = nuke.createNode('Copy', inpanel=False)
	  c.setInput(0, n)
	  c.setInput(1, s)
	  c.knob('to0').setValue(rp + '.red')
	  c.knob('to1').setValue(rp + '.green')
	  c.knob('to2').setValue(rp + '.blue')
	  c.knob('from0').setValue('rgba.red')
	  c.knob('from1').setValue('rgba.green')
	  c.knob('from2').setValue('rgba.blue')
	  nuke.autoplace(s)
	  nuke.autoplace(c)	 
	
	else:
	  pass

