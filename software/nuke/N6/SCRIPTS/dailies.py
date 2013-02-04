# -*- coding: utf-8 -*-
'''Script for dailies creation. 
OS: Linux, for Nuke5.x
uses DJV for *.mov creation
Written by Anton Mitrakhov
The Chimney Pot

'''

import os
from time import strftime

def MakeMov():

  # paths to djv folder
  pp = os.getenv('PROGRAM_PATH')
  djv = pp + '/djv/bin/djv_convert'
  djView = pp + '/djv/bin/djv_view'
  
  # path for render preview folder and filename
  rPath = nuke.root().name().rsplit('/', 1)[0] + '/render/preview/'
  fName = nuke.root().name().rsplit('/', 1)[-1].split('.nk')[0]	
  prList = [x for x in os.listdir(rPath) if x[:len(fName)] == fName]
  prList.sort()
  sPath = prList[0].rsplit('.', 1)[0] + '-' + str(int(nuke.animationEnd())) + '.jpg'
  dPath = rPath.split('_compose')[0] + '_out/_dailies/' + strftime('%y.%m.%d')
  
  # creates dailies folder if necessary
  if not os.path.exists(dPath):
    os.makedirs(dPath)
  fPath = djv + ' ' + rPath + sPath + ' ' + dPath + '/' + fName + '.mov'
  
  # runs convertation
  os.system(fPath)
  
  # opens *.mov file
  vPath = djView+ ' ' + dPath + '/' + fName + '.mov &'
  os.system(vPath)

def Dailies():
  
  # path for render preview folder and filename
  rPath = nuke.root().name().rsplit('/', 1)[0] + '/' + 'render' + '/' + 'preview' + '/'
  fName = nuke.root().name().rsplit('/', 1)[-1].split('.nk')[0]	
  
  # creates preview render folder if necessary
  if not os.path.exists(rPath):
    os.makedirs(rPath)  
  
  # takes padding
  pad = len(str(int(nuke.animationEnd())))
  
  # creates write node
  w = nuke.createNode('Write')
  w.knob('file').setValue(rPath + fName + '_' '%0' + str(pad) + 'd.jpg')
  w.knob("_jpeg_quality").setValue(1)
  w.addKnob(nuke.Tab_Knob('CMov', 'Create *.mov'))
  w.addKnob(nuke.PyScript_Knob('MMov', 'Make *.mov'))
  w.knob('MMov').setCommand('MakeMov()')
  
  # user part
  a = nuke.ask('Othuyachit sequence?')
  if a == True:
    nuke.render (w.knob('name').getText(), start=int(nuke.animationStart()), end=int(nuke.animationEnd()), incr=1)
    b = nuke.ask('Othuyachit *.mov?')
    if b == True:
      MakeMov()
    else:
      pass
  else:
    pass







  
  
  
  
  
  
  
  
  
  
  
  
  
