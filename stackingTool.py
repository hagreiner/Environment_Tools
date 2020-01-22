import maya.cmds as cmds
import ui
import random


class LogObjects:
    savedObjectList = {}
    heightDict = {}
    widthDict = {}
    depthDict = {}

    def saveObject(self, strType, index):
        LogObjects.savedObjectList[index] = cmds.ls(sl=True)
        cmds.textField(strType, edit=True, text="Object Logged")

    def deleteObject(self, strType, index):
        del LogObjects.savedObjectList[index]
        cmds.textField(strType, edit=True, text="None")


class Stack:
    def create(self):
        keyAbleList = varifyObjects()

        for object in keyAbleList:
            LogObjects.heightDict[object] = GetObjectInformation(LogObjects.savedObjectList[object]).getHeight()
            LogObjects.widthDict[object] = GetObjectInformation(LogObjects.savedObjectList[object]).getWidth()
            LogObjects.depthDict[object] = GetObjectInformation(LogObjects.savedObjectList[object]).getDepth()

        startingHeight = 0
        rotationList = StackObjects().determineRotation()
        xMove, zMove = StackObjects().determineMovement()

        for object in range(StackObjects().determineStackSize()):
            key = random.choice(keyAbleList)
            rotation = random.choice(rotationList)

            stackItem = cmds.duplicate(LogObjects.savedObjectList[key])
            cmds.move(random.choice(xMove), startingHeight, random.choice(zMove), stackItem)
            cmds.rotate(0, rotation, 0, stackItem)

            startingHeight += LogObjects.heightDict[key]


class StackObjects:
    def __init__(self):
        self.disorderNum = cmds.floatSlider("disorder", query=True, value=True)

    def determineMovement(self):
        xMove = []
        zMove = []

        for key, val in LogObjects.widthDict.items():
            xMove += list(range(int(-self.disorderNum*(val/3.0)), int(self.disorderNum*(val/3.0))))

        for key, val in LogObjects.depthDict.items():
            zMove += list(range(int(-self.disorderNum*(val/3.0)), int(self.disorderNum*(val/3.0))))

        return xMove, zMove

    def determineRotation(self):
        rotList = list(range(int(-90*self.disorderNum), int(90*self.disorderNum)))
        if rotList == []:
            rotList.append(0)
        return rotList

    def determineStackSize(self):
        self.sizeDict = {0: list(range(2, 5)), 1: list(range(6, 10)), 2: list(range(11, 15))}
        self.size = findWhichChecked()
        return random.choice(self.sizeDict[self.size])


class GetObjectInformation:
    def __init__(self, object):
        self.object = object
        self.xmin, self.ymin, self.zmin, self.xmax, self.ymax, self.zmax = cmds.xform(bb=True, query=True)

    def getHeight(self):
        return abs(self.ymax - self.ymin)

    def getWidth(self):
        return abs(self.xmax - self.xmin)

    def getDepth(self):
        return abs(self.zmax - self.zmin)


def findWhichChecked():
    if cmds.radioButton("smallStack", query=True, sl=True) == True:
        return 0
    elif cmds.radioButton("mediumStack", query=True, sl=True) == True:
        return 1
    elif cmds.radioButton("largeStack", query=True, sl=True) == True:
        return 2


def varifyObjects():
    keyList = []
    for key, val in LogObjects.savedObjectList.items():
        keyList.append(key)
    if len(keyList) == 0:
        print("this will not work")
    return keyList
