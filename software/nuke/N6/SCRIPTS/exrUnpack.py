def exrUnpack():
    
    n = nuke.selectedNode()
    chList = list(set([x.split('.')[0] for x in n.channels()]))
    
    allNames = [x['name'].value() for x in nuke.allNodes() if x.Class()=="Shuffle"]
    
    for i in chList:
        sh = nuke.createNode('Shuffle', inpanel=False)       
        sh.knob('in').setValue(i)
        iName = i + '.1'
        if iName in allNames: 
            iName = i + '.' + str(int(iName.rsplit('.',1)[-1])+1)
        sh.knob('name').setValue(iName)
        sh.setInput(0, n)
        sh.knob('hide_input').setValue(True)
        sh.knob('postage_stamp').setValue(True)
    