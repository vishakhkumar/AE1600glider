$fn = 480;

union() {
	union() {
		cube(size = [18, 0.2500000000, 0.2500000000]);
		translate(v = [3, 0, 0]) {
			rotate(a = [5, 0, 90]) {
				rotate(a = [0, 10, 0]) {
					linear_extrude(center = true, convexity = 0, height = 0.0625000000, twist = 0) {
						polygon(paths = [[0, 1, 2, 3]], points = [[0, 0], [-8, -0.8885280531], [-8, -1.8885280531], [0, -2]]);
					}
				}
				rotate(a = [0, -10, 0]) {
					linear_extrude(center = true, convexity = 0, height = 0.0625000000, twist = 0) {
						polygon(paths = [[0, 1, 2, 3]], points = [[0, 0], [8, -0.8885280531], [8, -1.8885280531], [0, -2]]);
					}
				}
			}
		}
	}
	translate(v = [15, 0, 0]) {
		rotate(a = [5, 0, -90]) {
			rotate(a = [0, 10, 0]) {
				linear_extrude(center = true, convexity = 0, height = 0.0625000000, twist = 0) {
					polygon(paths = [[0, 1, 2, 3]], points = [[0, 0], [-3, 1.5036083501], [-3, 0.5036083501], [0, -1.5000000000]]);
				}
			}
			rotate(a = [0, -10, 0]) {
				linear_extrude(center = true, convexity = 0, height = 0.0625000000, twist = 0) {
					polygon(paths = [[0, 1, 2, 3]], points = [[0, 0], [3, 1.5036083501], [3, 0.5036083501], [0, -1.5000000000]]);
				}
			}
		}
	}
}
/***********************************************
*********      SolidPython code:      **********
************************************************
 
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

def glider(canardWingSpan,canardWingTipChord,canardWingRootChord,canardWingSweepAngle,canardWingDihedralAngle,canardWingXPos,canardWingAngleOfAttack,
           mainWingSpan,mainWingTipChord,mainWingRootChord,mainWingSweepAngle,mainWingDihedralAngle,mainWingXPos,mainWingAngleOfAttack,
           fuselageLength,fuselageWidth):

    def generateWing(Span,TipChord,RootChord,SweepAngle,DihedralAngle,flip):
        #forwardLeft = [0,0,0] #starts from the origin #forwardRight = [0+Span,0-Span/tan(SweepAngle),0]
        #backwardLeft = [0,0-RootChord,0] #backwardRight = [0+Span,0-Span/tan(SweepAngle)-TipChord,0]
        #linear_extrude(height = 1/16, center = true, convexity = 10, twist = 0)
        if flip == True:
            points=[[0,0],[0+Span,0-Span/math.tan(90-SweepAngle)],[0+Span,0-Span/math.tan(90-SweepAngle)-TipChord],[0,0-RootChord]]
        else:
            points=[[0,0],[0-Span,0-Span/math.tan(90-SweepAngle)],[0-Span,0-Span/math.tan(90-SweepAngle)-TipChord],[0,0-RootChord]]

        return polygon(points)

    #drawing the fuselage
    final = cube([fuselageLength,fuselageWidth,fuselageWidth])

    mainWings = translate([mainWingXPos,0,0])(
                     rotate([mainWingAngleOfAttack,0,90])
                        (
                        rotate([0,mainWingDihedralAngle,0])
                            (linear_extrude(1/16,True,0,0)
                                (generateWing(mainWingSpan,mainWingTipChord,mainWingRootChord,mainWingSweepAngle,mainWingDihedralAngle,False))),
                        rotate([0,-mainWingDihedralAngle,0])
                            (linear_extrude(1/16,True,0,0)
                                (generateWing(mainWingSpan,mainWingTipChord,mainWingRootChord,mainWingSweepAngle,mainWingDihedralAngle,True)))
                        ))

    canardWings = translate([canardWingXPos,0,0])(
                         rotate([canardWingAngleOfAttack,0,-90])
                            (
                            rotate([0,canardWingDihedralAngle,0])(linear_extrude(1/16,True,0,0)(generateWing(canardWingSpan,canardWingTipChord,canardWingRootChord,canardWingSweepAngle,canardWingDihedralAngle,False))),
                            rotate([0,-canardWingDihedralAngle,0])(linear_extrude(1/16,True,0,0)(generateWing(canardWingSpan,canardWingTipChord,canardWingRootChord,canardWingSweepAngle,canardWingDihedralAngle,True)))
                            ))

    #final = final + mainWings
    final = final + mainWings + canardWings
    return final

if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    file_out = os.path.join(out_dir, 'gliderFinal.scad')

    # for canard of aircraft
    canardWingSpan = 3
    canardWingTipChord = 1
    canardWingRootChord = 1.5
    canardWingSweepAngle = 0
    canardWingDihedralAngle = 10
    canardWingXPos = 15
    canardWingAngleOfAttack = 5

    #for Main wing of aircraft
    mainWingSpan = 8
    mainWingTipChord = 1
    mainWingRootChord = 2
    mainWingSweepAngle = 10
    mainWingDihedralAngle = 10
    mainWingXPos = 3 #Yes, yes, I know it's negative, big fucking brohaha.
    mainWingAngleOfAttack = 5

    # for fuselage of Aircraft
    fuselageLength = 18
    fuselageWidth = 0.25



    a = glider(canardWingSpan,canardWingTipChord,canardWingRootChord,
               canardWingSweepAngle,canardWingDihedralAngle,
               canardWingXPos,canardWingAngleOfAttack,
               mainWingSpan,mainWingTipChord,mainWingRootChord,
               mainWingSweepAngle,mainWingDihedralAngle,
               mainWingXPos,mainWingAngleOfAttack,
               fuselageLength,fuselageWidth)


    print("%(__file__)s: SCAD file written to: \n%(file_out)s" % vars())

    # Adding the file_header argument as shown allows you to change
    # the detail of arcs by changing the SEGMENTS variable.  This can
    # be expensive when making lots of small curves, but is otherwise
    # useful.
    scad_render_to_file(a, file_out, file_header='$fn = %s;' % SEGMENTS)
 
 
************************************************/
