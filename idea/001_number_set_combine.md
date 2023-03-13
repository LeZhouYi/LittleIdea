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