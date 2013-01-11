# formats.tcl
# Copyright (c) 2007 The Foundry Visionmongers Ltd.  All Rights Reserved.
#
# Formats let Nuke assign a name, pixel aspect ratio, and possibly
# a cropped image area, to any size of input image. You can make
# more than one format for a given size but the user will have to
# pick the other ones from the chooser in the file reader.
#
#       W = Total image width in pixels
#       H = Total image height in pixels
#       x = left edge of active region
#       y = bottom edge of active region
#       r = right edge of active region
#       t = top edge of active region
#      pa = pixel-aspect ratio (width/height of a pixel)
#    name = the name displayed in the menus
#
# xyrt may be omitted to set them to 0 0 W H.
# if xyrt are omitted, you can also omit pa and it is set to 1.0
#---------------------------------------------------------------------------

# The PAL and NTSC formats were changed in Nuke 5.2 to respect the pixel aspect ratio of
# the production aperture instead of the clean aperture. This provides greater compatibility
# with other software, and produces images which are no longer slightly stretched.

#              W    H   x   y    r    t   pa   name
#---------------------------------------------------------------------------
# 4:3 video formats
add_format " 640  480                    1.0   PC_Video"
add_format " 720  486                    0.91  NTSC"
add_format " 720  576                    1.09  PAL"

# 16:9 video formats
add_format "1920 1080                    1.0   HD"
add_format " 720  486                    1.21  NTSC_16:9"
add_format " 720  576                    1.46  PAL_16:9"

# FILM FORMATS
add_format "1024 778                     1.0   1K_Super_35(full-ap)"
add_format "914 778                      2.0   1K_Cinemascope"

add_format "2048 1556                    1.0   2K_Super_35(full-ap)"
add_format "1828 1556                    2.0   2K_Cinemascope"

add_format "4096 3112                    1.0   4K_Super_35(full-ap)"
add_format "3656 3112                    2.0   4K_Cinemascope"

#add_format "2048 1558 220 284 2048 1272  1.0   2K_Academy_aperture"

#SQUARE FORMATS
add_format " 256  256                    1.0   square_256"
add_format " 512  512                    1.0   square_512"
add_format "1024 1024                    1.0   square_1K"
add_format "2048 2048                    1.0   square_2K"


