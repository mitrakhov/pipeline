'''Creates preview jpegs for TCP tracker to dailies folder
for TCP internal use
written by Anton Mitrakhov'''

def TPreview():
  
  import os
  from time import strftime
  
  # gets a list of read nodes
  n = nuke.selectedNodes('Read')
  for i in n:
    
    # holds a frame
    f = nuke.createNode('FrameHold')
    f.knob('first_frame').setValue(i.knob('first').getValue())
    f.setInput(0, i)
    f.knob('xpos').setValue(i.knob('xpos').getValue())
    f.knob('ypos').setValue(i.knob('ypos').getValue() + 100)
    
    # scales image to 0.5
    r = nuke.createNode('Reformat')
    r.setInput(0, f)
    f.knob('xpos').setValue(i.knob('xpos').getValue())    
    r.knob('type').setValue('scale')
    r.knob('scale').setValue(0.5)
    r.knob('ypos').setValue(i.knob('ypos').getValue() + 250)
    
    # gets output path and filename
    fname = i.knob('file').getText().rsplit('.', 1)[0].rsplit('/', 1)[-1] + '.jpg'
    fpath = i.knob('file').getText().split('/_src')[0] + '/_out/_dailies/' + strftime('%y.%m.%d')
    
    # creates write node
    w = nuke.createNode('Write')
    w.knob('file').setValue(fpath + '/' + fname)
    
    # checks for path existence
    if not os.path.exists(fpath):
      os.makedirs(fpath)
    
    # renders the output
    nuke.render (w.knob('name').getText(), start=1, end=1, incr=1)
    
    


	