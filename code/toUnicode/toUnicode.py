import os

def createPath(path:str)->None:
    '''若文件路径不存在，则新建'''
    if not os.path.exists(path):
        os.makedirs(path)

def isChineseChar(char:str)->bool:
    """判断是否为中文字符"""
    if '\u2E80' <= char <= '\u2EF3':
        return True
    elif '\u2F00' <= char <= '\u2FD5':
        return True
    elif '\u3005' <= char <= '\u3029':
        return True
    elif '\u3038' <= char <= '\u4DB5':
        return True
    elif '\u4E00' <= char <= '\uFA6A':
        return True
    elif '\uFA70' <= char <= '\uFAD9':
        return True
    elif '\u20000' <= char <= '\u2FA1D':
        return True
    return False

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