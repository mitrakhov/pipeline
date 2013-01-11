import os

def exr2tif():
    
    n = nuke.selectedNode()
    
    if not n.Class() == 'Read':
        
        nuke.message('Not a Read node!')
        
        return
    
    chList = list(set([x.split('.')[0] for x in n.channels()]))
    
    nList = [x.name() for x in nuke.allNodes('Shuffle')]
    
    for i in chList:
        
        sh = nuke.createNode('Shuffle', inpanel=False)
        
        sh.knob('in').setValue(i)
        
        sh.knob('name').setValue(i)
             
        sh.setInput(0, n)
        
        w = nuke.createNode('Write', inpanel=False)
        
        newPath = n.knob('file').value().rsplit('/',1)[0] + '/' + i
        
        if not os.path.exists(newPath):
            
            os.mkdir(newPath)
            
        w.knob('file').setValue(newPath + '/' + i + '.%06d.tif')
        
        w.knob('file_type').setValue('tiff')
        
        w.knob('datatype').setValue(1)
        
        nuke.execute(w.name(), n.knob('first').value(), n.knob('last').value())
        
        nuke.delete(sh)
        
        nuke.delete(w)
    