def techrig_buildFKControlChain_Tool():
    import hou 
    bones = techrig_userInput_startBoneEndBone()
    if (bones == (None, None)):
        return None
    techrig_buildFKControlChain(bones[0], bones[1])



def techrig_userInput_startBoneEndBone():
    import toolutils 
    sViewer = toolutils.sceneViewer()
    startBone = sViewer.selectObjects('Select start bone, press enter to confirm', allowed_types=('bone',), allow_multisel=False)
    if (startBone == ()):
        hou.ui.displayMessage('Start bone not selected, terminating tool', severity=hou.severityType.Error)
        return (None, None)
    startBone[0].setSelected(0, True)
    endBone = sViewer.selectObjects('Select end bone, press enter to confirm', allowed_types=('bone',), allow_multisel=False)
    if (endBone == ()):
        hou.ui.displayMessage('End bone not selected, terminating tool', severity=hou.severityType.Error)
        return (None, None)
    if (not techrig_findChildInHierarchy(startBone[0], endBone[0])):
        hou.ui.displayMessage('End bone does not exist in same hierarchy as start bone, terminating tool', severity=hou.severityType.Error)
        return (None, None)
    return (startBone[0],
     endBone[0])



def techrig_findChildInHierarchy(parentNode, childNode):
    done = 0
    currentNode = childNode
    while (not done):
        if (currentNode == parentNode):
            return 1
        elif (currentNode.inputs() != ()):
            currentNode = currentNode.inputs()[0]
        else:
            done = 1

    return 0



def techrig_buildFKControlChain(startBone, endBone):
    done = 0
    currentBone = endBone
    returnList = []
    while (not done):
        returnList.append(techrig_buildFKControl(currentBone))
        if (currentBone == startBone):
            done = 1
        else:
            currentBone = currentBone.inputs()[0]

    return returnList



def techrig_buildFKControl(bone):
    import hou 
    parentNode = bone.parent()
    fkControl = parentNode.createNode('null', (bone.name() + '_FKControl'))
    fkControl.setFirstInput(bone)
    fkControl.parm('keeppos').set(1)
    fkControl.parm('rOrd').setExpression((('ch("' + fkControl.relativePathTo(bone)) + '/rOrd")'))
    if (bone.inputs() != ()):
        fkControl.setFirstInput(bone.inputs()[0])
    else:
        fkControl.setFirstInput(None)
    fkControl.moveParmTransformIntoPreTransform()
    bone.parm('rx').setExpression((('ch("' + bone.relativePathTo(fkControl)) + '/rx")'))
    bone.parm('ry').setExpression((('ch("' + bone.relativePathTo(fkControl)) + '/ry")'))
    bone.parm('rz').setExpression((('ch("' + bone.relativePathTo(fkControl)) + '/rz")'))
    bone.parm('picking').set(0)
    fkControl.setColor(hou.Color((0, 0.59999999999999998, 1)))
    fkControl.parm('controltype').set(1)
    fkControl.parm('tx').lock(1)
    fkControl.parm('ty').lock(1)
    fkControl.parm('tz').lock(1)
    fkControl.parm('sx').lock(1)
    fkControl.parm('sy').lock(1)
    fkControl.parm('sz').lock(1)
    fkControl.parm('px').lock(1)
    fkControl.parm('py').lock(1)
    fkControl.parm('pz').lock(1)
    fkControl.moveToGoodPosition()
    return fkControl