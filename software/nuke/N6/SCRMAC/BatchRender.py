#
# launchNukes_inNuke.py
#
# v01
#
# a script for launching single-core command-line nuke renderers 
# from inside the Nuke UI.
# 
# also saves log files of each instance's output to the same folder
# where the Nuke script lives. 
#

import re
import nuke
import os
import sys

def launch_nukes(): 
    a = nuke.knob("first_frame")
    b = nuke.knob("last_frame")
    start = int(a)
    end = int(b)
    incr = 1
    instances = 1
    _range = a+","+b
    p = nuke.Panel("Launch Nukes")
    p.addSingleLineInput("Frames to execute:", _range)
    p.addSingleLineInput("Number of background procs:", instances)
    p.addButton("Cancel")
    p.addButton("OK")
    result = p.show()
    
    r = p.value("Frames to execute:")
    s = p.value("Number of background procs:")
    if r is None: 
        return
    if s is None: 
        return
    # this is the requested frame range
    frames = r
    # this is the number of instances to launch
    inst = int(s)

    (scriptpath, scriptname) = os.path.split(nuke.value("root.name"))
    flags = "-ixfm 1"
    
    print ">>> launching %s nuke instances" % inst
    
    # create a frame range string for each renderer
    for i in range(inst):
        print ">>> generating range for instance %d" % i
        instRange = ""
    
        # separate ranges at spaces
        f = frames.split(" ")
        
        # separate individual start, end, and increment values
        for p in f:
            c = p.split(",")
            incr = 1
            if len(c) > 0:
                start = int(c[0])
                end = start
            if len(c) > 1: end = int(c[1])
            if len(c) > 2: incr = int(c[2])
            
            # re-jigger this range for this instance of the renderer
            st = start + ( i * incr )
            en = end
            inc = incr * inst
            new = "%d,%d,%d" % (st, en, inc)
            if inc == 1:
                new = "%d,%d" % (st, en)
            if en == st:
                new = "%d" % st
            if st > en:
                new = ""
            else:
                # add the re-jiggered range to the instances range string
                instRange = instRange + " " + new
                
        print ">>> range for instance %d is: %s" % (i, instRange)
        
        logFile = "%s/%s_log%02d.log" % (scriptpath, scriptname, i)
        
        cmd = "%s %s %s/%s %s > %s &" % (nuke.EXE_PATH, flags, scriptpath, scriptname, instRange, logFile)
        print ">>> starting instance %d" % (i, )
        print "command: " + cmd
        os.system(cmd)