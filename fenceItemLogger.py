import maya.cmds as cmds


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

    def logLoop_1(self, strType):
        selection = cmds.ls(sl=True)
        Logger.loop_1 = findLocationData(selection)
        cmds.textField(strType, edit=True, text=selection[0])

    def logLoop_2(self, strType):
        selection = cmds.ls(sl=True)
        Logger.loop_2 = findLocationData(selection)
        cmds.textField(strType, edit=True, text=selection[0])

    def logLoop_3(self, strType):
        selection = cmds.ls(sl=True)
        Logger.loop_3 = findLocationData(selection)
        cmds.textField(strType, edit=True, text=selection[0])

    def logLoop_4(self, strType):
        selection = cmds.ls(sl=True)
        Logger.loop_4 = findLocationData(selection)
        cmds.textField(strType, edit=True, text=selection[0])

    def curve(self):
        selection = cmds.ls(sl=True)
        Logger.nurbsCurve = selection

    def fencePost(self):
        selection = cmds.ls(sl=True)
        Logger.post = selection

    def fencePicket(self):
        selection = cmds.ls(sl=True)
        Logger.picket = selection


def findLocationData(selection):
    cmds.select(selection)
    xmin, ymin, zmin, xmax, ymax, zmax = cmds.xform(bb=True, query=True)
    width = abs(xmax - xmin)
    height = abs((ymin - ymax) / 2.0)
    return {"width": width, "height": height}