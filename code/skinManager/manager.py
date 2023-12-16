import json
import os
import data
import sys


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

    def setModsPath(self, modsPath:str):
        self.modsPath = modsPath

    def loadByFile(self):
        """从文件中读取数据"""
        jsonData = None
        file = sys.path[0] + "/" + data.FILE
        if os.path.exists(file):
            with open(file, encoding="utf-8") as f:
                jsonData = json.load(f)
        if jsonData != None:
            self.skinSourcePath = jsonData["skinSourcePath"]
            self.modsPath = jsonData["modsPath"]
