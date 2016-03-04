__author__ = 'Vishakh Kumar'

import collections
import math
import numpy as np


from itertools import product





#number of wing parameters. Refer generateWing for list of parameters.
wingParameters = 11
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
        self.rootAngle = d["rootAngle"]*math.pi/180
        self.tipAngle = d["tipAngle"]*math.pi/180
        self.sweepAngle = d["sweepAngle"]*math.pi/180
        self.dihedralAngle = d["dihedralAngle"]*math.pi/180
        self.attackAngle = d["attackAngle"]*math.pi/180
        self.velocity = d["velocity"]
        self.airDensity = d["airDensity"]
        self.pos = d["pos"]
        self.point1 = (lambda a,pos: [a[0]+pos[0],a[1]+pos[1],a[2]+pos[2]])(    [0,0,0],self.pos)
        self.point4 = (lambda a,pos: [a[0]+pos[0],a[1]+pos[1],a[2]+pos[2]])(    (lambda a,x,y,z:rotation(a,x,y,z))( (lambda rootChord, rootAngle: [rootChord*math.sin(rootAngle), rootChord*math.cos(rootAngle),0])(self.rootChord, self.tipAngle)                                                                                      ,self.dihedralAngle,self.attackAngle,0),self.pos)
        self.point2 = (lambda a,pos: [a[0]+pos[0],a[1]+pos[1],a[2]+pos[2]])(    (lambda a,x,y,z:rotation(a,x,y,z))( (lambda span, tipChord, tipAngle, attackAngle : [span - tipChord*math.sin(tipAngle),(span - tipChord*math.sin(tipAngle))*math.tan(attackAngle),0])(self.span, self.tipChord, self.tipAngle, self.attackAngle)      ,self.dihedralAngle,self.attackAngle,0),self.pos)
        self.point3 = (lambda a,pos: [a[0]+pos[0],a[1]+pos[1],a[2]+pos[2]])(    (lambda a,x,y,z:rotation(a,x,y,z))( (lambda span, tipChord, tipAngle, attackAngle: [span, tipChord*math.cos(tipAngle)+ (span-tipChord*math.sin(tipAngle))*math.tan(attackAngle),0])(self.span, self.tipChord, self.tipAngle, self.attackAngle)         ,self.dihedralAngle,self.attackAngle,0),self.pos)
        self.centroid = [(point1[0]+point2[0]+point3[0]+point4[0])/4,(point1[1]+point2[1]+point3[1]+point4[1])/4,(point1[2]+point2[2]+point3[2]+point4[2])/4]
        self.area = (lambda point1,point2,point3,point4: 0.5*abs(np.linalg.norm(np.cross([point2[0]-point1[0],point2[1]-point1[1],point2[2]-point1[2]],[point4[0]-point1[0],point4[1]-point1[1],point4[2]-point1[2]]))) + 0.5*abs(np.linalg.norm(np.cross([point3[0]-point1[0],point3[1]-point1[1],point3[2]-point1[2]],[point4[0]-point1[0],point4[1]-point1[1],point4[2]-point1[2]]))))(self.point1,self.point2,self.point3,self.point4)
        self.liftCoefficient = (lambda x: 2*math.pi*x)(self.attackAngle)
        # NOTE: need to correct the conditions if angle of attack exceeds stall angle
        self.dragCoefficient = (lambda x: 1.28*math.sin(x))(self.attackAngle)
        self.lift = (lambda a,x,y,z:rotation(a,x,y,z))([0,0,(lambda airDensity,velocity,liftCoefficient,area :abs(self.airDensity*np.linalg.norm(self.velocity)*np.linalg.norm(self.velocity)*self.liftCoefficient*self.area/2))(self.airDensity,self.velocity,self.liftCoefficient,self.area)],self.dihedralAngle,self.attackAngle,0)
        # lift is always perpendicular to the wing surface, regardless of other angles.
        self.drag = (lambda a,x,y,z:rotation(a,x,y,z))([0,(lambda airDensity,velocity,dragCoefficient,area :abs(self.airDensity*np.linalg.norm(self.velocity)*np.linalg.norm(self.velocity)*self.dragCoefficient*self.area/2))(self.airDensity,self.velocity,self.dragCoefficient,self.area),0],self.dihedralAngle,self.attackAngle,0)
        # drag is always parallel to the wing surface, regardless of other angles.


'''
def generateWing(d): # pass me my values in the form of a dictionary.
    global wingParameters
    global stallAngle
    if len(d) != wingParameters:
        print("You have incorrect number of wingParameters")
        return None

    # we define the X,Y coordinates of our wings by going over
    # the wing clockwise where the leading edge in above and the root chord
    #is to the left. Refer the slide 4.
    wing = ("wing","rootChord tipChord span rootAngle tipAngle sweepAngle dihedralAngle attackAngle velocity airDensity point1 point2 point3 point4 area liftCoefficient lift")
    return wing(
                      )
'''

#sample wing
def main():

    d = {}
    d["rootChord"] = 5
    d["tipChord"] =3
    d["span"] = 2
    d["rootAngle"] = 3
    d["tipAngle"] = 3
    d["sweepAngle"] = 2
    d["dihedralAngle"] = 4
    d["attackAngle"] = 4
    d["velocity"] = [0,-4,0]
    d["airDensity"] = 1
    d["pos"]=[0,0,0]
    sample = wing(d)
    print(d["rootChord"])
    print(sample.lift)
    print(sample.drag)

###################################################
# ensuring that everything loads properly
assert multiply([[6, 7, 8],
                 [5, 4, 5],
                 [1, 1, 1]],
                [[1, 2, 3],
                 [1, 2, 3],
                 [1, 2, 3]]) == [[21, 42, 63],
                                 [14, 28, 42],
                                 [3, 6, 9]]
###################################################


main()
