import json
import os
from data import FrameConfig

class Manager:
    def __init__(self):
        self.skinSourcePath = None  # 源皮肤路径
        self.modsPath = None  # 3dmigoto Mods文件夹
        self.roleKeys = []
        self.roleKeysText = {}
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
        file = os.path.join(os.getcwd(), FrameConfig.dataFile)
        if os.path.exists(file):
            with open(file, encoding="utf-8") as f:
                jsonData = json.load(f)
        if jsonData != None:
            self.skinSourcePath = jsonData["skinSourcePath"]
            self.modsPath = jsonData["modsPath"]
            self.roleKeys = jsonData["roleKeys"]
            self.roleKeysText = jsonData["roleKeysText"]

    def writeToFile(self):
        """将当前数据写到文件"""
        jsonData = {"skinSourcePath": self.skinSourcePath, "modsPath": self.modsPath,"roleKeys":self.roleKeys,"roleKeysText":self.roleKeysText}
        file = os.path.join(os.getcwd(), FrameConfig.dataFile)
        if os.path.exists(file):
            with open(file, encoding="utf-8", mode="w") as f:
                f.write(json.dumps(jsonData))

    def existRole(self,fileName: str) -> bool:
        """判断是否存在角色"""
        return fileName in self.roleKeys

    def getRoleText(self,fileName: str) -> str:
        """返回当前角色对应角色名"""
        if fileName in self.roleKeysText:
            return self.roleKeysText[fileName]
        return ""