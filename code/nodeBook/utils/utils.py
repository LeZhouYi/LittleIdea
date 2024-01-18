
def createKey(key:str,*args)->str:
    """创建Key"""
    for value in args:
        key=key+"_"+str(value)
    return key

def isEmpty(value:str)->bool:
    """判断字符串是否为空"""
    return value==None or value=="" or value==[]