m=nuke.menu('Nuke')
n=m.addMenu('&TCP')

n.addCommand('Run degrainer', "os.system('/mnt/opt/eyeon/wine/bin/wine /mnt/opt/eyeon/Fusion/Fusion.exe &')")
n.addCommand('LightWrap2', "nuke.createNode('Lightwrap2')")
#n.addCommand('&Rise_Slate', "nuke.createNode('Rice_Slate')", "Alt+F1")
n.addCommand('&VRayElements', "nuke.createNode('VRayElements')", "Alt+F1")
#n.addCommand('&VRayElements v2', "nuke.createNode('VRayElements_v2')", "Alt+F2")
n.addCommand('&Cache D1', "nuke.createNode('cacheD1')")
n.addCommand('&FrameNumber', "nuke.createNode('FrameNumber')")
n.addCommand('&AEpremult', "nuke.createNode('AEpremult')")
n.addCommand('&ReTouch', "nuke.createNode('ReTouch')", "Alt+R")
n.addCommand('&SynthObj', "nuke.createNode('SynthObj')", "Alt+O")
n.addCommand('WaterDistort', "nuke.createNode('WaterDistort')")
n.addCommand('FakeMotionBlur', "nuke.createNode('FakeMotionBlur')")
n.addCommand('&LABCorrect', "nuke.createNode('LABCorrect')")
n.addCommand('Duplicator', "nuke.createNode('Duplicator')")
n.addCommand('LinkTo', "nuke.createNode('LinkTo')")
nuke.load("autobackdrop")
n.addCommand('AutoBackdrop', "AutoBackDrop()", "Ctrl+Alt+B")
nuke.load("mocha_autoimport")
n.addCommand('Import Mocha tracker', "MochaImport()", "Ctrl+Alt+T")
nuke.load("mocha_autoimport_cornerpin")
n.addCommand('Import Mocha cornerpin', "MochaImportCornerPin()", "Ctrl+Alt+C")
nuke.load("projectioncam")
n.addCommand('ProjectionCamSetup', "ProjectionCam()", "Ctrl+Alt+P")
nuke.load("framehold2")
n.addCommand('FrameHold2', "FrameHold()", "Ctrl+Alt+F")
nuke.load("pythonhelp")
nuke.load("TimeO")
n.addCommand('TimeOffset2', "TimeOff()", "Ctrl+Shift+T")

nuke.load('dailies')
n.addCommand('CreateDailies (old)', 'Dailies()')

nuke.load('exr2tif')
n.addCommand('Exr2Tif', 'exr2tif()')

nuke.menu("Nodes").addCommand("Draw/Bezier", "nuke.createNode('Bezier')", "u")

#n.addCommand('PythonHelp', "PythonHelp()")
# kogda blya!
#m.addCommand("-", "", "")
#m.addCommand("Submit To Deadline", "nuke.tcl( \"SubmitToDeadline\" )" , "")


m.addCommand("TCP/ioManager", "nuke.tcl( \"ioManager\" )", "+i")

n=m.addMenu('&Deadline')
#m.addCommand('Deadline', "nuke.tcl( \"SubmitToDeadline\" )" , "F10")
m.addCommand("Deadline/Submit to &Deadline", "nuke.tcl( \"SubmitToDeadline\" )", "F10")

nuke.menu("Nuke").addCommand("Edit/Node/Paste Knob Values", "nuke.tcl('paste_knobs')", "alt+v")
nuke.menu("Nuke").addCommand("Edit/Node/Paste Animatable Knob Links", "nuke.tcl('paste_knobs link')", "ctrl+alt+v")
nuke.menu("Nuke").addCommand("Edit/Node/Paste All Knob Links", "nuke.tcl('paste_knobs linkall')", "shift+alt+v")

# Pipeline
n = m.addMenu('Pipeline')

#nuke.load('mocha_open')
#n.addCommand('Go to mocha', 'mocha_open()')

#nuke.load('load_src')
#n.addCommand('Load SRC', 'load_src()')

#nuke.load('hqsubmit')
#n.addCommand('HQ submit','hqsubmit()')

#nuke.load('cnew')
#n.addCommand('New script', 'cnew()')

#nuke.load('cvci')
#n.addCommand('CheckIn', 'cvci()')

#nuke.load('cvco')
#n.addCommand('CheckOut','cvco()')

#nuke.load('hiRes')
#n.addCommand('Create HiRes','CreateHires()')

#nuke.load('tfxGetResources')
#n.addCommand('Get render data','GetResources()')

#nuke.load('hiResAfanasyTfx')
#n.addCommand('Create HiRes Afanasy','CreateHiresByAfanasy()')

#nuke.load('pipeDailies')
#n.addCommand('Create Dailies','PipeDailies()')

#nuke.load('slate')
#n.addCommand('Create TCP Slate', 'Slate()')

#nuke.load('tfxSlate')
#nuke.load('slate2')
#n.addCommand('Create TFX Slate', 'tfxSlate()')

#nuke.load('fillReads')
#n.addCommand('ReloadRenders', 'fillReads()')

nuke.load('jobLocal')
n.addCommand('Set local', 'setLocal()')
n.addCommand('Add to local', 'addLocal()')

nuke.load('www')
n.addCommand('Watch some porn', 'www()')

nuke.load('flipbookRV')

# IBKAuto
nuke.load("AutoIBK")

# Misc scripts
nuke.load("AutoProxy")
nuke.load("deniska")
nuke.load("getpass")
# AutoBackdrop



# Knob defaults
nuke.knobDefault("Bezier.cliptype", "none")
#nuke.knobDefault("Write.channels", "rgba")
nuke.knobDefault("Bezier.output", "alpha")
nuke.knobDefault("Tracker3.filter", "Simon")
nuke.knobDefault("Constant.channels", "rgba")
nuke.knobDefault("Constant.format", str(nuke.root()['format'].value().name()))
#nuke.knobDefault("Tracker3.black_outside", "false")
#nuke.knobDefault("Transform.black_outside", "false")
nuke.knobDefault("Reformat.black_outside", "true")
nuke.knobDefault("CornerPin2D.filter", "Simon")
nuke.knobDefault("AddMix.premultiplied", "true")
nuke.knobDefault("Root.fps", "24")
nuke.knobDefault("Root.format", "RED 2K")
nuke.knobDefault("CheckerBoard2.name", "Kachur")
nuke.knobDefault("CheckerBoard2.format", str(nuke.root()['format'].value().name()))
nuke.knobDefault('Slate.format', 'HDHalf')
nuke.knobDefault('slate2.format', 'RED 1K')
nuke.knobDefault('Roto.format', str(nuke.root()['format'].value().name()))
nuke.knobDefault('RotoPaint.format', str(nuke.root()['format'].value().name()))
nuke.knobDefault('Read.auto_alpha', 'True')
# flameconnect
import flameConnect 

nodeMenu = nuke.menu('Nodes')
nodeMenu.addCommand ('Other/flameConnect', 'flameConnect.testen()', ' +y')

# Mari
import mari_bridge
