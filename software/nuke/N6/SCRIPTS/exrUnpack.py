def exrUnpack():
    
    n = nuke.selectedNode()
    chList = list(set([x.split('.')[0] for x in n.channels()]))
    
    for i in chList:
        sh = nuke.createNode('Shuffle', inpanel=False)       
        sh.knob('in').setValue(i)
        sh.knob('name').setValue(i)
        sh.setInput(0, n)
        sh.knob('hide_input').setValue(True)
        sh.knob('postage_stamp').setValue(True)
    