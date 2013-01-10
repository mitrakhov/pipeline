# ###   Rename several nodes at once
# ###   renamenodes.py
# ###   v2.1 - Last modified: 09/12/2008
# ###   Written by Diogo Girondi
# ###   diogogirondi@gmail.com

import nuke

def renamenodes():

    sn = nuke.selectedNodes()
    sn.reverse()

    if sn != []:
        newname = nuke.getInput("New name:")
        for index, n in enumerate(sn):
            n.knob('name').setValue(newname.replace(' ', '_') + str(index+1))
    else:
        nuke.message("Rename Nodes:\nSelect at least one node")