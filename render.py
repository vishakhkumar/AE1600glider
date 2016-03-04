#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import division
import os
import sys
import re
from solid import *
import solid.utils
import math
SEGMENTS = 48000


def make(*args):
    final = args[0] # creates the first object as an OpenSCAD object.
    for i in range(1,len(args)):
        finals = finals + generateWing(args[i]) #creates a union of all the required wings
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    file_out = os.path.join(out_dir, 'gliderFinal.scad')


    print("%(__file__)s: SCAD file written to: \n%(file_out)s" % vars())

    # Adding the file_header argument as shown allows you to change
    # the detail of arcs by changing the SEGMENTS variable.  This can
    # be expensive when making lots of small curves, but is otherwise
    # useful.
    scad_render_to_file(final, file_out, file_header='$fn = %s;' % SEGMENTS)

def generateWing(obj):
    a= color([1,0,0])(polyhedron(points=obj.renderpoints[0],faces=renderpoints[1]))
    return a
