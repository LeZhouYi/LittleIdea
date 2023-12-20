import json
import os
import sys
from data import FrameConfig

class Manager:
    def __init__(self):
        self.skinSourcePath = None  # 源皮肤路径
        self.modsPath = None  # 3dmigoto Mods文件夹
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
        file = os.path.join(sys.path[0], FrameConfig.dataFile)
        if os.path.exists(file):
            with open(file, encoding="utf-8") as f:
                jsonData = json.load(f)
        if jsonData != None:
            self.skinSourcePath = jsonData["skinSourcePath"]
            self.modsPath = jsonData["modsPath"]

    def writeToFile(self):
        """将当前数据写到文件"""
        jsonData = {"skinSourcePath": self.skinSourcePath, "modsPath": self.modsPath}
        file = os.path.join(sys.path[0], FrameConfig.dataFile)
        if os.path.exists(file):
            with open(file, encoding="utf-8", mode="w") as f:
                f.write(json.dumps(jsonData))
