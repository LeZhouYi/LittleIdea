from treeNode import TreeNode
from copy import deepcopy

level = {
	"+":0,
	"-":0,
	"*":1,
	"/":1
}

transMap = {
	"+":"-",
	"-":"+",
	"*":"/",
	"/":"*"
}

def main():
    data={
        "pattern":"a/b-f*g=c+d",
        "keys":[
            {
                "a":"13"
            },
            {
                "b":"#"
            },
            {
                "c":"13"
            },
            {
                "e":"13"
            },
            {
                "d":"13"
            },
            {
                "f":"13"
            },
            {
                "g":"13"
            },
            {
                "h":"#"
            }
        ]
    }
    calSourceStr = data["pattern"]
    calSourceList = str(calSourceStr).split("=")
    keys = getResultKeys(data)
    valueCalIndexs = getValueIndexs(calSourceList,keys) #获得不包含答案的算式的下标
    resultCalIndexs = getResultIndexs(calSourceList,keys) #获得包含答案的算式的下标

    assert len(valueCalIndexs)>0,"需要至少存在一个不包含答案的算式"

    valueCalStr = calSourceList[valueCalIndexs[0]] #获取不包含答案的算式

    for resultCalIndex in resultCalIndexs:
        resultCalStr = calSourceList[resultCalIndex] #获取包含答案的算式
        reulstKey = getResultKey(resultCalStr,keys) #获取原等式中要算出答案的Key
        resultCalTree = getCalTree(resultCalStr) #获得算术表达式的树
        valueCalTemp = deepcopy(valueCalStr) #构造属于当前答案的等式

        treeNode = resultCalTree[0] #获得根节点
        while(True):
            if treeNode!=None and isinstance(treeNode,TreeNode):
                if treeNode.getValue()==reulstKey:
                    break #等于要算出答案的Key，则表示完成算式的转换
                assert treeNode.getValue() in transMap,"算术运算符必需存在"
                if containElement(treeNode.left(),reulstKey):
                    #要算的答案在左子树
                    if treeNode.getValue()=="+":
                        valueCalTemp = "(%s)-%s"%(valueCalTemp,getCalStr(treeNode.right()))
                    elif treeNode.getValue()=="-":
                        valueCalTemp = "%s-(%s)"%(getCalStr(treeNode.right()),valueCalTemp)
                    elif treeNode.getValue()=="*":
                        valueCalTemp = "(%s)/%s"%(valueCalTemp,getCalStr(treeNode.right()))
                    elif treeNode.getValue()=="/":
                        valueCalTemp = "%s/(%s)"%(getCalStr(treeNode.right()),valueCalTemp)
                    treeNode = treeNode.left()
                else:
                    #要算的答案在右子树
                    if treeNode.getValue()=="+":
                        valueCalTemp = "(%s)-%s"%(valueCalTemp,getCalStr(treeNode.left()))
                    elif treeNode.getValue()=="-":
                        valueCalTemp = "(%s)+%s"%(valueCalTemp,getCalStr(treeNode.left()))
                    elif treeNode.getValue()=="*":
                        valueCalTemp = "(%s)/%s"%(valueCalTemp,getCalStr(treeNode.left()))
                    elif treeNode.getValue()=="/":
                        valueCalTemp = "(%s)*%s"%(valueCalTemp,getCalStr(treeNode.left()))
                    treeNode = treeNode.right()
            else:
                break
        print(valueCalTemp)

def getCalStr(treeNode:TreeNode):
    """中序遍历，输出算术表达式"""
    if treeNode.left()==None or treeNode.right()==None:
        return treeNode.getValue()
    return "("+getCalStr(treeNode.right())+str(treeNode.getValue())+getCalStr(treeNode.left())+")"

def deepCalStr(treeNode:TreeNode):
    """将树的每一层输出出来"""
    calTreeStack = [treeNode]
    tempStack = []
    while(len(calTreeStack)>0):
        while(len(calTreeStack)>0):
            node = calTreeStack.pop()
            print(node.getValue())
            if node.left()!=None:
                print(node.left().getValue())
                tempStack.append(node.left())
            if node.right()!=None:
                print(node.right().getValue())
                tempStack.append(node.right())
        calTreeStack = deepcopy(tempStack)
        tempStack = []
        print("\n")

def containElement(treeNode:TreeNode,key):
    """树是否存在某值"""
    calTreeStack = [treeNode]
    while(len(calTreeStack)>0):
        node = calTreeStack.pop()
        if node.getValue() == key:
            return True
        else:
            if node.left()!=None:
                calTreeStack.append(node.left())
            if node.right()!=None:
                calTreeStack.append(node.right())
    return False

def getCalTree(calStr:str):
    """获得表达式树"""
    calStr = calStr.replace("{","(").replace("}",")").replace("[","(").replace("]",")")#将所有{}[]换成()
    suffixCalStr = getSuffixCal(calStr) #逆波兰表达式
    calTreeStack= [] #表达式树
    for char in suffixCalStr:
        if char not in level:
            calTreeStack.append(TreeNode(char)) #入栈
        else:
            parentNode = TreeNode(char).addLeftChild(calTreeStack.pop()).addRightChild(calTreeStack.pop())
            calTreeStack.append(parentNode)
    return calTreeStack

def getSuffixCal(calStr:str)->str:
    """将当前算术表达式转成逆波兰表达式"""
    suffixCalStr = "" #逆波兰表达式
    elementStack = [] #临时存储栈
    for char in calStr:
        if char == "(":
            elementStack.append(char) #左括号入栈
        elif char == ")":
            while(len(elementStack)>0):
                popElement = elementStack.pop()
                if popElement == "(":
                    break
                else:
                    suffixCalStr+=popElement #在碰到左括号前将所有元素放入表达式中
        elif char in level:
            if(len(elementStack)>0):
                while(len(elementStack)>0):
                    popElement = elementStack[-1] #读但不弹出
                    if popElement not in level: #非操作符，压入并终止
                        break
                    if level[popElement]>=level[char]:
                        popElement = elementStack.pop() #优先级大于或等于当前的弹出
                        suffixCalStr+=popElement
                    else:
                        break
            elementStack.append(char)
        else:
            suffixCalStr+=char
    while(len(elementStack)>0):
        suffixCalStr+=elementStack.pop()
    return suffixCalStr

def getResultKeys(data:dict):
    """获得所有答案的keys"""
    keys = []
    for key in data["keys"]:
        for teKey,teValue in key.items():
            if teValue == "#":
                keys.append(teKey)
    return keys

def getResultKey(resultCalStr,keys):
    """获取原等式中要算出答案的Key"""
    for key in keys:
        if str(resultCalStr).find(key)>=0:
            return key
    return None

def getValueIndexs(calSourceList,keys):
    #获得不包含答案的算式的下标
    indexs = []
    for i in range(len(calSourceList)):
        calStr = calSourceList[i]
        flags = False #标记当前是否有答案
        for key in keys:
            if str(calStr).find(key)>=0:
                flags = True
                break
        if not flags:
            indexs.append(i)
    return indexs

def getResultIndexs(calSourceList,keys):
    #获得包含答案的算式的下标
    indexs = []
    for i in range(len(calSourceList)):
        calStr = calSourceList[i]
        for key in keys:
            if str(calStr).find(key)>=0:
                indexs.append(i)
    return indexs

if __name__ == "__main__":
    main()