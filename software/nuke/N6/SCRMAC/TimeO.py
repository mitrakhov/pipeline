def TimeOff():
	n = nuke.selectedNode()
	t = nuke.createNode('TimeOffset')
	t['time_offset'].setValue( -(n['first'].value() - 1))