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
        self.points = curvePoints()
        CrossBeams().findActive()

    def postPositions(self):
        oldPost = None
        XZ = 0, 0

        for num in range(self.postNum):
            pos = cmds.pointOnCurve(FindPositions.nurbsCurve, p=True, pr=float(num) / (float(self.postNum)/float(self.points)))
            post = cmds.duplicate(FindPositions.post)
            cmds.move(pos[0], pos[1], pos[2], post)

            if num > 0:
                yRot = findYRot(XZ, (pos[0], pos[2]))
                cmds.rotate(0, yRot, 0, oldPost, relative=True)
                if num != self.postNum:
                    crossBeams = CrossBeams().addBeams(width=distance(XZ[0], pos[0], XZ[1], pos[2]))
                    pickets = Pickets().create(totalSpace=(distance(XZ[0], pos[0], XZ[1], pos[2]) - findWidth(FindPositions.post)))
                    cmds.move(XZ[0], 0, XZ[1], crossBeams)
                    cmds.rotate(0, yRot, 0, crossBeams, relative=True, p=[XZ[0], 0, XZ[1]])
                    cmds.move(XZ[0], 0, XZ[1], pickets)
                    cmds.rotate(0, yRot, 0, pickets, relative=True, p=[XZ[0], 0, XZ[1]])

            oldPost = post
            XZ = pos[0], pos[2]


class CrossBeams:
    activeList = []

    def __init__(self):
        self.sidesNum = cmds.intSliderGrp('sidesNum', query=True, value=True)
        self.crossWidth = cmds.floatSliderGrp('crossWidth', query=True, value=True)
        self.crossHeight = cmds.floatSliderGrp('crossHeight', query=True, value=True)
        self.spacing = cmds.floatSliderGrp('spacing', query=True, value=True)

    def findActive(self):
        CrossBeams.activeList = []
        if FindPositions.loop_1 != None:
            CrossBeams.activeList.append(FindPositions.loop_1)
        if FindPositions.loop_2 != None:
            CrossBeams.activeList.append(FindPositions.loop_2)
        if FindPositions.loop_3 != None:
            CrossBeams.activeList.append(FindPositions.loop_3)
        if FindPositions.loop_4 != None:
            CrossBeams.activeList.append(FindPositions.loop_4)

    def addBeams(self, width):
        cBGroup = cmds.group(em=True)
        objList = []
        xScale = findScale(self.crossHeight, self.crossWidth)

        for loop in CrossBeams.activeList:
            beam = cmds.polyCylinder(r=self.crossWidth, h=width - loop["width"]/3.0, sx=self.sidesNum, ch=False)
            cmds.rotate(0, 0, 90, beam)
            cmds.scale(xScale, 1, 1, beam)
            cmds.move(width/2.0, (self.crossWidth * xScale)/2.0 + loop["height"], 0, beam, relative=True)
            objList.append(beam)
            cmds.parent(beam, cBGroup)

        return cBGroup


class Pickets(CrossBeams):
    def create(self, totalSpace):
        picketWidth = findWidth(FindPositions.picket)
        picketNum = findPicketNum(self.spacing, totalSpace, picketWidth)

        pGroup = cmds.group(em=True)
        widthLeft = totalSpace - self.spacing

        for num in range(picketNum):
            picket = cmds.duplicate(FindPositions.picket)
            cmds.move(picketWidth/2.0 + ((self.spacing + picketWidth)*num + (findWidth(FindPositions.post)/2.0)) +
                      self.spacing, 0, 0, picket)
            widthLeft -= (picketWidth + self.spacing)
            cmds.parent(picket, pGroup)

        cmds.move(widthLeft, 0, 0, pGroup)
        return pGroup


def findPicketNum(spacingBetween, totalSpace, picketWidth):
    return int((totalSpace - spacingBetween) / (spacingBetween + picketWidth))


def findWidth(selection):
    cmds.select(selection)
    xmin, ymin, zmin, xmax, ymax, zmax = cmds.xform(bb=True, ws=True, query=True)
    return abs(xmax - xmin)


def findScale(wantedValue, currentValue):
    return wantedValue / currentValue


def curvePoints():
    return cmds.getAttr(FindPositions.nurbsCurve[0] + ".cp", s=1) - 3


def findHeight(selection):
    cmds.select(selection)
    xmin, ymin, zmin, xmax, ymax, zmax = cmds.xform(bb=True, query=True)
    return abs(ymax - ymin)


def findXMin(selection):
    cmds.select(selection)
    xmin, ymin, zmin, xmax, ymax, zmax = cmds.xform(bb=True, query=True)
    print xmin
    return xmin


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
