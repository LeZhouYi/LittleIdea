import os

def createPath(path:str)->None:
    '''若文件路径不存在，则新建'''
    if not os.path.exists(path):
        os.makedirs(path)

def toUnicode(text:str)->str:
    '''将文本包含中文的部分转为unicode字符串'''
    toText = ""
    for char in text:
        if '\u4e00' <= char <= '\u9fff' or char=='\uff0c':
            toText+= hex(ord(char)).upper().replace('0X','\\u')
        else:
            toText+=char
    return toText

def dealFile()->None:
    inPath = "%s/input"%(os.getcwd()) #导入路径
    outPath = "%s/output"%(os.getcwd()) #导出路径
    createPath(inPath)
    createPath(outPath)
    for dirPath, dirNames, fileNames in os.walk(inPath):
        for fileName in fileNames:
            #排除其它格式的文件
            if not fileName.endswith(".json"):
                continue
            inFileName = os.path.join(dirPath, fileName)
            prefixPath = dirPath.replace(inPath,"") #解析前缀
            outFilePath = "%s%s"%(outPath,prefixPath) #输出路径

            with open(inFileName) as file:
                lines = file.readlines()
            for i in range(len(lines)):
                lines[i] = toUnicode(lines[i])
            createPath(outFilePath)
            outFileName = os.path.join(outFilePath,fileName)
            with open(outFileName,'w+') as file:
                for line in lines:
                    file.write(line)

if __name__ == '__main__':
    dealFile()