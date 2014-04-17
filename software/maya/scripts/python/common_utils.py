from pymel.core import *

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
        

def assignWarningShader(node):
    surface = createNode('lambert', name = node.name() + '_Surface')
    surface.color.set([1, 0, 0])
    shader = sets( renderable=True, noSurfaceShader=True, empty=True, name=node.name() + '_Shader' )
    connectAttr(surface.name() + '.outColor', shader.name() + '.surfaceShader')
    sets(shader.name(),  forceElement = node.name())

def analyzeStruct(rootNode):
    if not rootNode.getShape() and not rootNode.getParent():
        struct = rootNode.listRelatives(allDescendents = True, type = 'transform')
        for node in struct:
            nodeNameIdent = node.name().split('_')
            #test group node
            if not node.getShape() and len(nodeNameIdent) == 2:
                if not nodeNameIdent[0] == 'g':
                        select(node)
                        warning(''.join(['[', node.name(), ']', ' - ', 'Transform have wrong prefix']) )
            elif len(nodeNameIdent) == 4:
                print 'a', node.name()
                sets('initialShadingGroup',  forceElement = node.name())
            else:
                assignWarningShader(node)
                    
    else:
        warning('It not Root Node')

#for x in ls( type='transform'):
analyzeStruct(selected()[0])
