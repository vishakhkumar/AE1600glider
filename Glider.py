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

def area(root,tip,length):
    return(root+tip)*length/2
def lift(liftcoefficient,density,velocity,area,angleofattack,dihedralangle):
    return liftcoefficient*density*velocity*velocity*area*math.cos(angleofattack)*math.cos(dihedralangle)/2
def drag(dragcoefficient,density,velocity,area,angleofattack,dihedralangle):
    return dragcoefficient*density*velocity*velocity*area*math.cos(angleofattack)*math.cos(dihedralangle)/2
def centerY(root,tip,length,sweptangle):
    return root/2 + (length*math.tan(sweptangle) + (tip - root)/2)*(2*tip + root)/(3*(tip+root))
def momentOfForceXTypeOne(lift,root,tip,length):
    return lift*(length*(root + 2*tip)/(3*(root+tip)))
def momentOfForceXTypeTwo(lift,root,tip,length,main_root,main_tip,main_length):
    return lift*(2*main_length*(main_root+2*main_tip)/(3*(main_root+main_tip)) + length*(root + 2*tip)/(3*(root+tip)))
def stabilityInY(areaTypeOne,areaTypeTwo,areaTypeThree,liftTypeOne,liftTypeTwo,liftTypeThree,YPosOne,YPosTwo,YPosThree,centerYOne,centerYTwo,centerYThree):
    centerOfGravity = (areaTypeOne*(YPosOne + centerYOne) + areaTypeTwo*(YPosTwo + centerYTwo) + areaTypeThree*(YPosThree + centerYThree))/(areaTypeOne+areaTypeTwo+areaTypeThree)
    centerOfLift    = (liftTypeOne*(YPosOne + centerYOne) + liftTypeTwo*(YPosTwo + centerYTwo) + liftTypeThree*(YPosThree + centerYThree))/(liftTypeOne+liftTypeTwo+liftTypeThree)
    return centerOfLift - centerOfGravity

def TotalFunc(listE):
        # do this stuff now :)
    global liftWeight
    global dragWeight
    global stabilityWeight
    global YstabilityWeight

    sumLift = 0
    sumdrag = 0
    sumStability = 0

    temp1 =  lift(listE[3],listE[1],listE[2],area(listE[7],listE[6],listE[5]),listE[11],listE[9]) # canardWings
    sumLift = sumLift + temp1
    sumStability = sumStability + momentOfForceXTypeOne(temp1,listE[7],listE[6],listE[5])

    temp2 =  lift(listE[3],listE[1],listE[2],area(listE[7+7],listE[6+7],listE[5+7]),listE[11+7],listE[9+7]) # mainWings
    sumLift = sumLift + temp2
    sumStability = sumStability + momentOfForceXTypeOne(temp2,listE[7+7],listE[6+7],listE[5+7])

    temp3 =  lift(listE[3],listE[1],listE[2],area(listE[7+7+7],listE[6+7+7],listE[5+7+7]),listE[11+7+7],listE[9+7+7]) # miniWings
    sumLift = sumLift + temp3
    sumStability = sumStability + momentOfForceXTypeTwo(temp3,listE[7+7+7],listE[6+7+7],listE[5+7+7],listE[7+7],listE[6+7],listE[5+7])

    sumdrag = sumdrag + drag(listE[4],listE[1],listE[2],area(listE[7],listE[6],listE[5]),listE[11],listE[9]) # canardWings
    sumdrag = sumdrag + drag(listE[4],listE[1],listE[2],area(listE[7+7],listE[6+7],listE[5+7]),listE[11+7],listE[9+7]) # mainWings
    sumdrag = sumdrag + drag(listE[4],listE[1],listE[2],area(listE[7+7+7],listE[6+7+7],listE[5+7+7]),listE[11+7+7],listE[9+7+7]) # miniWings


    sumLift = sumLift*2
    sumdrag = sumdrag*2
    sumStability = sumStability * 2
    StabY = stabilityInY(area(listE[7],listE[6],listE[5]),area(listE[7+7],listE[6+7],listE[5+7]),area(listE[7+7+7],listE[6+7+7],listE[5+7+7]),temp1,temp2,temp3,listE[10],listE[10],listE[10],centerY(listE[7],listE[6],listE[5],listE[8]),centerY(listE[7+7],listE[6+7],listE[5+7],listE[8+7]),centerY(listE[7+7+7],listE[6+14],listE[5+14],listE[8+14]))

    #print(sumLift)
    #print(sumdrag)
    #print(sumStability)
    #print(StabY)

    total = (liftWeight*sumLift)/(dragWeight*sumdrag) + 0.001*stabilityWeight*sumStability + 0.001*YstabilityWeight*StabY

    return total

    # use as reference
    '''
        listOfVariablesToBeOptimized = [
             aircraftWingSpan,              1
             density,                       2
             velocity,                      3
             liftcoefficient,               4
             dragcoefficient,               5

             canardWingSpan,                6
             canardWingTipChord,            7
             canardWingRootChord,           8
             canardWingSweepAngle,          9
             canardWingDihedralAngle,       10
             canardWingYPos,                11
             canardWingAngleOfAttack,       12

             mainWingSpan,                  13
             mainWingTipChord,              14
             mainWingRootChord,             15
             mainWingSweepAngle,            16
             mainWingDihedralAngle,         17
             mainWingYPos,                  18
             mainWingAngleOfAttack,         19

             miniWingSpan,                  20
             miniWingTipChord,              21
             miniWingRootChord,             22
             miniWingSweepAngle,            23
             miniWingDihedralAngle,         24
             miniWingYPos,                  25
             miniWingAngleOfAttack,         26
             fuselageLength,                27
             fuselageWidth                  28
        ]
    '''



