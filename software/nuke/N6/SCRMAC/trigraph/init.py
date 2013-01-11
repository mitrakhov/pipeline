# Copyright 2010 by Serge Zaporozhtsev.
# TRIinit nuke script v1.1
# -*- coding: utf-8 -*-
#

import os
import nuke
import re
import getpass
from datetime import datetime

def _check_framerange():
    if int(nuke.numvalue("root.first_frame")) < 1:
        raise ValueError("Start frame number can not be less than 1")
    return

nuke.addBeforeRender(_check_framerange)

def fr2tc(f, fps):
    """
    Convert frame nuber to timecode string
    """
    fr = f % fps
    f = int(f / fps)
    s = f % 60
    f = int(f / 60)
    m = f % 60
    h = int(f / 60)
    return '%02d:%02d:%02d:%02d' % (h, m, s, fr)

def sceneName():
    """
    Return scene name without version
    """
    root = nuke.root()
    (pName, pExt) = os.path.splitext(os.path.basename(root['name'].value()))
    
    m = re.search("^(.*)_(v\d\d)_?(.*)$", pName)
    if m is None:
        return pName
    else:
        return m.group(1)

def sceneVer(prefix=""):
    """
    Return scene version number if any
    """
    root = nuke.root()
    (pName, pExt) = os.path.splitext(os.path.basename(root['name'].value()))
    
    m = re.search("^(.*)_(v\d\d)_?(.*)$", pName)
    if m is None:
        return None
    else:
        return prefix + m.group(2)

def sceneComment():
    """
    Return scene comment if any
    """
    root = nuke.root()
    (pName, pExt) = os.path.splitext(os.path.basename(root['name'].value()))
    
    m = re.search("^(.*)_(v\d\d)_?(.*)$", pName)
    if m is None:
        return None
    else:
       	return m.group(3)

def artistName():
    """
    Return artist name
    """
    if 'tri_project_artist' in nuke.root().knobs():
        if nuke.root()['tri_project_artist'].value() != "":
            return nuke.root()['tri_project_artist'].value()
    else:
        return getpass.getuser().lower()

def getDate(format):
    """
    Return stirn wih current data in given format
    """
    return datetime.now().strftime(format)

def sceneLenght():
    return int(nuke.numvalue("root.last_frame") - nuke.numvalue("root.first_frame") + 1)
    """
    Return lenght of scene in frames
    """

def startFrame():
    """
    Return first frame number in scene
    """
    return int(nuke.numvalue("root.first_frame"))

def lastFrame():
    """
    Return last frame number in scene
    """
    return int(nuke.numvalue("root.last_frame"))

def currentFrame():
    """
    Return current source frame number
    """
    return int(nuke.numvalue("frame"))

def currentSceneFrame():
    """
    Return current frame number in scene
    """
    return int(nuke.numvalue("frame") - nuke.numvalue("root.first_frame") + 1)


def _tri_render_panel(_list, exceptOnError=True):
 	"""
	This is copied directly from execute_panel.py with the exception
	of changing "execute" to "render" but is likely to evolve
	over time with other rendering-specific options.
	"""

	start = int(nuke.numvalue("root.first_frame"))
	end = int(nuke.numvalue("root.last_frame"))
	incr = 1
	if start < 1:
	    nuke.message("Start frame number cannot be less than 1")
	    return

	try:
	    _range = str(nuke.FrameRange(start, end, incr))
	except ValueError,e:
	     # In this case we have to extract from the error message the
	     # correct frame range format string representation.
	     # I'm expecting to have an error like: "Frame Range invalid (-1722942,-1722942)"
	     msg = e. __str__()
	     _range = msg[msg.index("(")+1:  msg.index(")")]

	r = nuke.getInput("Frames to render:", _range)
	if r is not None:
	    frame_ranges = nuke.FrameRanges(r)
	    if nuke.thisNode()['slate'].value() is True:
	        frame_ranges.add(nuke.FrameRange(start - 1, start - 1, 1))
	        frame_ranges.compact()
	    nuke.tprint(frame_ranges)
 
	    try:
	        nuke.executeMultiple(_list, frame_ranges)
	    except RuntimeError, e:
	        if exceptOnError or e.message[0:9] != "Cancelled":   # TO DO: change this to an exception type
	            raise
