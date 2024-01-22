import os
import tkinter as tk
from PIL import Image, ImageTk
from utils import utils
from config.pwdbook import PwdBook
from frame.baseFrame import BaseFrame
from control.event import Event, WmEvent
from control.controller import Controller

"""密码内容页"""


class PwdBookFrame(BaseFrame):
    def __init__(self, controller: Controller) -> None:
        super().__init__(controller)
        self.passwordBook = PwdBook(self.getConfig().getPwdBook())
        self.loadIcon()
        self.checkPwdData()

    def loadIcon(self):
        """加载图片资源"""
        iconPaths = os.path.join(os.getcwd(), self.getConfig().getPwdIconPath())
        for fileName in os.listdir(iconPaths):
            if utils.isPhoto(fileName):
                iconfile = os.path.join(iconPaths, fileName)
                image = Image.open(iconfile).resize(self.getConfig().getpwdIconSize())
                image = ImageTk.PhotoImage(image)
                self.cacheImage(image, utils.getFileName(fileName), "pwdbookIcon")

    def checkPwdData(self) -> None:
        """检查密码本数据，若无数据则加入默认数据"""
        if len(self.passwordBook.getGroupKeys()) == 0:
            self.passwordBook.addGroup("default")

    ###########控件事件################
    def clickDeleteGroup(self, event, eventInfo: dict):
        """点击删除组事件"""
        self.passwordBook.deletetGroup(eventInfo["groupKey"])
        self.passwordBook.writeToFile()
        self.destroyWidget(eventInfo["widget"])
        self.closeDialog(event, eventInfo["dialogKey"])

        self.updateCanvas(
            self.getWidget("pwdScrollCanvas"),
            self.getWidget("pwdContentFrame"),
            "pwdDispalyFrame",
        )

    def clickDeleteEnv(self, event, eventInfo: dict):
        """点击删除环境事件"""
        self.passwordBook.deletetEnv(eventInfo["groupKey"], eventInfo["envKey"])
        self.passwordBook.writeToFile()
        self.destroyWidget(eventInfo["widget"])
        self.closeDialog(event, eventInfo["dialogKey"])

        self.updateCanvas(
            self.getWidget("pwdScrollCanvas"),
            self.getWidget("pwdContentFrame"),
            "pwdDispalyFrame",
        )

    def closeDialog(self, event, dialogKey: str):
        """关闭提示框事件"""
        self.destroyWidget(dialogKey)

    ###########渲染相关################
    def loadDeleteDialog(
        self,
        event,
        eventInfo: dict,
    ) -> None:
        """加载删除提示框"""
        mainWindow = self.getWidget("baseWindow")
        pwdDeleteDialog = tk.Toplevel(mainWindow, cnf=self.getCnf("pwdDeleteDialog"))
        pwdDeleteDialog.title("")
        mainWindow.update_idletasks()
        pwdDeleteDialog.transient(mainWindow)
        pwdDeleteDialog.grab_set()
        winX = (
            mainWindow.winfo_rootx()
            + (mainWindow.winfo_width() // 2)
            - (pwdDeleteDialog.winfo_width() // 2)
        )
        winY = (
            mainWindow.winfo_rooty()
            + (mainWindow.winfo_height() // 2)
            - (pwdDeleteDialog.winfo_height() // 2)
        )
        pwdDeleteDialog.geometry("+{}+{}".format(winX, winY))
        pwdDeleteDialog.bind(
            WmEvent.WindowClose,
            utils.eventAdaptor(self.closeDialog, dialogKey="pwdDeleteDialog"),
        )

        pwdDelDlgFrame = tk.Frame(pwdDeleteDialog, cnf=self.getCnf("pwdDelDlgFrame"))
        pwdDelDlgLabel = tk.Label(
            pwdDelDlgFrame, text="请确认是否删除", cnf=self.getCnf("pwdDelDlgLabel")
        )
        pwdDelDlgYesBtn = tk.Label(
            pwdDelDlgFrame, text="确定", cnf=self.getCnf("pwdDelDlgYesBtn")
        )
        pwdDelDlgNoBtn = tk.Label(
            pwdDelDlgFrame, text="取消", cnf=self.getCnf("pwdDelDlgNoBtn")
        )

        eventInfo["dialogKey"] = "pwdDeleteDialog"

        pwdDelDlgYesBtn.bind(
            Event.MouseLeftClick,
            utils.eventAdaptor(eventInfo["method"], eventInfo=eventInfo),
        )
        pwdDelDlgNoBtn.bind(
            Event.MouseLeftClick,
            utils.eventAdaptor(self.closeDialog, dialogKey="pwdDeleteDialog"),
        )

        self.cacheWidget(pwdDeleteDialog, "baseWindow", "pwdDeleteDialog")
        self.cacheWidget(pwdDelDlgFrame, "pwdDeleteDialog", "pwdDelDlgFrame")
        self.cacheWidget(pwdDelDlgLabel, "pwdDelDlgFrame", "pwdDelDlgLabel")
        self.cacheWidget(pwdDelDlgYesBtn, "pwdDelDlgFrame", "pwdDelDlgYesBtn")
        self.cacheWidget(pwdDelDlgNoBtn, "pwdDelDlgFrame", "pwdDelDlgNoBtn")

        mainWindow.wait_window(pwdDeleteDialog)

    def loadPasswordNote(self, contentFrameKey: str) -> None:
        """加载密码本页面"""
        contentFrame = self.getWidget(contentFrameKey)
        pwdDispalyFrame = tk.Frame(contentFrame, cnf=self.getCnf("pwdDispalyFrame"))
        pwdScrollCanvas = tk.Canvas(pwdDispalyFrame, cnf=self.getCnf("pwdScrollCanvas"))
        pwdContentFrame = tk.Frame(pwdScrollCanvas, cnf=self.getCnf("pwdContentFrame"))
        pwdScrollBar = tk.Scrollbar(pwdDispalyFrame, self.getCnf("pwdScrollBar"))

        pwdScrollCanvas.config(yscrollcommand=pwdScrollBar.set, yscrollincrement=5)
        pwdScrollBar.config(command=pwdScrollCanvas.yview)  # 绑定滚动

        self.cacheWidget(pwdDispalyFrame, contentFrameKey, "pwdDispalyFrame")
        self.cacheWidget(pwdScrollCanvas, "pwdDispalyFrame", "pwdScrollCanvas")
        self.cacheWidget(pwdContentFrame, "pwdScrollCanvas", "pwdContentFrame")
        self.cacheWidget(pwdScrollBar, "pwdDispalyFrame", "pwdScrollBar")

        frameCount = 0
        for groupKey in self.passwordBook.getGroupKeys():
            pwdSingleFrameKey = utils.createKey("pwdSingleFrame", frameCount)
            pwdGroupLineKey = utils.createKey("pwdGroupLine", frameCount)
            pwdGroupLabelKey = utils.createKey("pwdGroupLabel", frameCount)
            pwdGroupPackBtnKey = utils.createKey("pwdGroupPackBtn", frameCount)
            pwdGroupAddBtnKey = utils.createKey("pwdGroupAddBtn", frameCount)
            pwdGroupEditBtnKey = utils.createKey("pwdGroupEditBtn", frameCount)
            pwdGroupDelBtnKey = utils.createKey("pwdGroupDelBtn", frameCount)

            pwdSingleFrame = tk.Frame(
                pwdContentFrame, cnf=self.getCnf(pwdSingleFrameKey)
            )
            pwdGroupLineFrame = tk.Frame(
                pwdSingleFrame, cnf=self.getCnf(pwdGroupLineKey)
            )
            pwdGroupLabel = tk.Label(
                pwdGroupLineFrame, text=groupKey, cnf=self.getCnf(pwdGroupLabelKey)
            )
            pwdGroupAddBtn = tk.Label(
                pwdGroupLineFrame,
                image=self.getImage("add", "pwdbookIcon"),
                cnf=self.getCnf(pwdGroupAddBtnKey),
            )
            pwdGroupPackBtn = tk.Label(
                pwdGroupLineFrame,
                image=self.getImage("pack", "pwdbookIcon"),
                cnf=self.getCnf(pwdGroupPackBtnKey),
            )
            pwdGroupEditBtn = tk.Label(
                pwdGroupLineFrame,
                image=self.getImage("edit", "pwdbookIcon"),
                cnf=self.getCnf(pwdGroupEditBtnKey),
            )
            pwdGroupDelBtn = tk.Label(
                pwdGroupLineFrame,
                image=self.getImage("delete", "pwdbookIcon"),
                cnf=self.getCnf(pwdGroupDelBtnKey),
            )

            pwdGroupDelBtn.bind(
                Event.MouseLeftClick,
                utils.eventAdaptor(
                    self.loadDeleteDialog,
                    eventInfo={
                        "groupKey": groupKey,
                        "widget": pwdSingleFrameKey,
                        "method": self.clickDeleteGroup,
                    },
                ),
            )

            self.cacheWidget(pwdSingleFrame, "pwdContentFrame", pwdSingleFrameKey)
            self.cacheWidget(pwdGroupLineFrame, pwdSingleFrameKey, pwdGroupLineKey)
            self.cacheWidget(pwdGroupPackBtn, pwdGroupLineKey, pwdGroupPackBtnKey)
            self.cacheWidget(pwdGroupAddBtn, pwdGroupLineKey, pwdGroupAddBtnKey)
            self.cacheWidget(pwdGroupEditBtn, pwdGroupLineKey, pwdGroupEditBtnKey)
            self.cacheWidget(pwdGroupDelBtn, pwdGroupLineKey, pwdGroupDelBtnKey)
            self.cacheWidget(pwdGroupLabel, pwdGroupLineKey, pwdGroupLabelKey)

            group = self.passwordBook.getGroup(groupKey)
            envconut = 0
            for envkey, pwdList in group.items():
                pwdEnvFrameKey = utils.createKey("pwdEnvFrame", frameCount, envconut)
                pwdEnvLineKey = utils.createKey("pwdEnvLineFrame", frameCount, envconut)
                pwdEmptyKey = utils.createKey("pwdEmptyLabel", frameCount, envconut)
                pwdEnvKey = utils.createKey("pwdEnvLabel", frameCount, envconut)
                pwdEnvPackKey = utils.createKey("pwdEnvPackBtn", frameCount, envconut)
                pwdEnvAddKey = utils.createKey("pwdEnvAddBtn", frameCount, envconut)
                pwdEnvEditKey = utils.createKey("pwdEnvEditBtn", frameCount, envconut)
                pwdEnvDelKey = utils.createKey("pwdEnvDelBtn", frameCount, envconut)

                pwdEnvFrame = tk.Frame(pwdSingleFrame, cnf=self.getCnf(pwdEnvFrameKey))
                pwdEnvLineFrame = tk.Frame(pwdEnvFrame, cnf=self.getCnf(pwdEnvLineKey))
                pwdEmptyLabel = tk.Label(pwdEnvFrame, cnf=self.getCnf(pwdEmptyKey))
                pwdEnvLabel = tk.Label(
                    pwdEnvLineFrame, text=envkey, cnf=self.getCnf(pwdEnvKey)
                )
                pwdEnvPackBtn = tk.Label(
                    pwdEnvLineFrame,
                    image=self.getImage("pack", "pwdbookIcon"),
                    cnf=self.getCnf(pwdEnvPackKey),
                )
                pwdEnvAddBtn = tk.Label(
                    pwdEnvLineFrame,
                    image=self.getImage("add", "pwdbookIcon"),
                    cnf=self.getCnf(pwdEnvAddKey),
                )
                pwdEnvEditBtn = tk.Label(
                    pwdEnvLineFrame,
                    image=self.getImage("edit", "pwdbookIcon"),
                    cnf=self.getCnf(pwdEnvEditKey),
                )
                pwdEnvDelBtn = tk.Label(
                    pwdEnvLineFrame,
                    image=self.getImage("delete", "pwdbookIcon"),
                    cnf=self.getCnf(pwdEnvDelKey),
                )

                pwdEnvDelBtn.bind(
                    Event.MouseLeftClick,
                    utils.eventAdaptor(
                        self.loadDeleteDialog,
                        eventInfo={
                            "groupKey": groupKey,
                            "envKey": envkey,
                            "widget": pwdEnvFrameKey,
                            "method": self.clickDeleteEnv,
                        },
                    ),
                )

                self.cacheWidget(pwdEnvFrame, pwdSingleFrameKey, pwdEnvFrameKey)
                self.cacheWidget(pwdEmptyLabel, pwdEnvFrameKey, pwdEmptyKey)
                self.cacheWidget(pwdEnvLineFrame, pwdEnvFrameKey, pwdEnvLineKey)
                self.cacheWidget(pwdEnvPackBtn, pwdEnvLineKey, pwdEnvPackKey)
                self.cacheWidget(pwdEnvAddBtn, pwdEnvLineKey, pwdEnvAddKey)
                self.cacheWidget(pwdEnvEditBtn, pwdEnvLineKey, pwdEnvEditKey)
                self.cacheWidget(pwdEnvDelBtn, pwdEnvLineKey, pwdEnvDelKey)
                self.cacheWidget(pwdEnvLabel, pwdEnvLineKey, pwdEnvKey)

                pwdCount = 0
                for pwdData in pwdList:
                    pwdDataFrameKey = utils.createKey(
                        "pwdDataFrame", frameCount, envconut, pwdCount
                    )
                    pwdDataFrame = tk.Frame(
                        pwdEnvFrame, cnf=self.getCnf(pwdDataFrameKey)
                    )
                    self.cacheWidget(pwdDataFrame, pwdEnvFrameKey, pwdDataFrameKey)

                    pwdKeyCount = 0
                    for pwdKey, pwdValue in pwdData.items():
                        if (
                            not utils.isEmpty(pwdValue) and pwdKey != "id"
                        ) or pwdKey == "labels":
                            pwdItemFrameKey = utils.createKey(
                                "pwdItemFrame",
                                frameCount,
                                envconut,
                                pwdCount,
                                pwdKeyCount,
                            )
                            pwdItemLabelKey = utils.createKey(
                                "pwdItemLabel",
                                frameCount,
                                envconut,
                                pwdCount,
                                pwdKeyCount,
                            )
                            pwdItemValueKey = utils.createKey(
                                "pwdItemValue",
                                frameCount,
                                envconut,
                                pwdCount,
                                pwdKeyCount,
                            )
                            pwdItemCopyKey = utils.createKey(
                                "pwdItemCopyBtn",
                                frameCount,
                                envconut,
                                pwdCount,
                                pwdKeyCount,
                            )

                            pwdItemFrame = tk.Frame(
                                pwdDataFrame, cnf=self.getCnf(pwdItemFrameKey)
                            )
                            pwdItemLabel = tk.Label(
                                pwdItemFrame,
                                text=pwdKey,
                                cnf=self.getCnf(pwdItemLabelKey),
                            )

                            self.cacheWidget(
                                pwdItemFrame, pwdDataFrameKey, pwdItemFrameKey
                            )
                            self.cacheWidget(
                                pwdItemLabel, pwdItemFrameKey, pwdItemLabelKey
                            )

                            if pwdKey == "labels":
                                labelCount = 0
                                for pwdLabel in pwdValue:
                                    pwdValueLabelKey = utils.createKey(
                                        "pwdValueLabel",
                                        frameCount,
                                        envconut,
                                        pwdCount,
                                        pwdKeyCount,
                                        labelCount,
                                    )
                                    pwdValueLabel = tk.Label(
                                        pwdItemFrame,
                                        text=pwdLabel,
                                        cnf=self.getCnf(pwdValueLabelKey),
                                    )
                                    self.cacheWidget(
                                        pwdValueLabel, pwdItemFrameKey, pwdValueLabelKey
                                    )
                                    labelCount += 1
                                pwdValueEditKey = utils.createKey(
                                    "pwdValueEditBtn",
                                    frameCount,
                                    envconut,
                                    pwdCount,
                                    pwdKeyCount,
                                )
                                pwdValueDelKey = utils.createKey(
                                    "pwdValueDelBtn",
                                    frameCount,
                                    envconut,
                                    pwdCount,
                                    pwdKeyCount,
                                )
                                pwdValueEditBtn = tk.Label(
                                    pwdItemFrame,
                                    image=self.getImage("edit", "pwdbookIcon"),
                                    cnf=self.getCnf(pwdValueEditKey),
                                )
                                pwdValueDelBtn = tk.Label(
                                    pwdItemFrame,
                                    image=self.getImage("delete", "pwdbookIcon"),
                                    cnf=self.getCnf(pwdValueDelKey),
                                )
                                self.cacheWidget(
                                    pwdValueEditBtn, pwdItemFrameKey, pwdValueEditKey
                                )
                                self.cacheWidget(
                                    pwdValueDelBtn, pwdItemFrameKey, pwdValueDelKey
                                )
                            elif pwdKey == "website":
                                pwdItemValue = tk.Entry(
                                    pwdItemFrame, cnf=self.getCnf(pwdItemValueKey)
                                )
                                pwdItemValue.insert(tk.END, pwdValue)
                                pwdItemValue.config(state="readonly")
                                pwdItemBrowserBtn = tk.Label(
                                    pwdItemFrame,
                                    image=self.getImage("browser", "pwdbookIcon"),
                                    cnf=self.getCnf(pwdItemCopyKey),
                                )

                                self.cacheWidget(
                                    pwdItemBrowserBtn, pwdItemFrameKey, pwdItemCopyKey
                                )
                                self.cacheWidget(
                                    pwdItemValue, pwdItemFrameKey, pwdItemValueKey
                                )
                            else:
                                pwdItemValue = tk.Entry(
                                    pwdItemFrame, cnf=self.getCnf(pwdItemValueKey)
                                )
                                pwdItemValue.insert(tk.END, pwdValue)
                                pwdItemValue.config(state="readonly")
                                pwdItemCopyBtn = tk.Label(
                                    pwdItemFrame,
                                    image=self.getImage("copy", "pwdbookIcon"),
                                    cnf=self.getCnf(pwdItemCopyKey),
                                )

                                self.cacheWidget(
                                    pwdItemCopyBtn, pwdItemFrameKey, pwdItemCopyKey
                                )
                                self.cacheWidget(
                                    pwdItemValue, pwdItemFrameKey, pwdItemValueKey
                                )
                        pwdKeyCount += 1
                    pwdCount += 1
                envconut += 1
            frameCount += 1

        self.refreshCanvas()
