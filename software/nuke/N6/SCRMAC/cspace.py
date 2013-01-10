def CSpace(csp = 'sRGB'):
    inp = nuke.selectedNodes()
    for n in inp:
        n.knob('colorspace').setValue(csp)
        
        
        
