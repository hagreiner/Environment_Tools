import maya.cmds as cmds
from functools import partial
import renamer as rn
import fenceItemLogger as fl
import nurbsLine_creation as nl


def start():
    """
    :summary: the function that is called to start the UI, sets the timeline to 30fps, and resets the timeline
    :parameter: none
    :return: nothing
    """
    MainMenu().start()


def end():
    """
    :summary: closes the main UI window
    :parameter: none
    :return: nothing
    """
    reset()
    if cmds.window("mainUI", exists=True):
        cmds.deleteUI("mainUI", window=True)


def delete():
    """
    :summary: selects everything in the scene and then deletes it
    :parameter: none
    :return: nothing
    """
    cmds.select(all=True)
    cmds.delete()


class MainMenu:
    def __init__(self):
        self.col = "mainCol"
        self.window = "mainUI"
        self.width = 300
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)

        if cmds.windowPref(self.window, exists=True):
            cmds.windowPref(self.window, remove=True)

        self.window = cmds.window(self.window, title="Tools Package",
                                  minimizeButton=False, maximizeButton=False, sizeable=False)

    def start(self):
        """
        :summary: is called in the start() function, contains the main UI for the scripts
        :parameter: none
        :return: nothing
        """
        self.typeCol = cmds.columnLayout(self.col, parent=self.window, w=self.width)

        # section one
        frameLayout1 = cmds.frameLayout(width=self.width, label="Rocks", collapse=True, collapsable=True,
                                        marginHeight=10,
                                        marginWidth=5, parent=self.typeCol,
                                        ec=partial(frameCollapseChanged, str(self.col)),
                                        cc=partial(frameCollapseChanged, str(self.col)))

        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width - 10)], parent=frameLayout1,
                             co=[1, "both", 5])
        cmds.text("stuff")

        # section two
        frameLayoutFence = cmds.frameLayout(width=self.width, label="Fences", collapse=True, collapsable=True,
                                            marginHeight=10,
                                            marginWidth=5, parent=self.typeCol,
                                            ec=partial(frameCollapseChanged, str(self.col)),
                                            cc=partial(frameCollapseChanged, str(self.col)))

        cmds.rowColumnLayout(numberOfColumns=2,
                             columnWidth=[(1, (self.width - 20) / 2.0), (2, (self.width - 20) / 2.0)],
                             parent=frameLayoutFence, co=[1, "both", 5])
        cmds.button(label="Curve", h=20, command=lambda args: fl.Logger().curve("curve"))
        cmds.textField("curve", en=False, text="None", height=20)
        cmds.button(label="Post", h=20, command=lambda args: fl.Logger().fencePost("post"))
        cmds.textField("post", en=False, text="None", height=20)
        cmds.button(label="Picket", h=20, command=lambda args: fl.Logger().fencePicket("picket"))
        cmds.textField("picket", en=False, text="None", height=20)

        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width - 10)], parent=frameLayoutFence,
                             co=[1, "both", 5])
        cmds.floatSliderGrp('spacing', label='Picket Spacing', field=True, minValue=1, maxValue=100,
                            value=1, columnWidth=[(1, 100), (2, 50), (3, self.width - 150)], cal=[1, "center"])
        cmds.intSliderGrp('postNum', label='Number of Posts', field=True, minValue=2, maxValue=30, value=2, step=2,
                            columnWidth=[(1, 100), (2, 50), (3, self.width - 150)], cal=[1, "center"])
        cmds.text("Cross Beams", height=20)
        cmds.text("select edge-loop location on post")

        cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, (self.width - 20)/2.0), (2, (self.width - 20)/2.0)],
                             parent=frameLayoutFence, co=[1, "both", 5])
        cmds.button(label="Location One", h=20, command=lambda args: fl.Logger().logLoop_1("locationOne"))
        cmds.textField("locationOne", en=False, text="None", height=20)
        cmds.button(label="Location Two", h=20, command=lambda args: fl.Logger().logLoop_2("locationTwo"))
        cmds.textField("locationTwo", en=False, text="None", height=20)
        cmds.button(label="Location Three", h=20, command=lambda args: fl.Logger().logLoop_3("locationThree"))
        cmds.textField("locationThree", en=False, text="None", height=20)
        cmds.button(label="Location Four", h=20, command=lambda args: fl.Logger().logLoop_4("locationFour"))
        cmds.textField("locationFour", en=False, text="None", height=20)
        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width - 10)], parent=frameLayoutFence,
                             co=[1, "both", 5])
        cmds.intSliderGrp('sidesNum', label='Number of Sides', field=True, minValue=3, maxValue=30,
                          value=1, columnWidth=[(1, 100), (2, 50), (3, self.width - 150)], cal=[1, "center"])
        cmds.floatSliderGrp('crossWidth', label='Width', field=True, minValue=5, maxValue=75,
                            value=1, columnWidth=[(1, 100), (2, 50), (3, self.width - 150)], cal=[1, "center"])
        cmds.floatSliderGrp('crossHeight', label='Height', field=True, minValue=5, maxValue=75,
                            value=1, columnWidth=[(1, 100), (2, 50), (3, self.width - 150)], cal=[1, "center"])

        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width - 10)], parent=frameLayoutFence,
                             co=[1, "both", 5])
        cmds.button(label="Test", h=20,
                    command=lambda args: (fl.Logger().confirm(), nl.FindPositions().postPositions()))

        # section three
        frameLayoutRenamer = cmds.frameLayout(width=self.width, label="Renaming Objects", collapse=False,
                                              collapsable=True, marginHeight=10,
                                              marginWidth=5, parent=self.typeCol,
                                              ec=partial(frameCollapseChanged, str(self.col)),
                                              cc=partial(frameCollapseChanged, str(self.col)))

        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width - 10)], parent=frameLayoutRenamer,
                             co=[1, "both", 5])

        cmds.text("Prefix", align="center")
        cmds.radioCollection("prefix")
        cmds.radioButton("character", label="Character")
        cmds.radioButton("ui", label="UI")
        cmds.radioButton("staticMesh", label="Static Mesh", sl=True)
        cmds.radioButton("vehicle", label="Vehicle")
        cmds.radioButton("weapon", label="Weapon")

        cmds.text("", h=2)
        cmds.separator()
        cmds.text(" ", h=2)

        cmds.text("Object Name", h=20)
        cmds.text("  ", h=2)
        cmds.textField("baseName")

        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width - 10)], parent=frameLayoutRenamer,
                             co=[1, "both", 5])
        cmds.button(label="Rename Object", h=30, command=lambda args: rn.rename())

        # put this at end
        winHeight = 0
        for child in cmds.columnLayout(self.typeCol, q=1, ca=1):
            winHeight += eval('cmds.' + cmds.objectTypeUI(child) + '("' + child + '", q=1, h=1)')
        cmds.window(self.window, e=1, h=winHeight)
        cmds.showWindow(self.window)


def frameCollapseChanged(column):
    """
    :summary: updates the height of the column frames within it are collapsed or expanded
    :param column: the column
    :return: nothing
    """
    cmds.evalDeferred(
        "cmds.window('mainUI', e=1, h=sum([eval('cmds.' + cmds.objectTypeUI(child) + '(\\'' + child + '\\', q=1, h=1)') "
        "for child in cmds.columnLayout('" + column + "', q=1, ca=1)]))")
