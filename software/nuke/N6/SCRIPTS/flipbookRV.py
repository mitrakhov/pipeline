import os
import shutil


def flipbookToRV():
    
    n = nuke.selectedNode()
    
    rv = '/mnt/opt/rv-3.4.22/bin/rv'
    
    renderPath = os.getenv('NUKE_TEMP_DIR') + os.sep + 'fbRV'
    
    if os.path.exists(renderPath):
        shutil.rmtree(renderPath)
        os.makedirs(renderPath)
    else:
        os.makedirs(renderPath)   
    
    
    fRange = nuke.getInput('Frame range:', str(n.frameRange()))
    pad = len(fRange.split('-')[-1])
    
    
    w = nuke.createNode('Write')
    if nuke.root()['proxy'].value()==1:
	       w['proxy'].setValue(renderPath + os.sep + 'tmp.%0' + str(pad) + 'd.sgi')
    else:
	       w['file'].setValue(renderPath + os.sep + 'tmp.%0' + str(pad) + 'd.sgi')
    
    w['datatype'].setValue(1)
    
    r = nuke.render (w.name(), start=int(fRange.split('-')[0]), end=int(fRange.split('-')[-1]), incr=1)
    
    nuke.delete(w)
    
    os.system(rv + ' ' + renderPath + os.sep + 'tmp.' + '#'*pad + '.sgi &')
    
nuke.menu("Nuke").addCommand("Render/Flipbook to RV", "flipbookToRV()", "ctrl+shift+f")