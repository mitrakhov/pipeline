#
# Produced by:
#       Graham Thompson
#       captainhammy@gmail.com
#       www.captainhammy.com
#
# Name:         viewportutils.py
#
# Comments:     Perform tasks related to Houdini viewports.
#
# Version:      1.0
#
# Compatibility: Houdini 9.0
#

import hou

import toolutils

import time


def buildViewPath(viewer_or_scriptargs):
    """ Get a string representing the current viewport. """

    if isinstance(viewer_or_scriptargs, dict):
        activepane = toolutils.activePane(viewer_or_scriptargs)
    elif isinstance(viewer_or_scriptargs, hou.SceneViewer):
        activepane = viewer_or_scriptargs

    desktop_name = hou.ui.curDesktop().name()
    
    if not isinstance(activepane, hou.SceneViewer):
        raise hou.OperationFailed("Pane is not a Scene Viewer.")

    # Get the name of the current viewer.
    pane_name = activepane.name()

    # Get the name of the current viewer's viewport.
    viewport_name = activepane.curViewport().name()

    return "%s.%s.world.%s" % (desktop_name, pane_name, viewport_name)


def createAttributeVisualization(attribute_name, attribute_class, display_type):
    """ Add attribute visualization to the display preferences
        for the specified attribute and type.

        attribute_name: Name of the attribute to visualize.

        attribute_class: The type of attribute (point, vertex, prim)

        display_type: Type of visualization (vector, text)

        Return: The name of the display option created.

    """
    # The name of our display option.
    option_name = "\"%s (%s)\"" % (attribute_name, attribute_class.title())

    # Add a new display option.
    hou.hscript("viewoptadd %s %s" % (display_type, option_name))

    # Set the attribute of the display option.
    hou.hscript("viewoptset %s attrib ( %s )" % (option_name, attribute_name))

    # Set the geometry class type.
    hou.hscript("viewoptset %s class ( %s )" % (option_name, attribute_class))

    # Generate a random color for the visualization text.
    color = [hou.hmath.rand(time.clock() + i) for i in range(3)]

    # Override the options color.
    hou.hscript("viewoptset %s overridecolor ( 1 )" % option_name)

    # Set the option color.
    hou.hscript("viewoptset %s color ( %0.3f % 0.3f % 0.3f )" % (option_name, 
                                                                 color[0],
                                                                 color[1],
                                                                 color[2]))
    return option_name



def enableAttributeVisualization(view_path, option_name):
    """ Enable a display option in a specific viewer.

        view_path: Path to the viewport.
        option_name: Name of the the display option to enable.
    """
    hou.hscript("viewoptenable %s all +%s" % (view_path, option_name))


def disableAttributeVisualization(view_path, option_name):
    """ Disable a display option in a specific viewer.

        view_path: Path to the viewport.
        option_name: Name of the the display option to disable.
    """
    hou.hscript("viewoptenable %s all -%s" % (view_path, option_name))


def applyCOPToBackground(scene_viewer, cop_node):
    """ Apply a COP node to the Scene Viewer background. """
    view_path = buildViewPath(scene_viewer)
    hou.hscript("viewbackground -b on -S cop -C %s %s" 
                % (cop_node.path(), view_path))


def applyImageToBackground(scene_viewer, file_path):
    """ Apply an image file to the Scene Viewer background. """
    view_path = buildViewPath(scene_viewer)
    hou.hscript("viewbackground -b on -S file -F %s %s" 
                 % (file_path, view_path))

