
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


def generateWing(obj):
    a = color([1,0,0])(polyhedron(points=obj.renderpoints[0],faces=obj.renderpoints[1]))
    return a

if __name__ == '__main__':

    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    out_dir = '/Users/vishakhkumar/Desktop/.'
    file_out = os.path.join(out_dir, 'test.scad')


    # Use only when program is complete
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
    "rootAngle":10,
    "tipAngle":3,
    "sweepAngle":2,
    "dihedralAngle":10,
    "attackAngle":5,
    "velocity":[0,-4,0],
    "airDensity": 1,
    "pos":[0,0,0],
    "flip":False,
    "thickness":1/16,
    "density":0.5})
    ]
    # converting into GliderV2 wing objects

    final = GliderV2.glider(parts)
    print(final.components[0].area)

    print(final.weight)

    '''
        final = (wing(parts[0]).OpenSCAD_obj)

        for i in range(1,len(parts)):
            final = final + (wing(parts[i]).OpenSCAD_obj)

        scad_render_to_file(final, file_out)
        #print("%(__file__)s: SCAD file written to: \n%(file_out)s" % vars())


        subprocess.call("/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD "+file_out, shell=True)
    '''



    print("\n Created by Vishakh Pradeep Kumar 2016. \n Email: vkumar@gatech.edu \n\n")
    subprocess.call('echo "End of program"', shell=True)


























    ########                Deep Storage
    ###########################################################################
    #
    #   Values for canard reverse.
    ''',
    {"rootChord":5,
    "tipChord":3,
    "span":10,
    "rootAngle":100,
    "tipAngle":3,
    "sweepAngle":2,
    "dihedralAngle":10,
    "attackAngle":5,
    "velocity":[0,-4,0],
    "airDensity": 1,
    "pos":[0,0,0],
    "flip":True,
    "thickness":1/16,
    "density":0.5}
    '''
    #
