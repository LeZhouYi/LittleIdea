import os
import json

class PwdBook:

    def __init__(self,filePath:str) -> None:
        self.filePath = filePath #本地配置文件路径
        self.data = {} #样式数据集
        self.loadByFile()

    def loadByFile(self) -> None:
        """从文件中读取数据"""
        jsonData = None
        file = os.path.join(os.getcwd(), self.filePath)
        if os.path.exists(file):
            with open(file, encoding="utf-8") as f:
                jsonData = json.load(f)
        if jsonData != None:
            self.cnfs = jsonData

    def getGroupKeys(self)->list[str]:
        """获取组的键集"""
        return list(self.data.keys())

    def getGroup(self,groupKey:str)->dict:
        """获取组"""