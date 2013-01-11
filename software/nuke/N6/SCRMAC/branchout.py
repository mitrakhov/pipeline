###   Branch out Layers
###   v1.0 - Last modified: 11/01/2008
###   Written by Diogo Girondi
###   diogogirondi@gmail.com

import nuke

def branchout():
    
    sn = nuke.selectedNode()
    ch = nuke.channels(sn)
    layers = []
    valid_channels = ['red', 'green', 'blue', 'alpha', 'black', 'white']

    for each in ch:
        current = each.split('.')
        layer = current[0]
        channel = current[1]
        tmp = []
        
        for x in ch:
            if x.startswith(layer) == True:
                tmp.append(x)
                
        if len(tmp) < 4:
            for i in range(4-len(tmp)):
                tmp.append(layer+".black")
                
        if tmp not in layers:
            layers.append(tmp)
            
    for each in layers:
        name = each[0].split('.')[0]
        
        r = each[0].split('.')[1]
        if r not in valid_channels:
            r = valid_channels[0]
            
        g = each[1].split('.')[1]
        if g not in valid_channels:
            g = valid_channels[1]
        
        b = each[2].split('.')[1]
        if b not in valid_channels:
            b = valid_channels[2]
        
        a = each[3].split('.')[1]
        if a not in valid_channels:
            r = valid_channels[3]
            
        inLayer = "in " + name + " red " + r + " green " + g + " blue " + b + " alpha " + a
        shuffle = nuke.createNode('Shuffle', inLayer)
        shuffle.knob('label').setValue(name)
        shuffle.setInput(0, sn)