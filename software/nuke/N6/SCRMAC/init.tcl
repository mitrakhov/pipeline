#plugin_addpath "//bigboy/d/tfxtools/Nuke/gizmo"
#plugin_addpath "//bigboy/d/tfxtools/Nuke/python"
#plugin_addpath "//bigboy/d/tfxtools/Nuke/tcl"

#plugin_addpath "/mnt/bigboy/tfxtools/Nuke/gizmo"
#plugin_addpath "/mnt/bigboy/tfxtools/Nuke/python"
#plugin_addpath "/mnt/bigboy/tfxtools/Nuke/tcl"

#plugin_addpath "/Volumes/d/tfxtools/Nuke/gizmo"
#plugin_addpath "/Volumes/d/tfxtools/Nuke/python"
#plugin_addpath "/Volumes/d/tfxtools/Nuke/tcl"

add_format "4096 2304                    1.0   RED 4K"
#add_format "4096 2048                    1.0   RED 4K 2:1"
add_format "3072 1728                    1.0   RED 3K"
#add_format "3072 1152                    1.0   RED 3K 2:1"
add_format "2048 1152                    1.0   RED 2K"
#add_format "2048 1024                    1.0   RED 2K 2:1"
add_format "1024 576                    1.0   RED 1K"
#add_format "1024 512                    1.0   RED 1K 2:1"

add_format "768 576                    1.0   PAL square"

knob_default root.format "1920 1080 1"
knob_default root.proxy_format "960 540 1"