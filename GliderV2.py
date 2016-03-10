__author__ = 'Vishakh Kumar'


# Whenever we deal with 3-D values, we will mention it just so that you remember.
# These values will be numpy.array types.




import collections
import math
from math import cos
from math import sin
from math import tan
import numpy as np
from itertools import product
import os
import sys
import re
from solid import *
import solid.utils
import math

#number of wing parameters. Refer generateWing for list of parameters.
wingParameters = 14
stallAngle = 5   * math.pi /180

def multiply(matr_a, matr_b):
    """Return product of an MxP matrix A with an PxN matrix B."""
    cols, rows = len(matr_b[0]), len(matr_b)
    resRows = range(len(matr_a))
    rMatrix = [[0] * cols for _ in resRows]
    for idx in resRows:
        for j, k in product(range(cols), range(rows)):
            rMatrix[idx][j] += matr_a[idx][k] * matr_b[k][j]
    return rMatrix
def rotation(a,x,y,z):
    X = [ [1,0,0],
          [0,cos(x),-sin(x)],
          [0,sin(x),cos(x)]
        ]
    Y = [ [cos(y),0,sin(y)],
          [0,1,0],
          [-sin(y),0,cos(y)]
        ]
    Z = [
          [cos(z),-sin(z),0],
          [sin(z),cos(z),0],
          [0,0,1]
        ]
    A = [
          [a[0]],
          [a[1]],
          [a[2]]
        ]
    ANS = multiply(multiply(Z,Y),multiply(X,A))
    return [ANS[0][0],ANS[1][0],ANS[2][0]]
def point(a,x,y,z,pos):
    X = [ [1,0,0],
          [0,cos(x),-sin(x)],
          [0,sin(x),cos(x)]
        ]
    Y = [ [cos(y),0,sin(y)],
          [0,1,0],
          [-sin(y),0,cos(y)]
        ]
    Z = [
          [cos(z),-sin(z),0],
          [sin(z),cos(z),0],
          [0,0,1]
        ]
    A = [
          [a[0]],
          [a[1]],
          [a[2]]
        ]
    ANS = multiply(multiply(Z,Y),multiply(X,A))
    a = [ANS[0][0],ANS[1][0],ANS[2][0]]
    if len(a)!=len(pos):
        return None
    else:
        for i in range(len(a)):
            a[i] = a[i] + pos[i]
        return a

