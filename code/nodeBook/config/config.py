import json
import os

dataFile = "src/config.json"  # 默认数据储存位置
configKeys = ["windowSize","windowTitle"]

"""配置文件相关，读取/写配置文件"""
class Config:
    def __init__(self) -> None:
        self.data = {}
        self.loadByFile()

    def loadByFile(self) -> None:
        """从文件中读取数据"""
        jsonData = None
        file = os.path.join(os.getcwd(), dataFile)
        if os.path.exists(file):
            with open(file, encoding="utf-8") as f:
                jsonData = json.load(f)
        if jsonData != None:
            for key in configKeys:
                self.data[key]=jsonData[key]

    def writeToFile(self) -> None:
        """将当前数据写到文件"""
        file = os.path.join(os.getcwd(), dataFile)
        if os.path.exists(file):
            with open(file, encoding="utf-8", mode="w") as f:
                f.write(json.dumps(self.data))

    def getGeometry(self)->str:
        """获取窗口大小/位置"""
        windowSize = self.data["windowSize"]
        return "%dx%d"%(windowSize[0],windowSize[1])

    def getTitle(self)->str:
        """获取窗口标题"""
        return str(self.data["windowTitle"])