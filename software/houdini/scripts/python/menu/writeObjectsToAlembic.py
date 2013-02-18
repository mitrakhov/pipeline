import cache_utils
reload(cache_utils)

i, buff = hou.ui.readMultiInput("Input framerange and increment", ("Start","End", "Increment"),title="Write Objects To Alembic") 
cache_utils.abcCacheWrite(int(buff[0]),int(buff[1]), int(buff[2]) )