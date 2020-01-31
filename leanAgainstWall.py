import maya.cmds as cmds
import math


class LeanObject:
    wall = None
    object = None

    def loadInWall(self):
        LeanObject.wall = cmds.ls(sl=True)

    def loadInObject(self):
        LeanObject.object = cmds.ls(sl=True)

    def leanIt(self):
        directionList = FindPolyInformation().direction()
        angleForRot = FindPolyInformation().findAxis()
        if angleForRot[0] == True:
            if directionList[0] == -1:
                rot, piv = FindPolyInformation().findRotXNeg()
            else:
                rot, piv = FindPolyInformation().findRotXPos()
            cmds.rotate(rot, 0, 0, LeanObject.object, pivot=piv)
        elif angleForRot[2] == True:
            if directionList[2] == 1:
                rot, piv = FindPolyInformation().findRotZNeg()
            else:
                rot, piv = FindPolyInformation().findRotZPos()
            cmds.rotate(0, 0, rot, LeanObject.object, pivot=piv)


class FindPolyInformation:
    def __init__(self):
        cmds.select(LeanObject.wall)
        self.xmin_Wall, self.ymin_Wall, self.zmin_Wall, self.xmax_Wall, self.ymax_Wall, self.zmax_Wall = \
            cmds.xform(bb=True, query=True)
        cmds.select(LeanObject.object)
        self.xmin_Obj, self.ymin_Obj, self.zmin_Obj, self.xmax_Obj, self.ymax_Obj, self.zmax_Obj = \
            cmds.xform(bb=True, query=True)

    def findRotXPos(self):
        adjacentLine = abs(self.zmax_Obj - self.zmin_Wall)
        hypLine = self.ymax_Obj
        return (90 - radiansToDegree(math.acos(adjacentLine / hypLine))), \
               [(self.xmax_Obj + self.xmin_Obj) / 2.0, 0, self.zmax_Obj]

    def findRotXNeg(self):
        adjacentLine = abs(self.zmin_Obj - self.zmax_Wall)
        hypLine = self.ymax_Obj
        return (-90 + radiansToDegree(math.acos(adjacentLine / hypLine))), \
               [(self.xmax_Obj + self.xmin_Obj) / 2.0, 0, self.zmin_Obj]

    def findRotZPos(self):
        adjacentLine = abs(self.xmin_Obj - self.xmax_Wall)
        hypLine = self.ymax_Obj
        return 90 - radiansToDegree(math.acos(adjacentLine/hypLine)), \
               [self.xmin_Obj, 0, (self.zmax_Obj + self.zmin_Obj)/2.0]

    def findRotZNeg(self):
        adjacentLine = abs(self.xmax_Obj - self.xmin_Wall)
        hypLine = self.ymax_Obj
        return -90 + radiansToDegree(math.acos(adjacentLine / hypLine)), \
               [self.xmax_Obj, 0, (self.zmax_Obj + self.zmin_Obj) / 2.0]

    def direction(self):
        direction = [0, 0, 0]
        if (self.xmax_Obj + self.xmin_Obj)/2.0 > (self.xmax_Wall + self.xmin_Wall)/2.0:
            direction[2] = -1
        elif (self.xmax_Obj + self.xmin_Obj)/2.0 < (self.xmax_Wall + self.xmin_Wall)/2.0:
            direction[2] = 1
        if (self.zmax_Obj + self.zmin_Obj)/2.0 > (self.zmax_Wall + self.zmin_Wall)/2.0:
            direction[0] = -1
        elif (self.zmax_Obj + self.zmin_Obj)/2.0 < (self.zmax_Wall + self.zmin_Wall)/2.0:
            direction[0] = 1

        return direction

    def findAxis(self):
        angles = [False, False, False]
        if abs((self.xmax_Wall - self.xmin_Wall)) > abs((self.zmax_Wall - self.zmin_Wall)):
            angles[0] = True
        else:
            angles[2] = True

        return angles


def radiansToDegree(radian):
    return radian * 180 / 3.14
