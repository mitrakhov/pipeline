def FH():
    n = nuke.selectedNodes()
    for i in n:
        f = nuke.createNode('FrameHold')
        f.knob('first_frame').setValue(i.knob('first').getValue())
        f.setInput(0, i)
        f.knob('ypos').setValue(i.knob('ypos').getValue() + 20)