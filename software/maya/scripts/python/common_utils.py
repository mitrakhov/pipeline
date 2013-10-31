def bakeObjectAnimToWorld(object, startFrame, endFrame):
    try:
        object[0]
    except IndexError:
        warning('Select Object for Baking')
    else:
        
        camBake = duplicate(name = ''.join([object[0].name(), '_bake']))[0]
        if camBake.getParent() != None:
            parent(camBake, world = True)
        camBake.setTranslation( (0, 0, 0), space='world' )
        camBake.setRotation( (0, 0, 0), space='world' )
        pointCon = pointConstraint(object, camBake)
        orientCon = orientConstraint(object, camBake)
        bakeResults(camBake, attribute = ('translate', 'rotate'), time = (startFrame, endFrame) )
        delete(pointCon, orientCon)