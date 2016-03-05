
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

def generateWing(obj):
    a= color([1,0,0])(polyhedron(points=obj.renderpoints[0],faces=obj.renderpoints[1]))
    return a
'''
def make(*args):
    final = args[0] # creates the first object as an OpenSCAD object.
    for i in range(1,len(args)):
        final = final + generateWing(args[i]) #creates a union of all the required wings
    return final

    # Adding the file_header argument as shown allows you to change
    # the detail of arcs by changing the SEGMENTS variable.  This can
    # be expensive when making lots of small curves, but is otherwise
    # useful.
'''

if __name__ == '__main__':

    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    file_out = os.path.join(out_dir, 'test.scad')

    # Simple command
    subprocess.call(['clear'], shell=True)
    subprocess.call('echo "Running the program"', shell=True)
    subprocess.call('echo "Running the program"', shell=True)


    #defining the required values of all wings
    canard = {  "rootChord":5,
                "tipChord":3,
                "span":10,
                "rootAngle":0,
                "tipAngle":3,
                "sweepAngle":2,
                "dihedralAngle":0,
                "attackAngle":0,
                "velocity":[0,-4,0],
                "airDensity": 1,
                "pos":[0,0,0],
                "flip":False,
                "thickness":1/16
    }
    canardReverse =  {  "rootChord":5,
                "tipChord":3,
                "span":10,
                "rootAngle":0,
                "tipAngle":3,
                "sweepAngle":2,
                "dihedralAngle":0,
                "attackAngle":0,
                "velocity":[0,-4,0],
                "airDensity": 1,
                "pos":[0,0,0],
                "flip":True,
                "thickness":1/16
    }

    # converting into GliderV2 wing objects
    canard = GliderV2.wing(canard)
    canardReverse = GliderV2.wing(canardReverse)

    # passing it to render to make the OpenSCAD file.
    a = generateWing(canard) + generateWing(canardReverse)

    scad_render_to_file(a, file_out)
    print("%(__file__)s: SCAD file written to: \n%(file_out)s" % vars())
