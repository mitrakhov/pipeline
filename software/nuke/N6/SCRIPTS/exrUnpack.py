def exrUnpack():  
    """ Creates shuffle nodes for each channel in EXR
    
    """
    n = nuke.selectedNode()
    chList = list(set([x.split('.')[0] for x in n.channels()]))
    shList = [x['name'].value() for x in nuke.allNodes('Shuffle')]
    
    print 'ShotList is ', shList
    
    for i in chList:
        
        sh = nuke.createNode('Shuffle', inpanel=False)       
        sh.knob('in').setValue(i)
        
        nmList = [x for x in shList if x.startswith(i)]
        
        if nmList:
            nmList.sort()
            lastNumb = nmList[-1].rsplit('.',1)[-1]
            if lastNumb.isdigit():
                shName = i + '.' + str(int(lastNumb)+1)
            else:
                shName = nmList[0] + '.1'
        else:
            shName = i + '.1'    
        
        sh.knob('name').setValue(shName)
        sh.setInput(0, n)
        sh.knob('hide_input').setValue(True)
        sh.knob('postage_stamp').setValue(True)
