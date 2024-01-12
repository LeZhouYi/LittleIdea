import json
import os
import random
import math

dataFile = "data.json"  # 默认数据储存位置

class Config:
    def __init__(self):
        self.loadByFile()

    def setSkinPath(self, skinSourcePath: str):
        self.skinSourcePath = skinSourcePath

    def getSkinPath(self) -> str | None:
        return self.skinSourcePath

    def getModsPath(self) -> str | None:
        return self.modsPath

    def setModsPath(self, modsPath: str):
        self.modsPath = modsPath

    def loadByFile(self):
        """从文件中读取数据"""
        jsonData = None
        file = os.path.join(os.getcwd(), dataFile)
        if os.path.exists(file):
            with open(file, encoding="utf-8") as f:
                jsonData = json.load(f)
        if jsonData != None:
            self.skinSourcePath = jsonData["skinSourcePath"]
            self.modsPath = jsonData["modsPath"]
            self.roleKeys = jsonData["roleKeys"]
            self.roleKeysText = jsonData["roleKeysText"]
            self.backGroundColor = jsonData["backgroundColor"]
            self.title = jsonData["title"]
            self.font = jsonData["font"]
            self.windowWidth = jsonData["windowWidth"]
            self.windowHeight = jsonData["windowHeight"]
            self.roleIconSize = jsonData["roleIconSize"]
            self.defaultRoleKey = jsonData["defaultRoleKey"]
            self.defaultRoleIcon = jsonData["defaultRoleIcon"]
            self.skinControlWidth = jsonData["skinControlWidth"]
            self.defaultSkin = jsonData["defaultSkin"]
            self.roleSkinSize = jsonData["roleSkinSize"]
            self.colorSuccess = jsonData["colorSuccess"]
            self.colorDefault = jsonData["colorDefault"]
            self.colorFail = jsonData["colorFail"]
            self.tempDir = jsonData["tempDir"]

    def writeToFile(self):
        """将当前数据写到文件"""
        jsonData = {
            "skinSourcePath": self.skinSourcePath,
            "modsPath": self.modsPath,
            "roleKeys": self.roleKeys,
            "roleKeysText": self.roleKeysText,
            "backgroundColor": self.backGroundColor,
            "title": self.title,
            "font": self.font,
            "roleIconSize":self.roleIconSize,
            "defaultRoleKey":self.defaultRoleKey,
            "defaultRoleIcon":self.defaultRoleIcon,
            "skinControlWidth": self.skinControlWidth,
            "defaultSkin":self.defaultSkin,
            "roleSkinSize":self.roleSkinSize,
            "windowWidth":self.windowWidth,
            "windowHeight":self.windowHeight,
            "colorSuccess":self.colorSuccess,
            "colorDefault":self.colorDefault,
            "colorFail": self.colorFail,
            "tempDir": self.tempDir
        }
        file = os.path.join(os.getcwd(), dataFile)
        if os.path.exists(file):
            with open(file, encoding="utf-8", mode="w") as f:
                f.write(json.dumps(jsonData))

    def existRole(self, fileName: str) -> bool:
        """判断是否存在角色"""
        return fileName in self.roleKeys

    def getRoleText(self, fileName: str) -> str:
        """返回当前角色对应角色名"""
        if fileName in self.roleKeysText:
            return self.roleKeysText[fileName]
        return ""

    def getTitle(self)->str:
        """获得标题"""
        return self.title

    def getBackGround(self)->str:
        """背景颜色"""
        colors = ["white","black","green","blue","pink","yellow","brown","gray"]
        if self.backGroundColor!=None and self.backGroundColor in colors:
            return self.backGroundColor
        return random.choice(colors)

    def getFont(self)->tuple:
        """获取字体"""
        return tuple(self.font)

    def getWindowWidth(self)->int:
        """窗体宽度"""
        return self.windowWidth

    def getWindowHeight(self)->int:
        """窗体高度"""
        return self.windowHeight

    def getRoleIconSize(self)->tuple:
        """获取角色图标显示的尺寸"""
        return tuple(self.roleIconSize)

    def getDefaultRoleKey(self)->str:
        """获取默认角色Key"""
        return self.defaultRoleKey

    def getDefaultRoleIcon(self)->str:
        """获取默认角色图标路径"""
        return self.defaultRoleIcon

    def getRoleColoumnMax(self,width:int)->int:
        """获取一行最多角色数"""
        return math.floor(width/(self.roleIconSize[0]+20))

    def getRoleBtnBorder(self,width:int,columnMax:int)->int:
        """获取角色按钮合成的边距"""
        border = (width-(self.roleIconSize[0]+9)*columnMax)/columnMax/2
        return max(0,math.floor(border))

    def getControlPanelWidth(self)->int:
        """获取控制面板宽度"""
        return self.skinControlWidth

    def getDefaultSkin(self)->str:
        """获取默认皮肤路径"""
        return self.defaultSkin

    def getRoleSkinSize(self)->tuple:
        """获取默认皮肤尺寸"""
        return tuple(self.roleSkinSize)

    def getColorSuccess(self)->str:
        """操作成功字体颜色"""
        return self.colorSuccess

    def getColorDefault(self)->str:
        """默认字体颜色"""
        return self.colorDefault

    def getColorFail(self)->str:
        """操作失败字体颜色"""
        return self.colorFail

    def getTempDir(self)->str:
        """获取临时存储文件位置"""
        return self.tempDir

    def getSkinColoumMax(self,columnWidth:int)->int:
        """返回一行最多显示皮肤数"""
        return (columnWidth-self.skinControlWidth)//(self.roleSkinSize[0]+3)

    def getSkinBorder(self,columnWidth:int,cloumnMax:int)->int:
        """返回皮肤控件的border"""
        border = (columnWidth-self.skinControlWidth-(self.roleSkinSize[0])*cloumnMax)/cloumnMax/5
        return max(0,math.floor(border))