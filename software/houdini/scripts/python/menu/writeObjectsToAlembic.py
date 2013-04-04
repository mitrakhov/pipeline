import cache_utils
reload(cache_utils)
import string


formatIndex = hou.ui.selectFromList(choices = ['Alembic', 'Houdini bgeo'], default_choices = (0,), exclusive = True, title = 'Select Format')
if formatIndex: format = ''

if not format:
    if formatIndex[0] == 0: format = 'abc'
    if formatIndex[0] == 1: format = 'bgeo'

    rfstart = int(hou.playbar.playbackRange()[0])
    rfend = int(hou.playbar.playbackRange()[1])

    i, buff = hou.ui.readMultiInput("Input framerange and increment", ("Start","End", "Samples"),title = "Write Objects To Cache", buttons = ('Version', 'Overwrite', 'Cancel'), default_choice = 0, close_choice = 2, initial_contents = ( str(rfstart), str(rfend), '1' ) )  
    if i ==  0: cache_utils.cacheWrite(int(buff[0]),int(buff[1]), int(buff[2]), format, 'version' )
    if i ==  1: cache_utils.cacheWrite(int(buff[0]),int(buff[1]), int(buff[2]), format, 'overwrite' )