class wing(object):
    def __init__(self,d):
        # the unchanged values are your basic information. They WILL be changed over and over again.
        self.isWing = True
        # these values are inputed directly
        self.rootChord = d["rootChord"]
        self.tipChord = d["tipChord"]
        self.span = d["span"]
        self.velocity = d["velocity"]
        self.airDensity = d["airDensity"]
        self.pos = d["pos"]
        # quantities that are modified slightly.
        self.rootAngle = d["rootAngle"]*math.pi/180
        self.tipAngle = d["tipAngle"]*math.pi/180
        self.sweepAngle = d["sweepAngle"]*math.pi/180
        self.dihedralAngle = d["dihedralAngle"]*math.pi/180
        self.attackAngle = d["attackAngle"]*math.pi/180
        # quantities that are basic but do not change.
        self.flip = (lambda flip : (-1)**(flip*1+1))(d["flip"])
        self.thickness = d["thickness"]
        self.density = d["density"]

        #just modifying a little
        self.pos[0] = self.flip*self.pos[0]
        self.dihedralAngle = self.dihedralAngle*self.flip

        # all derived quantities
        # try not to mess around with the points. They tend to be finicky.
        self.p1 = ( lambda a,x,y,z,pos:point(a,x,y,z,pos)    )( np.array([self.flip,1,1])*np.array([0,0,0])                                                                                                                                                                   ,0,-self.dihedralAngle,0,   np.array([self.pos[0],self.pos[1],self.pos[2]])           )
        self.p2 = ( lambda a,x,y,z,pos:point(a,x,y,z,pos)    )( np.array([self.flip,1,1])*np.array([self.span/cos(self.dihedralAngle),self.span*tan(self.attackAngle)/cos(self.dihedralAngle),0])                                                                             ,0,-self.dihedralAngle,0,   np.array([self.pos[0],self.pos[1],self.pos[2]])           )
        self.p3 = ( lambda a,x,y,z,pos:point(a,x,y,z,pos)    )( np.array([self.flip,1,1])*np.array([(self.span/cos(self.dihedralAngle)-self.tipChord*cos(self.tipAngle)),self.span*tan(self.attackAngle)/cos(self.dihedralAngle)+self.tipChord*cos(self.tipAngle),0 ])        ,0,-self.dihedralAngle,0,   np.array([self.pos[0],self.pos[1],self.pos[2]])           )
        self.p4 = ( lambda a,x,y,z,pos:point(a,x,y,z,pos)    )( np.array([self.flip,1,1])*np.array([(self.rootChord*sin(self.rootAngle)),self.rootChord*cos(self.rootAngle),0])                                                                                               ,0,-self.dihedralAngle,0,   np.array([self.pos[0],self.pos[1],self.pos[2]])           )

        self.centroid = (lambda x: x)(np.array([   (self.p1[0]+self.p2[0]+self.p3[0]+self.p4[0])/4,    (self.p1[1]+self.p2[1]+self.p3[1]+self.p4[1])/4,    (self.p1[2]+self.p2[2]+self.p3[2]+self.p4[2])/4 ]))
        #self.area = (lambda p1,p2,p3,p4: 0.5*abs(np.linalg.norm(np.cross(np.array([p2[0]-p1[0],p2[1]-p1[1],p2[2]-p1[2]],[p4[0]-p1[0],p4[1]-p1[1],p4[2]-p1[2]])))) +0.5*abs(np.linalg.norm(np.cross(np.array([p3[0]-p1[0],p3[1]-p1[1],p3[2]-p1[2]],[p4[0]-p1[0],p4[1]-p1[1],p4[2]-p1[2]])))))(self.p1,self.p2,self.p3,self.p4)
        self.area = 5
        #self.liftCoefficient = (lambda x: 2*math.pi*x)(self.attackAngle)
        # NOTE: need to correct the conditions if angle of attack exceeds stall angle
        #self.dragCoefficient = (lambda x: 1.28*sin(x))(self.attackAngle)


        self.lift = np.array([0,0,1])
        #self.lift = (lambda a,x,y,z:rotation(a,x,y,z))([0,0,(lambda airDensity,velocity,liftCoefficient,area :abs(airDensity*np.linalg.norm(velocity)*np.linalg.norm(velocity)*liftCoefficient*area/2))(self.airDensity,self.velocity,self.liftCoefficient,self.area)],self.dihedralAngle,self.attackAngle,0)
        # lift is always perpendicular to the wing surface, regardless of other angles.
        self.drag = np.array([0,1,0])
        #self.drag = (lambda a,x,y,z:rotation(a,x,y,z))([0,(lambda airDensity,velocity,dragCoefficient,area :abs(airDensity*np.linalg.norm(velocity)*np.linalg.norm(velocity)*liftCoefficient*area/2))(self.airDensity,self.velocity,self.dragCoefficient,self.area),0],self.dihedralAngle,self.attackAngle,0)
        # drag is always parallel to the wing surface, regardless of other angles.

        #renderpoints are called only by the render function. It's to satisfy the conditions of a polyhedron with six faces - two surfaces and the four edges of the balsa plank.
        #AX are the points that make the points ABOVE
        #BX are the points that make the points BELOW
        self.A1 = (lambda x,y: np.array([x[0]+y[0],x[1]+y[1],x[2]+y[2]]))(rotation([0,0,self.thickness/2],self.dihedralAngle,self.attackAngle,0),self.p1)
        self.B1 = (lambda x,y: np.array([x[0]+y[0],x[1]+y[1],x[2]+y[2]]))(rotation([0,0,-self.thickness/2],self.dihedralAngle,self.attackAngle,0),self.p1)
        self.A2 = (lambda x,y: np.array([x[0]+y[0],x[1]+y[1],x[2]+y[2]]))(rotation([0,0,self.thickness/2],self.dihedralAngle,self.attackAngle,0),self.p2)
        self.B2 = (lambda x,y: np.array([x[0]+y[0],x[1]+y[1],x[2]+y[2]]))(rotation([0,0,-self.thickness/2],self.dihedralAngle,self.attackAngle,0),self.p2)
        self.A3 = (lambda x,y: np.array([x[0]+y[0],x[1]+y[1],x[2]+y[2]]))(rotation([0,0,self.thickness/2],self.dihedralAngle,self.attackAngle,0),self.p3)
        self.B3 = (lambda x,y: np.array([x[0]+y[0],x[1]+y[1],x[2]+y[2]]))(rotation([0,0,-self.thickness/2],self.dihedralAngle,self.attackAngle,0),self.p3)
        self.A4 = (lambda x,y: np.array([x[0]+y[0],x[1]+y[1],x[2]+y[2]]))(rotation([0,0,self.thickness/2],self.dihedralAngle,self.attackAngle,0),self.p4)
        self.B4 = (lambda x,y: np.array([x[0]+y[0],x[1]+y[1],x[2]+y[2]]))(rotation([0,0,-self.thickness/2],self.dihedralAngle,self.attackAngle,0),self.p4)

        self.renderpoints = (lambda A1,A2,A3,A4,B1,B2,B3,B4: np.array([[A1.tolist(),A2.tolist(),A3.tolist(),A4.tolist(),B1.tolist(),B2.tolist(),B3.tolist(),B4.tolist()],
                             [[0,1,4,5],[1,3,7,4],[2,1,5,6],[2,3,7,6],[0,1,2,3],[4,5,6,7]]
                            ]).tolist())(self.A1,self.A2,self.A3,self.A4,self.B1,self.B2,self.B3,self.B4)

        self.volume = (lambda area, thickness: area*thickness)(
                       self.area,self.thickness)

        # quamtities that are likely to be called - kept last for safety.
        self.mass = (lambda volume,density: volume*density)(self.volume,self.density)
        self.centerOfGravity = (lambda centroid:centroid)(self.centroid)

        self.OpenSCAD_obj = (lambda renderpoints: polyhedron(points=renderpoints[0],faces=renderpoints[1]))(self.renderpoints)

