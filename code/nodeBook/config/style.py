import os
import json

"""控件相关个性配置"""
class Style:

    def __init__(self,filePath:str) -> None:
        self.filePath = filePath #本地配置文件路径
        self.cnfs = {} #样式数据集
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

    def getCnf(self,key:str)->dict:
        """获取控件配置"""
        if str(key).find("_")>=0:
            key = key.split("_")[0]
        if key in self.cnfs:
            return self.cnfs[key]["cnf"]
        return {}

    def getPackCnf(self,key:str)->dict:
        """获取控件布局配置"""
        if str(key).find("_")>=0:
            key = key.split("_")[0]
        if key in self.cnfs and "packCnf" in self.cnfs[key]:
            return self.cnfs[key]["packCnf"]
        return None