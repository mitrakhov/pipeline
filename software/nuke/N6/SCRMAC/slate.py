import sys
sys.path.append('/usr/pipeline/lib')
import pipe
import os
import socket
import time


def Slate():
    
    sObj = pipe.Projects().GetAssetByInfo(nuke.root().name())

    # pInfo values

    pName = sObj.GetProject().name
    
    sqName = sObj.GetShot().seq_name
    
    sName = sObj.GetShot().name
    
    movPath = sObj.GetShot().GetOutPath() + '/dailies/'
    
    if os.listdir(movPath):
        
        vNum = str(max([int(x.rsplit('.', 2)[-2].split('v')[-1]) for x in os.listdir(movPath) if x[:len(sName)] == sName]) + 1)
    
    else:
    
        vNum = '1'
        
        
    # sInfo values
    
    sDescr = sObj.GetDescription()
 
    notes = nuke.getInput('Enter submission notes:\animation approval, rig removal approval etc', sDescr + ' approval')   
    
    mName = socket.gethostname().split('.', 1)[0]

    uVoc = {'scooby': 'Hanna Kucherevich',
            'porky': 'Anton Mitrakhov',
            'vinny': 'Zhanna Fitsay',
            'pluto':'Ievgen Kulieshov',
            'bender':'Denis Siplenko',
            'daffy':'Yevgen Skorobogatko',
            'piglet':'Ilya Goncharov',
            'lynx':'Alexandra Glukhova',
            'casper':'Vladimir Mikheyenko',
            'kermit':'Vlad Scripnik'}
    
    if not mName in uVoc.keys():
        
        aName = nuke.getInput('Enter your name:', 'Alexander Koreshkov')
        
    else:
        
        aName = uVoc[mName]
           
            
    res = nuke.root().knob('format').value().name() + ' ' + str(nuke.root().knob('format').value().width()) + 'x' + str(nuke.root().knob('format').value().height())                         
   
    tFC = str(int(nuke.animationEnd() - nuke.animationStart()) + 1) + ' frames'
    
    fps = str(int(nuke.root().knob('fps').value())) + ' fps'
    
    dOS = strftime('%y.%m.%d')    
    
    
    
    # slate node creation   
    
    s = nuke.createNode('Slate')
    
    s.knob('pInfo').setValue('Project: ' + pName + 
                             '\nSequence: ' + sqName +
                             '\nShot: ' + sName +  
                             '\nVersion: ' + vNum)
    
    s.knob('sInfo').setValue('Shot description: ' + sDescr +
                            '\nNotes: ' + notes +
                            '\nArtist: ' + aName +
                            '\nResolution: ' + res +
                            '\nTotal frame count: ' + tFC +
                            '\nFrame Rate: ' + fps +
                            '\nDate of submission: ' + dOS)
                                                    
 

    
    