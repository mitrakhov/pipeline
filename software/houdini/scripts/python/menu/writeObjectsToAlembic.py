import cache_utils
reload(cache_utils)

rfstart = int(hou.playbar.playbackRange()[0])
rfend = int(hou.playbar.playbackRange()[1])

i, buff = hou.ui.readMultiInput("Input framerange and increment", ("Start","End", "Samples"),title="Write Objects To Alembic",buttons = ('Ok', 'Cancel'), default_choice = 0, close_choice = 1, initial_contents = ( str(rfstart), str(rfend), '1' ) )  
if i ==  0: cache_utils.abcCacheWrite(int(buff[0]),int(buff[1]), int(buff[2]) )
