# Copyright (c) 2007 The Foundry Visionmongers Ltd.  All Rights Reserved.

# This is copied directly from execute_panel.py with the exception
# of changing "execute" to "render" but is likely to evolve
# over time with other rendering-specific options.
 
import re
import nuke

def render_panel(_list):
  nuke.tcl('render this')