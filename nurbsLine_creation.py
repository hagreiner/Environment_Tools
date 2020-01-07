import maya.cmds as cmds
import math

# cmds.arclen() == finds lens of curve
# cmds.pointOnCurve(p=True, pr=0.1)


class FindPositions:
    loop_1 = None
    loop_2 = None
    loop_3 = None
    loop_4 = None
    # item = {width: x_width, height: avg_y_loc}

    nurbsCurve = None
    post = None
    picket = None
    # item = object

    def __init__(self):
        self.postNum = makeEven(cmds.intSliderGrp('postNum', query=True, value=True))
        self.points = curvePoints() # self.epNum =

    def postPositions(self):
        oldPost = None
        XZ = 0, 0

        for num in range(self.postNum):
            pos = cmds.pointOnCurve(FindPositions.nurbsCurve, p=True, pr=float(num) / (float(self.postNum)/float(self.points)))
            post = cmds.duplicate(FindPositions.post)
            cmds.move(pos[0], pos[1] + (findHeight(post))/2.0, pos[2], post)

            if num > 0:
                yRot = findYRot(XZ, (pos[0], pos[2]))
                cmds.rotate(0, yRot, 0, oldPost, relative=True)
                print yRot, XZ, pos[0], pos[2]

            oldPost = post
            XZ = pos[0], pos[2]


def curvePoints():
    return cmds.getAttr(FindPositions.nurbsCurve[0] + ".cp", s=1) - 3


def findHeight(selection):
    cmds.select(selection)
    xmin, ymin, zmin, xmax, ymax, zmax = cmds.xform(bb=True, query=True)
    return abs(ymax - ymin)


def findYRot(oldXZ, newXZ):
    # oldXY acts as origin
    # newXY is the point rotated around
    # cos angle = b / c -> side over hypotenuse
    # angle = b / (c*cos)

    b = abs(oldXZ[0] - newXZ[0])
    c = distance(oldXZ[0], newXZ[0], oldXZ[1], newXZ[1])
    num = b / c
    angle = radToDegree(math.acos(num))

    return angle


def distance(x1, x2, y1, y2):
    math.pow((x2-x1), 2) + math.pow((y2-y1), 2)
    return math.sqrt((math.pow((x2-x1), 2) + math.pow((y2-y1), 2)))


def radToDegree(radian):
    return radian * 180 / 3.14


def makeEven(num):
    if num % 2 == 1:
        return num + 1
    return num
