import sys
import os
from PIL import Image

def createDir(path:str):
    """创建文件夹"""
    if not os.path.exists(path):
        os.mkdir(path)

def isPhoto(fileName:str):
    """判断是否为图片"""
    endStr = (".png")
    return fileName.endswith(endStr)

def getCropStage(width:int,height:int)->tuple|None:
    """获取剪切策略"""
    if width == 1920 and height== 1080:
        return (715,100,1205,1080)
    return None

def main():
    """主程序入口"""
    path = sys.path[0]
    sourcePath = os.path.join(path,"sources")
    resultPath = os.path.join(path,"results")
    createDir(sourcePath)
    createDir(resultPath)
    for fileName in os.listdir(sourcePath):
        filePath = os.path.join(sourcePath,fileName)
        if os.path.isfile(filePath) and isPhoto(fileName):
            image = Image.open(filePath)
            regionStage = getCropStage(image.width,image.height)
            if regionStage!=None:
                regoinImage = image.crop(regionStage)
                outFileName = os.path.join(resultPath,fileName)
                regoinImage.save(outFileName)

if __name__ == "__main__":
    main()