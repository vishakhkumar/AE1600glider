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

def glider(canardWingSpan,canardWingTipChord,canardWingRootChord,canardWingSweepAngle,canardWingDihedralAngle,canardWingYpos,canardWingAngleOfAttack,
           mainWingSpan,mainWingTipChord,mainWingRootChord,mainWingSweepAngle,mainWingDihedralAngle,mainWingYpos,mainWingAngleOfAttack,
           miniWingSpan,miniWingTipChord,miniWingRootChord,miniWingSweepAngle,miniWingDihedralAngle,miniWingYpos,miniWingAngleOfAttack,
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

    miniWings = translate([miniWingYpos,0,0])(
                     rotate([miniWingAngleOfAttack,0,90])
                        (
                        rotate([0,miniWingDihedralAngle,0])
                            (linear_extrude(1/16,True,0,0)
                                (generateWing(miniWingSpan,miniWingTipChord,miniWingRootChord,miniWingSweepAngle,miniWingDihedralAngle,False))),
                        rotate([0,-miniWingDihedralAngle,0])
                            (linear_extrude(1/16,True,0,0)
                                (generateWing(miniWingSpan,miniWingTipChord,miniWingRootChord,miniWingSweepAngle,miniWingDihedralAngle,True)))
                        ))


    mainWings = translate([mainWingYpos,0,0])(
                     rotate([mainWingAngleOfAttack,0,90])
                        (
                        rotate([0,mainWingDihedralAngle,0])
                            (linear_extrude(1/16,True,0,0)
                                (generateWing(mainWingSpan,mainWingTipChord,mainWingRootChord,mainWingSweepAngle,mainWingDihedralAngle,False))),
                        rotate([0,-mainWingDihedralAngle,0])
                            (linear_extrude(1/16,True,0,0)
                                (generateWing(mainWingSpan,mainWingTipChord,mainWingRootChord,mainWingSweepAngle,mainWingDihedralAngle,True)))
                        ))

    canardWings = translate([canardWingYpos,0,0])(
                         rotate([canardWingAngleOfAttack,0,-90])
                            (
                            rotate([0,canardWingDihedralAngle,0])(linear_extrude(1/16,True,0,0)(generateWing(canardWingSpan,canardWingTipChord,canardWingRootChord,canardWingSweepAngle,canardWingDihedralAngle,False))),
                            rotate([0,-canardWingDihedralAngle,0])(linear_extrude(1/16,True,0,0)(generateWing(canardWingSpan,canardWingTipChord,canardWingRootChord,canardWingSweepAngle,canardWingDihedralAngle,True)))
                            ))

    #final = final + mainWings
    final = final + mainWings + canardWings + miniWings
    return final
def area(root,tip,length):
    return(root+tip)*length/2
def lift(liftcoefficient,density,velocity,area,angleofattack,dihedralangle):
    return liftcoefficient*density*velocity*velocity*area*math.cos(angleofattack)*math.cos(dihedralangle)/2
def drag(dragcoefficient,density,velocity,area,angleofattack,dihedralangle):
    return dragcoefficient*density*velocity*velocity*area*math.cos(angleofattack)/2
def centerY(root,tip,length,sweptangle):
    return root/2 + (length*math.tan(sweptangle) + (tip - root)/2)*(2*tip + root)/(3*(tip+root))
def momentOfForceXTypeOne(lift,root,tip,length):
    return lift*(length*(root + 2*tip)/(3*(root+tip)))
def momentOfForceXTypeTwo(lift,root,tip,length,main_root,main_tip,main_length):
    return lift*(2*main_length*(main_root+2*main_tip)/(3*(main_root+main_tip)) + length*(root + 2*tip)/(3*(root+tip)))
def stabilityInY(areaTypeOne,areaTypeTwo,areaTypeThree,liftTypeOne,liftTypeTwo,liftTypeThree,YposOne,YposTwo,YposThree,centerYOne,centerYTwo,centerYThree):
    centerOfGravity = (areaTypeOne*(YposOne + centerYOne) + areaTypeTwo*(YposTwo + centerYTwo) + areaTypeThree*(YposThree + centerYThree))/(areaTypeOne+areaTypeTwo+areaTypeThree)
    centerOfLift    = (liftTypeOne*(YposOne + centerYOne) + liftTypeTwo*(YposTwo + centerYTwo) + liftTypeThree*(YposThree + centerYThree))/(liftTypeOne+liftTypeTwo+liftTypeThree)
    return centerOfLift - centerOfGravity
def TotalFunc(listE):
        # do this stuff now :)

    liftWeight = 0.2
    dragWeight = 0.2
    stabilityWeight = 2
    YstabilityWeight = 2
    weightWeight = 0.4
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
    weight = (area(listE[7],listE[6],listE[5])+area(listE[7+7],listE[6+7],listE[5+7])+area(listE[7+7+7],listE[6+7+7],listE[5+7+7]))*0.25*2*0.207 + listE[27]*listE[26]*listE[27]*0.207

    total = (liftWeight*sumLift) - (dragWeight*sumdrag) + 0.1*stabilityWeight*sumStability + 0.1*YstabilityWeight*StabY - weight*weightWeight

    if (sumdrag <0):
        print("sumdrag is less than zero")
    if (weight <0):
            print("weight is less than zero")





    return total

    # use as reference
def printDescription(WingDesc):
    print('\n\n\n')
    print ('aircraftWingSpan'+" "+str(WingDesc['aircraftWingSpan']))
    print ('density'+" "+str(WingDesc['density']))
    print ('velocity'+" "+str(WingDesc['velocity']))
    print ('liftcoefficient'+" "+str(WingDesc['liftcoefficient']))
    print ('dragcoefficient'+" "+str(WingDesc['dragcoefficient']))
    print('\n\n\n')
    print ('canardWingSpan'+" "+str(WingDesc['canardWingSpan']))
    print ('canardWingTipChord'+" "+str(WingDesc['canardWingTipChord']))
    print ('canardWingRootChord'+" "+str(WingDesc['canardWingRootChord']))
    print ('canardWingSweepAngle'+" "+str(WingDesc['canardWingSweepAngle']))
    print ('canardWingDihedralAngle'+" "+str(WingDesc['canardWingDihedralAngle']))
    print ('canardWingYpos'+" "+str(WingDesc['canardWingYpos']))
    print ('canardWingAngleOfAttack'+" "+str(WingDesc['canardWingAngleOfAttack']))
    print('\n\n\n')
    print ('mainWingSpan'+" "+str(WingDesc['mainWingSpan']))
    print ('mainWingTipChord'+" "+str(WingDesc['mainWingTipChord']))
    print ('mainWingRootChord'+" "+str(WingDesc['mainWingRootChord']))
    print ('mainWingSweepAngle'+" "+str(WingDesc['mainWingSweepAngle']))
    print ('mainWingDihedralAngle'+" "+str(WingDesc['mainWingDihedralAngle']))
    print ('mainWingYpos'+" "+str(WingDesc['mainWingYpos']))
    print ('mainWingAngleOfAttack'+" "+str(WingDesc['mainWingAngleOfAttack']))
    print('\n\n\n')
    print ('miniWingSpan'+" "+str(WingDesc['miniWingSpan']))
    print ('miniWingTipChord'+" "+str(WingDesc['miniWingTipChord']))
    print ('miniWingRootChord'+" "+str(WingDesc['miniWingRootChord']))
    print ('miniWingSweepAngle'+" "+str(WingDesc['miniWingSweepAngle']))
    print ('miniWingDihedralAngle'+" "+str(WingDesc['miniWingDihedralAngle']))
    print ('miniWingYpos'+" "+str(WingDesc['miniWingYpos']))
    print ('miniWingAngleOfAttack'+" "+str(WingDesc['miniWingAngleOfAttack']))
    print('\n\n\n')
    print ('fuselageLength'+" "+str(WingDesc['fuselageLength']))
    print ('fuselageWidth'+" "+str(WingDesc['fuselageWidth']))
def derivative(func,listOfVariablesToBeOptimized,i):
    oldX = listOfVariablesToBeOptimized
    Xi = func(oldX)
    newX = listOfVariablesToBeOptimized

    deltaX = 0.1
    newX[i] = newX[i]+ deltaX

    Xf = func(newX)

    newX[i] = newX[i]- deltaX

    der = (Xf-Xi)/deltaX

    return round(der,2)



if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    file_out = os.path.join(out_dir, 'gliderFinal.scad')

    # just general information - unchangeable
    numberOfIterations = 10000
    liftWeight = 0.4
    dragWeight = 0.4
    stabilityWeight = 0.15
    YstabilityWeight = 0.05
    aircraftWingSpan = 8
    density = 1
    velocity = 1
    liftcoefficient = 0.45
    dragcoefficient = 0.18
    # for canard of aircraft
    canardWingSpan = 3
    canardWingTipChord = 1
    canardWingRootChord = 1.5
    canardWingSweepAngle = -10    *math.pi/180
    canardWingDihedralAngle = 10*math.pi/180
    canardWingYpos = 15
    canardWingAngleOfAttack = 5 *math.pi/180
    #for Main wing of aircraft
    mainWingSpan = 5
    mainWingTipChord = 1
    mainWingRootChord = 2
    mainWingSweepAngle = -10     *math.pi/180
    mainWingDihedralAngle = 10  *math.pi/180
    mainWingYpos = 3
    mainWingAngleOfAttack = 5   *math.pi/180
    #for Mini wing of aircraft.
    miniWingSpan = aircraftWingSpan - mainWingSpan
    miniWingTipChord = 1
    miniWingRootChord = 2
    miniWingSweepAngle = -10     *math.pi/180
    miniWingDihedralAngle = 10  *math.pi/180
    miniWingYpos = 3
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
         canardWingYpos,
         canardWingAngleOfAttack,
         mainWingSpan,
         mainWingTipChord,
         mainWingRootChord,
         mainWingSweepAngle,
         mainWingDihedralAngle,
         mainWingYpos,
         mainWingAngleOfAttack,
         miniWingSpan,
         miniWingTipChord,
         miniWingRootChord,
         miniWingSweepAngle,
         miniWingDihedralAngle,
         miniWingYpos,
         miniWingAngleOfAttack,
         fuselageLength,
         fuselageWidth
    ]

    # repeat for number of iterations
    for j in range(numberOfIterations):
    # add stuff to each variable
        for i in range(5,len(listOfVariablesToBeOptimized)-2):
            if i in [5]:
                continue
            x = derivative(TotalFunc,listOfVariablesToBeOptimized, i)
            if listOfVariablesToBeOptimized[i] < 0:
                listOfVariablesToBeOptimized[i] = 0
            if x > 0:
                listOfVariablesToBeOptimized[i] = listOfVariablesToBeOptimized[i] + 0.000001
            elif x<0:
                listOfVariablesToBeOptimized[i] = listOfVariablesToBeOptimized[i] + 0.000001
            listOfVariablesToBeOptimized[19] =  aircraftWingSpan - listOfVariablesToBeOptimized[19-7]
            if i == 13:
                listOfVariablesToBeOptimized[13] = listOfVariablesToBeOptimized[21]
            #listOfVariablesToBeOptimized = list(map(lambda x: round(x,3),listOfVariablesToBeOptimized))
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
                 canardWingYpos,                11
                 canardWingAngleOfAttack,       12

                 mainWingSpan,                  13
                 mainWingTipChord,              14
                 mainWingRootChord,             15
                 mainWingSweepAngle,            16
                 mainWingDihedralAngle,         17
                 mainWingYpos,                  18
                 mainWingAngleOfAttack,         19

                 miniWingSpan,                  20
                 miniWingTipChord,              21
                 miniWingRootChord,             22
                 miniWingSweepAngle,            23
                 miniWingDihedralAngle,         24
                 miniWingYpos,                  25
                 miniWingAngleOfAttack,         26
                 fuselageLength,                27
                 fuselageWidth                  28
            ]
        '''
    # time to stop our satanic rituals.
    # after all this rubbish is complete, we can then use this piece of crap in
    # solidpython to render it in actual 3d :)
    WingDesc = {
        'aircraftWingSpan'       :listOfVariablesToBeOptimized[0],
        'density'                :listOfVariablesToBeOptimized[1],
        'velocity'               :listOfVariablesToBeOptimized[2],
        'liftcoefficient'        :listOfVariablesToBeOptimized[3],
        'dragcoefficient'        :listOfVariablesToBeOptimized[4],
        'canardWingSpan'         :listOfVariablesToBeOptimized[5],
        'canardWingTipChord'     :listOfVariablesToBeOptimized[6],
        'canardWingRootChord'    :listOfVariablesToBeOptimized[7],
        'canardWingSweepAngle'   :listOfVariablesToBeOptimized[8]*180/math.pi,
        'canardWingDihedralAngle':listOfVariablesToBeOptimized[9]*180/math.pi,
        'canardWingYpos'         :listOfVariablesToBeOptimized[10],
        'canardWingAngleOfAttack':listOfVariablesToBeOptimized[11]*180/math.pi,
        'mainWingSpan'           :listOfVariablesToBeOptimized[12],
        'mainWingTipChord'       :listOfVariablesToBeOptimized[13],
        'mainWingRootChord'      :listOfVariablesToBeOptimized[14],
        'mainWingSweepAngle'     :listOfVariablesToBeOptimized[15]*180/math.pi,
        'mainWingDihedralAngle'  :listOfVariablesToBeOptimized[16]*180/math.pi,
        'mainWingYpos'           :listOfVariablesToBeOptimized[17],
        'mainWingAngleOfAttack'  :listOfVariablesToBeOptimized[18]*180/math.pi,
        'miniWingSpan'           :listOfVariablesToBeOptimized[19],
        'miniWingTipChord'       :listOfVariablesToBeOptimized[20],
        'miniWingRootChord'      :listOfVariablesToBeOptimized[21],
        'miniWingSweepAngle'     :listOfVariablesToBeOptimized[22]*180/math.pi,
        'miniWingDihedralAngle'  :listOfVariablesToBeOptimized[23]*180/math.pi,
        'miniWingYpos'           :listOfVariablesToBeOptimized[24],
        'miniWingAngleOfAttack'  :listOfVariablesToBeOptimized[25]*180/math.pi,
        'fuselageLength'         :listOfVariablesToBeOptimized[26],
        'fuselageWidth'          :listOfVariablesToBeOptimized[27]
        }

    printDescription(WingDesc)

    print('\n\n\n\n')
    print(WingDesc['canardWingAngleOfAttack'])
    print(WingDesc['mainWingAngleOfAttack'])
    print(WingDesc['miniWingAngleOfAttack'])
    print('\n\n\n\n')
    print(WingDesc['canardWingDihedralAngle'])
    print(WingDesc['mainWingDihedralAngle'])
    print(WingDesc['miniWingDihedralAngle'])
    print('\n\n\n\n')
    print(WingDesc['canardWingSweepAngle'])
    print(WingDesc['mainWingSweepAngle'])
    print(WingDesc['miniWingSweepAngle'])


    a = glider(canardWingSpan,canardWingTipChord,canardWingRootChord,canardWingSweepAngle,canardWingDihedralAngle,canardWingYpos,canardWingAngleOfAttack,
               mainWingSpan,mainWingTipChord,mainWingRootChord,mainWingSweepAngle,mainWingDihedralAngle,mainWingYpos,mainWingAngleOfAttack,
               miniWingSpan,miniWingTipChord,miniWingRootChord,miniWingSweepAngle,miniWingDihedralAngle,miniWingYpos,miniWingAngleOfAttack,
               fuselageLength,fuselageWidth)


    print("%(__file__)s: SCAD file written to: \n%(file_out)s" % vars())

    # Adding the file_header argument as shown allows you to change
    # the detail of arcs by changing the SEGMENTS variable.  This can
    # be expensive when making lots of small curves, but is otherwise
    # useful.
    scad_render_to_file(a, file_out, file_header='$fn = %s;' % SEGMENTS)
