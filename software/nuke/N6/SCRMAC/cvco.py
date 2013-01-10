def cvco():
	import sys, cdebug
	from nukescripts import pyQtAppUtils, utils, pyWxAppUtils 
	import  subprocess

	sys.path.append('/usr/pipeline/lib')

	mdebug = cdebug.cdebug()
	import pipe
	import popen2

	name_node = '__PIPE__'
	
	nscript = nuke.scriptSaveAs('/tmp/_nktmp.nk',True)

	proc = subprocess.Popen('browser -m nuke',  shell=True, stdout=subprocess.PIPE, )
	stdout_value = proc.communicate()[0]
	
	proc2 = subprocess.Popen('vco '+stdout_value,  shell=True, stdout=subprocess.PIPE, )
	
	script_name = proc2.communicate()[0]
	mdebug(script_name)
	nuke.scriptOpen(script_name)
	
	nuke.scriptClose(nscript)
	nuke.fromScript()
	m = nuke.toNode(name_node)
	if not m: 
		m = nuke.createNode('StickyNote', inpanel=False)
		m.setName(name_node)
	asset_obj = pipe.Projects().GetAssetByInfo(script_name)
	seq = asset_obj.GetSequence()
	shot = asset_obj.GetShot()

	label = ''
	if seq: label = 'Sequence: %s'%seq.name
	if shot: label += '\nShot: %s'%shot.name
	
	m.knob('label').setValue(label)
	m.knob('note_font').setValue("Helvetica Bold")
	m.knob('note_font_size').setValue((18,))


