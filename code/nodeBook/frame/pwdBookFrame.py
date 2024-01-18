import tkinter as tk
from utils import utils
from config.pwdbook import PwdBook
from frame.baseFrame import BaseFrame
from control.event import Event, WmEvent
from control.controller import Controller

"""密码内容页"""
class PwdBookFrame(BaseFrame):

    def __init__(self,controller:Controller) -> None:
        super().__init__(controller)
        self.passwordBook = PwdBook(self.getConfig().getPwdBook())

    def loadPasswordNote(self,contentFrameKey:str)->None:
        """加载密码本页面"""
        contentFrame = self.getWidget(contentFrameKey)
        pwdDispalyFrame = tk.Frame(
            contentFrame, cnf=self.getCnf("pwdDispalyFrame")
        )
        pwdScrollCanvas = tk.Canvas(
            pwdDispalyFrame, cnf=self.getCnf("pwdScrollCanvas")
        )
        pwdContentFrame = tk.Frame(
            pwdScrollCanvas, cnf=self.getCnf("pwdContentFrame")
        )
        pwdScrollBar = tk.Scrollbar(pwdDispalyFrame,self.getCnf("pwdScrollBar"))

        pwdScrollCanvas.config(yscrollcommand=pwdScrollBar.set,yscrollincrement=5)
        pwdScrollBar.config(command=pwdScrollCanvas.yview) #绑定滚动

        self.cacheWidget(pwdDispalyFrame, contentFrameKey, "pwdDispalyFrame")
        self.cacheWidget(pwdScrollCanvas, "pwdDispalyFrame", "pwdScrollCanvas")
        self.cacheWidget(pwdContentFrame, "pwdScrollCanvas", "pwdContentFrame")
        self.cacheWidget(pwdScrollBar,"pwdDispalyFrame","pwdScrollBar")

        frameCount = 0
        for groupKey in self.passwordBook.getGroupKeys():
            pwdSingleFrameKey = utils.createKey("pwdSingleFrame",frameCount)
            pwdGroupLabelKey = utils.createKey("pwdGroupLabel",frameCount)

            pwdSingleFrame = tk.Frame(
                pwdContentFrame, cnf=self.getCnf(pwdSingleFrameKey)
            )
            pwdGroupLabel = tk.Label(
                pwdSingleFrame, text=groupKey, cnf=self.getCnf(pwdGroupLabelKey)
            )
            self.cacheWidget(pwdSingleFrame, "pwdContentFrame", pwdSingleFrameKey)
            self.cacheWidget(pwdGroupLabel, "pwdContentFrame", pwdGroupLabelKey)

            group = self.passwordBook.getGroup(groupKey)
            envconut = 0
            for envkey, pwdList in group.items():
                pwdEnvFrameKey =utils.createKey("pwdEnvFrame",frameCount,envconut)
                pwdEmptyKey = utils.createKey("pwdEmptyLabel",frameCount,envconut)
                pwdEnvKey = utils.createKey("pwdEnvLabel",frameCount,envconut)

                pwdEnvFrame = tk.Frame(pwdSingleFrame,cnf=self.getCnf(pwdEnvFrameKey))
                pwdEmptyLabel = tk.Label(pwdEnvFrame,cnf=self.getCnf(pwdEmptyKey))
                pwdEnvLabel = tk.Label(pwdEnvFrame,text=envkey,cnf=self.getCnf(pwdEnvKey))

                self.cacheWidget(pwdEnvFrame,pwdSingleFrameKey,pwdEnvFrameKey)
                self.cacheWidget(pwdEmptyLabel,pwdEnvFrameKey,pwdEmptyKey)
                self.cacheWidget(pwdEnvLabel,pwdEnvFrameKey,pwdEnvKey)

                pwdCount = 0
                for pwdData in pwdList:
                    pwdDataFrameKey = utils.createKey("pwdDataFrame",frameCount,envconut,pwdCount)
                    pwdDataFrame = tk.Frame(pwdEnvFrame,cnf=self.getCnf(pwdDataFrameKey))
                    self.cacheWidget(pwdDataFrame,pwdEnvFrameKey,pwdDataFrameKey)

                    pwdKeyCount = 0
                    for pwdKey,pwdValue  in pwdData.items():
                        if not utils.isEmpty(pwdValue):
                            pwdItemFrameKey = utils.createKey("pwdItemFrame",frameCount,envconut,pwdCount,pwdKeyCount)
                            pwdItemLabelKey = utils.createKey("pwdItemLabel",frameCount,envconut,pwdCount,pwdKeyCount)
                            pwdItemValueKey = utils.createKey("pwdItemValue",frameCount,envconut,pwdCount,pwdKeyCount)

                            pwdItemFrame = tk.Frame(pwdDataFrame,cnf=self.getCnf(pwdItemFrameKey))
                            pwdItemLabel = tk.Label(pwdItemFrame,text=pwdKey,cnf=self.getCnf(pwdItemLabelKey))

                            self.cacheWidget(pwdItemFrame,pwdDataFrameKey,pwdItemFrameKey)
                            self.cacheWidget(pwdItemLabel,pwdItemFrameKey,pwdItemLabelKey)

                            if pwdKey== "labels":
                                labelCount=0
                                for pwdLabel in pwdValue:
                                    pwdValueLabelKey = utils.createKey("pwdValueLabel",frameCount,envconut,pwdCount,pwdKeyCount,labelCount)
                                    pwdValueLabel = tk.Label(pwdItemFrame,text=pwdLabel,cnf=self.getCnf(pwdValueLabelKey))
                                    self.cacheWidget(pwdValueLabel,pwdItemFrameKey,pwdValueLabelKey)
                                    labelCount+=1
                            else:
                                pwdItemValue = tk.Entry(pwdItemFrame,cnf=self.getCnf(pwdItemValueKey))
                                pwdItemValue.insert(tk.END,pwdValue)
                                pwdItemValue.config(state="readonly")
                                self.cacheWidget(pwdItemValue,pwdItemFrameKey,pwdItemValueKey)


                        pwdKeyCount+=1

                    pwdCount+=1
                envconut+=1
            frameCount += 1

        self.refreshCanvas()