class glider(object):
    def __init__(self,components):
        self.components = components
        # 3-D
        self.lift   = (lambda components:        np.sum([i.lift    for i in components],axis=0)        )(self.components)
        # 3-D
        self.drag   = (lambda components:        np.sum([i.drag    for i in components],axis=0)        )(self.components)
        self.weight = (lambda components:        np.array([0,0,-sum([i.mass for i in components])])    )(self.components)
        # 3-D
        self.force = (lambda lift, drag, weight:np.sum([lift,drag,weight],axis=0))(self.lift,self.drag,self.weight)
        # 3-D
        self.acceleration = (lambda force, weight:force/weight)(self.force,np.linalg.norm(self.weight))
        self.OpenSCAD_obj = (lambda a : self.fitTogether(a))(self.components)
    def update(self,deltaT = 0.01):

        acceleration = self.acceleration

        for i in self.components:
            i.velocity = i.velocity + acceleration*deltaT
            i.pos = (np.array(i.pos) + i.velocity*deltaT).tolist()

        # We will define the moments of force later.
    def fitTogether(self,a):
        total = a[0].OpenSCAD_obj
        for i in a:
            total = total + i.OpenSCAD_obj

            #total = total + spherePoint(i.centroid)
        return total

def liftWing(a,b,c,d):
    return [0,0,1]



def spherePoint(pos=[0,0,0],color1=[0,0,1],color2=[0,1,0]):
    a = color(color2)(sphere(r=0.25,segments=100)*cube(2))
    a = a + color(color1)(rotate([0,90,0])((sphere(r=0.25,segments=100)*cube(2))))
    a = a + rotate([0,0,180])(a)
    a = a + rotate([180,0,0])(a)

    a = translate(pos)(a)
    return a
