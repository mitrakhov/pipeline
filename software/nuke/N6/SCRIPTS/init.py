 

nuke.knobDefault("fps", "25")
nuke.knobDefault("format", "1920 1080 0 0 1920 1080 1 HD")
nuke.knobDefault("proxy_type", "format")
nuke.knobDefault("before", "black")
nuke.knobDefault("after", "black")
nuke.knobDefault("on_error", "checkerboard")
nuke.addSequenceFileExtension("rat")
nuke.addSequenceFileExtension("pic")

#nuke.knobDefault("Root.monitorLut", "linear")
#nuke.knobDefault("Root.viewerLut", "linear")
#nuke.knobDefault("Root.int8Lut", "linear")
#nuke.knobDefault("Root.int16Lut", "linear")
#nuke.knobDefault("Root.logLut", "linear")
#nuke.knobDefault("Root.floatLut", "linear")
