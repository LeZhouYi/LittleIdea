# 数集组合

## 问题一
给定一个数集numberList，求n个数自由组合的所有可能的集

### 设定
1.设定数集numberList中的数字不重复，且len(numberList)>=2;组合数为combineCount(>=1)

### 实现

#### 一、主逻辑实现
1. 存储所有组合可能的集为combineList
2. 存储当前遍历下标的集为indexList，且len == combineCount，初始值为0，1，2依次递增
3. 开始循环，直至indexList(0) == len(numberList)-combineCount；
    (1) 将当前indexList所指的数作为一次组合添加进combineList中。
    (2) 执行indexList的自增
4. 循环结束，将当前indexList所指的数作为一次组合添加进combineList中，
5. 返回组合集combineList

#### 二、indexList的自增
1. 开始循环，从0到组合减1，变量名为time
2. 若当前位的下标值指的不是最后一位，且后一位的下标不等于当前下标值+1，则自增；后续的下标值为当前值递增
3. 若是最后一位，则访问前一位

#### 三、代码
```python 3.10
import copy

def getCombination(numberList:list[int],combineCount:int)->list:
    '''
    给定一个数集numberList，求combineCount个数自由组合的所有可能的集
    eg:
        getCombination(numberList=[100,101,102],combineCount=2)
    '''
    if len(numberList)<combineCount: #不符合组合条件
        return None
    if combineCount<=1: #已组合或不用组合
        return copy.deepcopy(numberList)
    combineList = []
    indexList = [i for i in range(combineCount)]
    while indexList[0]<len(numberList)-combineCount:
        combineList.append([numberList[i] for i in indexList])
        #indexList自增
        tIndex = combineCount-1 #index当前处理的下标
        while tIndex>=0:
            if tIndex == combineCount-1: #最后一项
                if indexList[tIndex]< len(numberList)-1:
                    indexList[tIndex]+=1 #自增成功
                    break
                else:
                    tIndex-=1 #自增失败，切换至上一个下标处理
            else: #非最后一项
                if indexList[tIndex]<indexList[tIndex+1]-1: #可自增
                    teIndexValue = indexList[tIndex]
                    for addIndex in range(combineCount-tIndex):
                        indexList[tIndex+addIndex]=teIndexValue+1+addIndex #当前及后续下标顺序递增
                    break
                else: #不可自增
                    tIndex-=1
    combineList.append([numberList[i] for i in indexList])
    return combineList
```

## 问题二
给定一个数集numberList，求数集所有数字按任意顺序排列的所有可能的集

### 设定

1. 设定数集numberList的数字不重复，且len(numberList)>=2
2. 其余情况则返回本身或None

### 实现

#### 一、主逻辑实现

1. 存储所有排列可能的集为combineList，length=len(numberList)
2. 临时存储过程可能的组合集为tempStack,tempStack2
3. 将[numberList[0]]添加进tempStack
4. 开始循环，从1到length-1，变量名为index:
5. 依次遍历tempStack中的所有组合，变量为tempBind:
6. [numberList[index]].extend(tempBind)并将该数列添加进tempStack2
7. 开始循环，从0到index-1，且0!=index，变量为insertIndex:
8. 将tempBind拷贝并将numList[index]插入至tempBind的insertIndex位置上，并将结果添加至tempStack2
9. 将tempBind.extend([numberList[index]])并将该数列添加进tempStack2
10. 结束insertIndex的循环
11. 结束tempStack的循环
11. 将tempStack2的数据拷贝到tempStack,并清空tempStack2
12. 结束index的循环

#### 二、主要想法

1. numberList=[1]时，结果=```[[1]]```
2. numberList=[1,2]时，结果=```[[1,2],[2,1]]```
3. 以此类推，即第n个的组合排序为第n-1个的组合排序插入新的数字组合形成

#### 三、代码实现

```python 3.10
def getNumberOrderlyCombine(numberList:list[int])->list|None:
    if numberList==None or len(numberList)<=1:
        return numberList
    length = len(numberList)
    combineList = []
    tempStack,tempStack2 = [],[]
    for index in range(length):
        if index==0:
            tempStack.append([numberList[index]])
            continue
        for tempList in tempStack:
            for insertIndex in range(index+1):
                tempCombine = copy.deepcopy(tempList)
                tempCombine.insert(insertIndex,numberList[index])
                tempStack2.append(tempCombine)
        tempStack = tempStack2
        tempStack2 = []
    combineList.extend(tempStack)
    return combineList
```