def derivative(func,listOfVariablesToBeOptimized,i):
    oldX = listOfVariablesToBeOptimized
    newX = listOfVariablesToBeOptimized
    newX[i] = newX[i]+ 0.1

    der = (func(newX) - func(oldX))/0.1

    return der




if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    file_out = os.path.join(out_dir, 'gliderFinal.scad')

    # just general information - unchangeable
    numberOfIterations = 1000
    liftWeight = 0.4
    dragWeight = 0.4
    stabilityWeight = 0.15
    YstabilityWeight = 0.05

    aircraftWingSpan = 8
    density = 1
    velocity = 1
    liftcoefficient = 0.45
    dragcoefficient = 0.45
    # for canard of aircraft
    canardWingSpan = 3
    canardWingTipChord = 1
    canardWingRootChord = 1.5
    canardWingSweepAngle = 0    *math.pi/180
    canardWingDihedralAngle = 10*math.pi/180
    canardWingYPos = 15
    canardWingAngleOfAttack = 5 *math.pi/180
    #for Main wing of aircraft
    mainWingSpan = 5
    mainWingTipChord = 1
    mainWingRootChord = 2
    mainWingSweepAngle = 10     *math.pi/180
    mainWingDihedralAngle = 10  *math.pi/180
    mainWingYPos = 3
    mainWingAngleOfAttack = 5   *math.pi/180
    #for Mini wing of aircraft.
    miniWingSpan = aircraftWingSpan - mainWingSpan
    miniWingTipChord = 1
    miniWingRootChord = 2
    miniWingSweepAngle = 10     *math.pi/180
    miniWingDihedralAngle = 10  *math.pi/180
    miniWingYPos = 3
    miniWingAngleOfAttack = 5   *math.pi/180
    # for fuselage of Aircraft
    fuselageLength = 18
    fuselageWidth = 0.25


    listOfVariablesToBeOptimized = [

         aircraftWingSpan,
         density,
         velocity,
         liftcoefficient,
         dragcoefficient,
         canardWingSpan,
         canardWingTipChord,
         canardWingRootChord,
         canardWingSweepAngle,
         canardWingDihedralAngle,
         canardWingYPos,
         canardWingAngleOfAttack,
         mainWingSpan,
         mainWingTipChord,
         mainWingRootChord,
         mainWingSweepAngle,
         mainWingDihedralAngle,
         mainWingYPos,
         mainWingAngleOfAttack,
         miniWingSpan,
         miniWingTipChord,
         miniWingRootChord,
         miniWingSweepAngle,
         miniWingDihedralAngle,
         miniWingYPos,
         miniWingAngleOfAttack,
         fuselageLength,
         fuselageWidth
    ]

    # repeat for number of iterations

    for j in range(numberOfIterations):
    # add stuff to each variable
        for i in range(5,len(listOfVariablesToBeOptimized)-2):
            if i in [19,5,7,6]:
                continue


            x = derivative(TotalFunc,listOfVariablesToBeOptimized, i)
            if x > 0:
                listOfVariablesToBeOptimized[i] = listOfVariablesToBeOptimized[i] + 0.1
            elif x < 0:
                listOfVariablesToBeOptimized[i] = listOfVariablesToBeOptimized[i] - 0.1
            listOfVariablesToBeOptimized[19] =  aircraftWingSpan - listOfVariablesToBeOptimized[19-7]

    # time to stop our satanic rituals.
    # after all this rubbish is complete, we can then use this piece of crap in
    # solidpython to render it in actual 3d :)


    print(listOfVariablesToBeOptimized)


'''

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

    '''
