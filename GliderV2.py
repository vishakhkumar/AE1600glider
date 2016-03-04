__author__ = 'Vishakh Kumar'

import collections
import math
import numpy as np

from itertools import product

#number of wing parameters. Refer generateWing for list of parameters.
wingParameters = 13
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
          [0,math.cos(x),-math.sin(x)],
          [0,math.sin(x),math.cos(x)]
        ]
    Y = [ [math.cos(y),0,math.sin(y)],
          [0,1,0],
          [-math.sin(y),0,math.cos(y)]
        ]
    Z = [
          [math.cos(z),-math.sin(z),0],
          [math.sin(z),math.cos(z),0],
          [0,0,1]
        ]
    A = [
          [a[0]],
          [a[1]],
          [a[2]]
        ]
    ANS = multiply(multiply(Z,Y),multiply(X,A))
    return [ANS[0][0],ANS[1][0],ANS[2][0]]


class wing(object):
    def __init__(self,d):
        self.rootChord = d["rootChord"]
        self.tipChord = d["tipChord"]
        self.span = d["span"]
        self.velocity = d["velocity"]
        self.airDensity = d["airDensity"]
        self.pos = d["pos"]
        self.thickness = d["thickness"]
        # quantities that are modified slightly.
        self.rootAngle = d["rootAngle"]*math.pi/180
        self.tipAngle = d["tipAngle"]*math.pi/180
        self.sweepAngle = d["sweepAngle"]*math.pi/180
        self.dihedralAngle = d["dihedralAngle"]*math.pi/180
        self.attackAngle = d["attackAngle"]*math.pi/180
        # quantities that modify the input given drasticly
        self.flip = (lambda flip : -1 if True else 1)(d["flip"])
        # all derived quantities
        self.point1 = (lambda a,pos: [self.flip*(a[0]+pos[0]),a[1]+pos[1],a[2]+pos[2]])(    [0,0,0],self.pos)
        self.point4 = (lambda a,pos: [self.flip*(a[0]+pos[0]),a[1]+pos[1],a[2]+pos[2]])(    (lambda a,x,y,z:rotation(a,x,y,z))( (lambda rootChord, rootAngle: [rootChord*math.sin(rootAngle), rootChord*math.cos(rootAngle),0])(self.rootChord, self.tipAngle)                                                                                      ,self.dihedralAngle,self.attackAngle,0),self.pos)
        self.point2 = (lambda a,pos: [self.flip*(a[0]+pos[0]),a[1]+pos[1],a[2]+pos[2]])(    (lambda a,x,y,z:rotation(a,x,y,z))( (lambda span, tipChord, tipAngle, attackAngle: [span - tipChord*math.sin(tipAngle),(span - tipChord*math.sin(tipAngle))*math.tan(attackAngle),0])(self.span, self.tipChord, self.tipAngle, self.attackAngle)      ,self.dihedralAngle,self.attackAngle,0),self.pos)
        self.point3 = (lambda a,pos: [self.flip*(a[0]+pos[0]),a[1]+pos[1],a[2]+pos[2]])(    (lambda a,x,y,z:rotation(a,x,y,z))( (lambda span, tipChord, tipAngle, attackAngle: [span, tipChord*math.cos(tipAngle)+ (span-tipChord*math.sin(tipAngle))*math.tan(attackAngle),0])(self.span, self.tipChord, self.tipAngle, self.attackAngle)         ,self.dihedralAngle,self.attackAngle,0),self.pos)
        self.centroid = [(self.point1[0]+self.point2[0]+self.point3[0]+self.point4[0])/4,(self.point1[1]+self.point2[1]+self.point3[1]+self.point4[1])/4,(self.point1[2]+self.point2[2]+self.point3[2]+self.point4[2])/4]
        self.area = (lambda point1,point2,point3,point4: 0.5*abs(np.linalg.norm(np.cross([point2[0]-point1[0],point2[1]-point1[1],point2[2]-point1[2]],[point4[0]-point1[0],point4[1]-point1[1],point4[2]-point1[2]]))) + 0.5*abs(np.linalg.norm(np.cross([point3[0]-point1[0],point3[1]-point1[1],point3[2]-point1[2]],[point4[0]-point1[0],point4[1]-point1[1],point4[2]-point1[2]]))))(self.point1,self.point2,self.point3,self.point4)
        self.liftCoefficient = (lambda x: 2*math.pi*x)(self.attackAngle)
        # NOTE: need to correct the conditions if angle of attack exceeds stall angle
        self.dragCoefficient = (lambda x: 1.28*math.sin(x))(self.attackAngle)
        self.lift = (lambda a,x,y,z:rotation(a,x,y,z))([0,0,(lambda airDensity,velocity,liftCoefficient,area :abs(self.airDensity*np.linalg.norm(self.velocity)*np.linalg.norm(self.velocity)*self.liftCoefficient*self.area/2))(self.airDensity,self.velocity,self.liftCoefficient,self.area)],self.dihedralAngle,self.attackAngle,0)
        # lift is always perpendicular to the wing surface, regardless of other angles.
        self.drag = (lambda a,x,y,z:rotation(a,x,y,z))([0,(lambda airDensity,velocity,dragCoefficient,area :abs(self.airDensity*np.linalg.norm(self.velocity)*np.linalg.norm(self.velocity)*self.dragCoefficient*self.area/2))(self.airDensity,self.velocity,self.dragCoefficient,self.area),0],self.dihedralAngle,self.attackAngle,0)
        # drag is always parallel to the wing surface, regardless of other angles.

        #renderpoints are called only by the render function. It's to satisfy the conditions of a polyhedron with six faces - two surfaces and the four edges of the balsa plank.
        #renderApointX are the points that make the points ABOVE
        #renderBpointX are the points that make the points BELOW
        self.renderApoint1 = (lambda x,y: [x[0]+y[0],x[1]+y[1],x[2]+y[2]])(rotation([0,0,self.thickness/2],self.dihedralAngle,self.attackAngle,0),self.point1)
        self.renderBpoint1 = (lambda x,y: [x[0]+y[0],x[1]+y[1],x[2]+y[2]])(rotation([0,0,-self.thickness/2],self.dihedralAngle,self.attackAngle,0),self.point1)

        self.renderApoint2 = (lambda x,y: [x[0]+y[0],x[1]+y[1],x[2]+y[2]])(rotation([0,0,self.thickness/2],self.dihedralAngle,self.attackAngle,0),self.point2)
        self.renderBpoint2 = (lambda x,y: [x[0]+y[0],x[1]+y[1],x[2]+y[2]])(rotation([0,0,-self.thickness/2],self.dihedralAngle,self.attackAngle,0),self.point2)

        self.renderApoint3 = (lambda x,y: [x[0]+y[0],x[1]+y[1],x[2]+y[2]])(rotation([0,0,self.thickness/2],self.dihedralAngle,self.attackAngle,0),self.point3)
        self.renderBpoint3 = (lambda x,y: [x[0]+y[0],x[1]+y[1],x[2]+y[2]])(rotation([0,0,-self.thickness/2],self.dihedralAngle,self.attackAngle,0),self.point3)

        self.renderApoint4 = (lambda x,y: [x[0]+y[0],x[1]+y[1],x[2]+y[2]])(rotation([0,0,self.thickness/2],self.dihedralAngle,self.attackAngle,0),self.point3)
        self.renderBpoint4 = (lambda x,y: [x[0]+y[0],x[1]+y[1],x[2]+y[2]])(rotation([0,0,-self.thickness/2],self.dihedralAngle,self.attackAngle,0),self.point3)

        self.renderpoints = [[self.renderApoint1,self.renderApoint2,self.renderApoint3,self.renderApoint4,
                             self.renderBpoint1,self.renderBpoint2,self.renderBpoint3,self.renderBpoint4],
                             [[0,1,4,5],[1,3,7,4],[2,1,5,6],[2,3,7,6],[0,1,2,3],[4,5,6,7]]
                            ]
