import maya.cmds as cmds


class LeanObject:
    wall = None
    object = None

    def loadInWall(self):
        LeanObject.wall = cmds.ls(sl=True)

    def loadInObject(self):
        LeanObject.object = cmds.ls(sl=True)

    def leanIt(self):
        print LeanObject.wall, "$$$$$", LeanObject.object
        print FindPolyInformation().direction()
        print FindPolyInformation().findAxis()


class FindPolyInformation:
    def __init__(self):
        cmds.select(LeanObject.wall)
        self.xmin_Wall, self.ymin_Wall, self.zmin_Wall, self.xmax_Wall, self.ymax_Wall, self.zmax_Wall = \
            cmds.xform(bb=True, query=True)
        cmds.select(LeanObject.object)
        self.xmin_Obj, self.ymin_Obj, self.zmin_Obj, self.xmax_Obj, self.ymax_Obj, self.zmax_Obj = \
            cmds.xform(bb=True, query=True)

    def findRot(self):
        pass

    def direction(self):
        direction = [0, 0, 0]
        if (self.xmax_Obj + self.xmin_Obj)/2.0 > (self.xmax_Wall + self.xmin_Wall)/2.0:
            direction[0] = -1
        elif (self.xmax_Obj + self.xmin_Obj)/2.0 < (self.xmax_Wall + self.xmin_Wall)/2.0:
            direction[0] = 1
        if (self.zmax_Obj + self.zmin_Obj)/2.0 > (self.zmax_Wall + self.zmin_Wall)/2.0:
            direction[2] = -1
        elif (self.zmax_Obj + self.zmin_Obj)/2.0 < (self.zmax_Wall + self.zmin_Wall)/2.0:
            direction[2] = 1

        return direction

    def findAxis(self):
        angles = [False, False, False]
        if abs((self.xmax_Wall - self.xmin_Wall)) > abs((self.zmax_Wall - self.zmin_Wall)):
            angles[2] = True
        else:
            angles[0] =True

        return angles
