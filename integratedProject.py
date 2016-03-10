
#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import division
import os
import sys
import re
from solid import *
import solid.utils
import math
SEGMENTS = 480
import GliderV2
import subprocess
import Menu


# Program Constants

noOfIterations = 10000





if __name__ == '__main__':

    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    out_dir = '/Users/vishakhkumar/Desktop/.'
    file_out = os.path.join(out_dir, 'test.scad')
    subprocess.call(['clear'], shell=True)

    #Use only when program is complete
    #Menu.startUpMenu()

    # Simple command
    subprocess.call(['clear'], shell=True)
    subprocess.call('echo "Running the program"', shell=True)
    # subprocess.call('say "Running the program"', shell=True)


    #defining the required values of all wings
    parts = [
        GliderV2.wing({"rootChord":5,
        "tipChord":3,
        "span":10,
        "rootAngle":0,
        "tipAngle":3,
        "sweepAngle":2,
        "dihedralAngle":10,
        "attackAngle":5,
        "velocity":[0,-4,0],
        "airDensity": 1,
        "pos":[1,0,0],
        "flip":False,
        "thickness":1/16,
        "density":0.5}),
        GliderV2.wing({"rootChord":5,
        "tipChord":3,
        "span":10,
        "rootAngle":0,
        "tipAngle":3,
        "sweepAngle":2,
        "dihedralAngle":10,
        "attackAngle":5,
        "velocity":[0,-4,0],
        "airDensity": 1,
        "pos":[1,0,0],
        "flip":True,
        "thickness":1/16,
        "density":0.5}),
        '''
        GliderV2.wing({"rootChord":2,
        "tipChord":1,
        "span":5,
        "rootAngle":0,
        "tipAngle":3,
        "sweepAngle":2,
        "dihedralAngle":20,
        "attackAngle":5,
        "velocity":[0,-4,0],
        "airDensity": 1,
        "pos":[1,7,0],
        "flip":False,
        "thickness":1/16,
        "density":0.5}),
        GliderV2.wing({"rootChord":2,
        "tipChord":1,
        "span":5,
        "rootAngle":0,
        "tipAngle":3,
        "sweepAngle":2,
        "dihedralAngle":20,
        "attackAngle":5,
        "velocity":[0,-4,0],
        "airDensity": 1,
        "pos":[1,7,0],
        "flip":True,
        "thickness":1/16,
        "density":0.5}),
        '''

            ]

    # converting into GliderV2 wing objects
    final = GliderV2.glider(parts)

    print((final.components[0]).velocity)
    print((final.components[0]).pos)
    print('\n\n')





    scad_render_to_file(final.OpenSCAD_obj, file_out)
    #subprocess.call("/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD "+file_out, shell=True)

    for i in range(noOfIterations):
        final.update()
        scad_render_to_file(final.OpenSCAD_obj, file_out)

    actualFinal = final.OpenSCAD_obj
    scad_render_to_file(actualFinal, file_out)




    print((final.components[0]).velocity)
    print((final.components[0]).pos)



    #print("%(__file__)s: SCAD file written to: \n%(file_out)s" % vars())


    subprocess.call("/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD "+file_out, shell=True)


    Menu.endProgram()
