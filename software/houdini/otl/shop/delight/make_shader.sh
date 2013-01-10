#!/bin/bash
shaderdl ${DELIGHT}/shaders/src/d_warunit.sl
cp d_warunit.sdl ${DELIGHT}/shaders/
sdl2otl.py -l shop_d_warunit.otl d_warunit.sdl
rm d_warunit.sdl