import maya.cmds as cmds
import nurbsLine_creation as nl


class Logger:
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
        self.selection = cmds.ls(sl=True)
        self.locationData = findLocationData(self.selection)

    def logLoop_1(self, strType):
        Logger.loop_1 = self.locationData
        updateField(strType, self.selection[0])

    def logLoop_2(self, strType):
        Logger.loop_2 = self.locationData
        updateField(strType, self.selection[0])

    def logLoop_3(self, strType):
        Logger.loop_3 = self.locationData
        updateField(strType, self.selection[0])

    def logLoop_4(self, strType):
        Logger.loop_4 = self.locationData
        updateField(strType, self.selection[0])

    def curve(self, strType):
        selection = cmds.ls(sl=True)
        Logger.nurbsCurve = selection
        updateField(strType, selection[0])

    def fencePost(self, strType):
        selection = cmds.ls(sl=True)
        Logger.post = selection
        updateField(strType, selection[0])

    def fencePicket(self, strType):
        selection = cmds.ls(sl=True)
        Logger.picket = selection
        updateField(strType, selection[0])

    def confirm(self):
        nl.FindPositions.nurbsCurve = Logger.nurbsCurve
        nl.FindPositions.loop_1 = Logger.loop_1
        nl.FindPositions.loop_2 = Logger.loop_2
        nl.FindPositions.loop_3 = Logger.loop_3
        nl.FindPositions.loop_4 = Logger.loop_4
        nl.FindPositions.post = Logger.post
        nl.FindPositions.picket = Logger.picket


def findLocationData(selection):
    cmds.select(selection)
    xmin, ymin, zmin, xmax, ymax, zmax = cmds.xform(bb=True, ws=True, query=True)
    width = abs(xmax - xmin)
    height = abs((ymin + ymax) / 2.0)
    return {"width": width, "height": height}


def updateField(fieldName, data):
    cmds.textField(fieldName, edit=True, text=data)