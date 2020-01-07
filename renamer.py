import maya.cmds as cmds


def rename():
    determinedPrefix = createPrefix()
    object = cmds.ls(sl=True)
    baseName = cmds.textField("baseName", query=True, text=True)

    cmds.rename(object, (determinedPrefix + "_" + baseName + "_" + "#"))


def createPrefix():
    if cmds.radioButton("character", query=True, sl=True) == True:
        return "CH"

    elif cmds.radioButton("ui", query=True, sl=True) == True:
        return "UI"

    elif cmds.radioButton("staticMesh", query=True, sl=True) == True:
        return "SM"

    elif cmds.radioButton("vehicle", query=True, sl=True) == True:
        return "VH"

    elif cmds.radioButton("weapon", query=True, sl=True) == True:
        return "WP"

