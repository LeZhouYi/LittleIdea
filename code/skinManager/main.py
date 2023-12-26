import os
import sys
import utils
import shutil
import tkinter as tk
import datetime
import mss
from tkinter.filedialog import askdirectory
from manager import Manager
from PIL import Image, ImageTk
from tkinter import ttk
from threading import Thread
from time import sleep
from data import RoleKey, FrameConfig, Event


class MainFrame:
    def __init__(self):
        self.manager = Manager()  # 数据
        self.mainWindow = tk.Tk()  # 主窗口

        # 基本配置
        self.initWindow()
        self.initFrameData()  # 初始化数据
        self.initWidgetPool()  # 初始化控件池
        self.initMainFrame()  # 初始化第一层
        self.initSideBar()  # 初始化侧边栏
        self.switchSideBar(None)  # 隐藏侧边栏
        self.initSkinManager()  # 初始化皮肤管理页面
        self.initRoleListPage()  # 初始化角色选择列表页面
        self.updateRoleList()  # 更新角色列表页面
        self.mainWindow.mainloop()  # 显示窗口

    ####################init&update############################
    # Init表示只会执行一次
    # Update表示会清空相关页面内容并重新渲染

    def initWindow(self):
        """初始化窗口"""
        self.mainWindow.title(FrameConfig.frameTitle)
        self.mainWindow.geometry("1536x828-1530+0")
        # self.mainWindow.attributes("-fullscreen", True)  # 全屏
        self.mainWindow.bind(Event.F4, self.close)  # F4退出程序
        self.mainWindow.bind(Event.Escape, self.backPage)
        self.mainWindow.bind(Event.Tab, self.switchSideBar)  # 切换侧边栏

    def initFrameData(self):
        """初始化框架相关数据"""
        self.sideBarSwitch = True  # 默认展开侧边栏
        self.roleImagePool = {}  # 角色图片池
        self.selectRoleKey = None  # 当前选择的角色
        self.skinImagePool = []  # 角色皮肤图片池
        self.skinThread = None  # 加载皮肤的线程
        self.skinThreadStopSymbol = False  # 标志正在等待线程结束
        self.page = "RoleListPage"  # 当前查看页

    def initWidgetPool(self):
        """初始化控件池"""
        self.widgetPool = {}

    def initMainFrame(self):
        """初始化第一层控件"""
        sideBarFrame = tk.Frame(self.getMainFrame(), background="white")  # 侧边栏
        contentFrame = tk.Frame(self.getMainFrame(), background="white")  # 内容页

        sideBarFrame.pack(side=tk.LEFT, fill=tk.Y, ipady=3)
        contentFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.addWidgetInPool(sideBarFrame, "sideBar")  # 缓存
        self.addWidgetInPool(contentFrame, "content")

    def initSideBar(self):
        """初始化侧边栏"""
        sideBarFrame = self.getWidgetFromPool("sideBar")  # 侧边栏框架

        sideBarCanvas = tk.Canvas(sideBarFrame, background="white")  # 侧边栏画布
        sideBarScroll = tk.Scrollbar(
            sideBarFrame, orient=tk.VERTICAL, width=2, background="white"
        )  # 侧边栏竖向滚动条
        sideBarScrollFrame = tk.Frame(sideBarCanvas, background="white", borderwidth=5)
        skinManagerBtn = tk.Button(
            sideBarScrollFrame, text="皮肤管理", font=FrameConfig.font, width=15
        )

        sideBarCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        sideBarScroll.pack(side=tk.RIGHT, fill=tk.Y)
        skinManagerBtn.pack(side=tk.TOP, fill=tk.X)

        sideBarCanvas.config(
            yscrollcommand=sideBarScroll.set, yscrollincrement=1
        )  # 侧边栏画布关联竖直滚动条
        sideBarScroll.config(command=sideBarCanvas.yview)  # 滚动条关联画布y轴
        sideBarCanvas.create_window(0, 0, window=sideBarScrollFrame, anchor=tk.NW)
        sideBarScrollFrame.bind(
            "<MouseWheel>",
            utils.eventAdaptor(self.scrollVerticalCanvas, widget=sideBarCanvas),
        )  # 绑定画布的滚动事件

        self.updateScrollFrame(sideBarFrame, sideBarCanvas, sideBarScrollFrame)  # 更新并配置

        self.addWidgetInPool(sideBarCanvas, "sideBarCanvas")  # 缓存
        self.addWidgetInPool(sideBarScroll, "sideBarScroll")
        self.addWidgetInPool(sideBarScrollFrame, "sideBarFrame")
        self.addWidgetInPool(skinManagerBtn, "sideBarBtn")

    def updateScrollFrame(
        self, parentFrame: tk.Frame, scrollCanvas: tk.Canvas, contentFrame: tk.Frame
    ):
        """更新滚动画布内容并重新定义"""
        parentFrame.update()
        scrollCanvas.config(
            scrollregion=contentFrame.bbox(tk.ALL),
            width=contentFrame.winfo_width(),
            height=contentFrame.winfo_height(),
        )  # 设定画布可滚区域及自适应内容

    def initSkinManager(self):
        """初始化皮肤管理页面"""
        contentFrame = self.getWidgetFromPool("content")

        skinTitleFrame = tk.Frame(contentFrame, background="white")  # 显示皮肤标题一栏
        skinSourceFrame = tk.Frame(skinTitleFrame, background="white")  # 皮肤标题第一行
        skinSourceLabel = tk.Label(
            skinSourceFrame, text="皮肤库", font=FrameConfig.font, background="white"
        )
        skinSourceSetBtn = tk.Button(
            skinSourceFrame, text="更新", font=FrameConfig.font, background="white"
        )
        skinSource = tk.Label(
            skinSourceFrame,
            text=self.getSkinPathText(),
            font=FrameConfig.font,
            background="white",
        )

        skinTitleFrame.pack(side=tk.TOP, fill=tk.X)
        skinSourceFrame.pack(side=tk.TOP, fill=tk.X)
        skinSourceLabel.pack(side=tk.LEFT)
        skinSourceSetBtn.pack(side=tk.RIGHT)
        skinSource.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        skinSourceSetBtn.bind(
            Event.MouseLefClick,
            utils.eventAdaptor(self.clickUpdateFile, btn=skinSourceSetBtn),
        )
        skinSource.bind(Event.MouseLefClick, self.selectSkinSource)  # 选择皮肤路径事件

        self.addWidgetInPool(skinTitleFrame, "skinTitle")
        self.addWidgetInPool(skinSourceFrame, "skinTitleFrame")
        self.addWidgetInPool(skinSourceLabel, "skinTitleLabel")
        self.addWidgetInPool(skinSourceSetBtn, "skinSourceBtn")
        self.addWidgetInPool(skinSource, "skinSource")

        modSourceFrame = tk.Frame(skinTitleFrame, background="white")  # 皮肤标题第二行
        modSourceLabel = tk.Label(
            modSourceFrame, text="Mods", font=FrameConfig.font, background="white"
        )
        modSourceBtn = tk.Button(
            modSourceFrame, text="更新", font=FrameConfig.font, background="white"
        )
        modSource = tk.Label(
            modSourceFrame,
            text=self.getModPathText(),
            font=FrameConfig.font,
            background="white",
        )  # 3dmigoto目标路径

        modSourceFrame.pack(side=tk.TOP, fill=tk.X)
        modSourceLabel.pack(side=tk.LEFT)
        modSourceBtn.pack(side=tk.RIGHT)
        modSource.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        modSourceBtn.bind(
            Event.MouseLefClick,
            utils.eventAdaptor(self.clickUpdateFile, btn=modSourceBtn),
        )
        modSource.bind(Event.MouseLefClick, self.selectModSource)

        self.addWidgetInPool(modSourceFrame, "skinTitleFrame")
        self.addWidgetInPool(modSourceLabel, "skinTitleLabel")
        self.addWidgetInPool(modSourceBtn, "modSourceBtn")
        self.addWidgetInPool(modSource, "modSource")

        skinControlCanvas = tk.Canvas(contentFrame, background="white")  # 皮肤操作页面包管理
        skinControlFrame = tk.Frame(skinControlCanvas, background="white")  # 显示皮肤操作一栏
        roleSelectDisplay = tk.Label(
            skinControlFrame,
            image=self.getDefaultRoleImage(),
            background="white",
            width=FrameConfig.skinControlWidth,
        )  # 显示当前选择的角色图标
        roleSelectText = tk.Label(
            skinControlFrame,
            text=RoleKey.getRoleText(FrameConfig.defaultRoleKey),
            background="white",
            font=FrameConfig.font,
        )  # 显示当前选择的角色文本
        skinSelectFrame = tk.Frame(skinControlFrame, background="white")  # 已选皮肤一栏
        skinSelectLabel = tk.Label(
            skinSelectFrame, text="当前选择：", anchor=tk.NW, font=FrameConfig.font,background="white"
        )  # 已选皮肤标签
        skinSelectText = tk.Label(
            skinSelectFrame, text="", font=FrameConfig.font, background="white"
        )  # 已选皮肤文件名
        skinReplaceBtn = tk.Button(
            skinControlFrame, text="替换", font=FrameConfig.font, background="white"
        )  # 替换皮肤
        skinBeSetFrame = tk.Frame(skinControlFrame, background="white")  # 当前使用的皮肤
        skinBeSetLabel = tk.Label(
            skinBeSetFrame,
            text="当前使用：",
            anchor=tk.NW,
            font=FrameConfig.font,
            background="white",
        )  # 已使用皮肤标签
        skinBeSetText = tk.Label(
            skinBeSetFrame,
            text=self.getModsUseSkinText(FrameConfig.defaultRoleKey),
            font=FrameConfig.font,
            background="white",
        )  # 已使用皮肤文件名
        skinUseDeleteBtn = tk.Button(
            skinControlFrame, text="删除", font=FrameConfig.font, background="white"
        )  # 删除正在使用的皮肤
        catchScreenBtn = tk.Button(
            skinControlFrame, text="截图制作预览", font=FrameConfig.font, background="white"
        )  # 截图并作为皮肤预览图

        skinControlCanvas.pack(side=tk.LEFT, fill=tk.Y)
        skinControlFrame.pack(side=tk.LEFT, fill=tk.Y)
        roleSelectDisplay.pack(side=tk.TOP, fill=tk.X)
        roleSelectText.pack(side=tk.TOP, fill=tk.X)
        skinSelectFrame.pack(side=tk.TOP, fill=tk.X)
        skinSelectLabel.pack(side=tk.TOP, fill=tk.X)
        skinSelectText.pack(side=tk.TOP, fill=tk.X)
        skinReplaceBtn.pack(side=tk.TOP, fill=tk.X)
        catchScreenBtn.pack(side=tk.TOP, fill=tk.X)
        skinBeSetFrame.pack(side=tk.TOP, fill=tk.X)
        skinBeSetLabel.pack(side=tk.TOP, fill=tk.X)
        skinBeSetText.pack(side=tk.TOP, fill=tk.X)
        skinUseDeleteBtn.pack(side=tk.TOP, fill=tk.X)

        skinReplaceBtn.bind(
            Event.MouseLefClick, utils.eventAdaptor(self.clickReplaceSkin)
        )
        skinUseDeleteBtn.bind(Event.MouseLefClick, self.clickDeleteModSkin)
        catchScreenBtn.bind(Event.MouseLefClick, self.clickCreateSkinImage)

        self.addWidgetInPool(skinControlCanvas, "skinControlCanvas")
        self.addWidgetInPool(skinControlFrame, "skinControl")
        self.addWidgetInPool(roleSelectDisplay, "skinDisplay")
        self.addWidgetInPool(roleSelectText, "skinDisplayText")
        self.addWidgetInPool(skinSelectFrame, "skinDisplayFrame")
        self.addWidgetInPool(skinSelectLabel, "skinSelectLabel")
        self.addWidgetInPool(skinSelectText, "skinSelectText")
        self.addWidgetInPool(skinReplaceBtn, "skinDisplayReplace")
        self.addWidgetInPool(skinBeSetFrame, "skinDisplayFrame")
        self.addWidgetInPool(skinBeSetLabel, "skinSelectLabel")
        self.addWidgetInPool(skinBeSetText, "modsUseText")
        self.addWidgetInPool(skinUseDeleteBtn, "skinDisplayDelete")
        self.addWidgetInPool(catchScreenBtn, "catchScreen")

        self.hideSkinControl()

        roleListFrame = tk.Frame(contentFrame, background="white")  # 显示皮肤内容一栏
        roleListFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.addWidgetInPool(roleListFrame, "roleList")

    def initRoleListPage(self):
        """初始化角色列表页面"""
        roleListFrame = self.getWidgetFromPool("roleList")

        roleListCanvas = tk.Canvas(roleListFrame, background="white")  # 角色选择页面画布
        roleListScrollX = tk.Scrollbar(
            roleListFrame, orient=tk.HORIZONTAL, width=2, background="white"
        )  # 横向滚动条
        roleListScrollY = tk.Scrollbar(
            roleListFrame, orient=tk.VERTICAL, width=2, background="white"
        )  # 竖向滚动条
        roleListCanvas.config(
            xscrollcommand=roleListScrollX.set,
            xscrollincrement=1,
            yscrollcommand=roleListScrollY.set,
            yscrollincrement=1,
        )  # 画布关联滚动条
        roleListScrollX.config(command=roleListCanvas.xview)  # 滚动条关联画布
        roleListScrollY.config(command=roleListCanvas.yview)
        roleListScrollX.pack(side=tk.BOTTOM, fill=tk.X)
        roleListScrollY.pack(side=tk.RIGHT, fill=tk.Y)
        roleListCanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        roleListContentFrame = tk.Frame(
            roleListCanvas, background="white", borderwidth=5
        )
        roleListCanvas.create_window(0, 0, window=roleListContentFrame, anchor=tk.NW)
        roleListCanvas.bind(
            Event.MouseWheel,
            utils.eventAdaptor(self.scrollVerticalCanvas, widget=roleListCanvas),
        )

        self.updateScrollFrame(roleListFrame, roleListCanvas, roleListContentFrame)

        self.addWidgetInPool(roleListCanvas, "roleListCanvas")
        self.addWidgetInPool(roleListScrollX, "roleListScroll")
        self.addWidgetInPool(roleListScrollY, "roleListScroll")
        self.addWidgetInPool(roleListContentFrame, "roleListContent")

    def updateRoleList(self):
        """更新角色列表控件"""
        self.cleaerSkinContent()
        roleListCanvas = self.getWidgetFromPool("roleListCanvas")
        roleContentFrame = tk.Frame(roleListCanvas, background="white", borderwidth=4)
        roleListCanvas.create_window(0, 0, window=roleContentFrame, anchor=tk.NW)
        self.addWidgetInPool(roleContentFrame, "roleListContent")

        skinSourcePath = self.manager.getSkinPath()  # 皮肤库路径
        if skinSourcePath != None and os.path.exists(skinSourcePath):
            roleIndex = 0
            for roleDir in os.listdir(skinSourcePath):
                rolePath = os.path.join(skinSourcePath, roleDir)
                if os.path.isdir(rolePath) and RoleKey.existRole(roleDir):
                    imageIcon = self.getRoleImage(roleDir, rolePath)
                    rowIndex = (roleIndex // 10) + 1
                    columnIndex = (roleIndex % 10) + 1
                    imageFrame = tk.Frame(
                        roleContentFrame, borderwidth=13, background="white"
                    )  # 单个角色框架
                    imageFrame.grid(row=rowIndex, column=columnIndex)
                    imageBtn = tk.Button(
                        imageFrame, image=imageIcon, background="white"
                    )  # 角色图片按钮
                    imageBtn.pack(side=tk.TOP)
                    imageBtn.bind(
                        Event.MouseLefClick,
                        utils.eventAdaptor(self.clickSelectRole, key=roleDir),
                    )
                    imageLabel = tk.Label(
                        imageFrame,
                        text=RoleKey.getRoleText(roleDir),
                        font=FrameConfig.font,
                        background="white",
                    )  # 角色名
                    imageLabel.pack(side=tk.TOP)
                    self.addWidgetInPool(imageFrame, "singleRole")
                    self.addWidgetInPool(imageBtn, "singleRole")
                    self.addWidgetInPool(imageLabel, "singleRole")
                    roleIndex += 1

        roleListFrame = self.getWidgetFromPool("roleList")
        self.updateScrollFrame(roleListFrame, roleListCanvas, roleContentFrame)

    def displaySkinControl(self):
        """显示皮肤管理页面"""
        skinTitleFrame = self.getWidgetFromPool("skinTitle")
        roleListFrame = self.getWidgetFromPool("roleList")
        skinControlCanvas = self.getWidgetFromPool("skinControlCanvas")

        skinTitleFrame.pack_forget()
        roleListFrame.pack_forget()
        skinControlCanvas.forget()

        skinTitleFrame.pack(side=tk.TOP, fill=tk.X)
        skinControlCanvas.pack(side=tk.LEFT, fill=tk.Y)
        roleListFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def hideSkinControl(self):
        """隐藏皮肤管理页面"""
        controlCanvas = self.getWidgetFromPool("skinControlCanvas")
        controlCanvas.forget()

    def updateSkinListPage(self):
        """更新单个角色的皮肤列表"""
        self.cleaerSkinContent()  # 清空角色内容页
        self.skinThread = Thread(target=self.updateSkinListThread, daemon=True)
        self.skinThread.start()

    def updateSkinListThread(self):
        """线程更新单个角色的皮肤"""
        roleListCanvas = self.getWidgetFromPool("roleListCanvas")
        roleContentFrame = tk.Frame(roleListCanvas, background="white", borderwidth=5)
        roleListCanvas.create_window(0, 0, window=roleContentFrame, anchor=tk.NW)
        self.addWidgetInPool(roleContentFrame, "roleListContent")
        if self.selectRoleKey != None:
            skinPath = os.path.join(
                self.getSkinPathText(), self.selectRoleKey
            )  # 角色皮肤路径
            indexCount = 0
            for fileDir in os.listdir(skinPath):
                filePath = os.path.join(skinPath, fileDir)
                if not os.path.isdir(filePath):
                    continue
                images = self.getSkinImages(filePath)
                for image in images:
                    rowIndex = indexCount // 5
                    columnIndex = indexCount % 5
                    skinImageFrame = tk.Frame(roleContentFrame, background="white")
                    skinImageFrame.grid(row=rowIndex, column=columnIndex)
                    skinImageBtn = tk.Button(
                        skinImageFrame, image=image, background="white"
                    )
                    skinImageBtn.pack(side=tk.TOP)
                    skinImageLabel = tk.Label(
                        skinImageFrame,
                        text=fileDir,
                        font=FrameConfig.font,
                        background="white",
                    )
                    skinImageLabel.pack(side=tk.TOP, fill=tk.X)
                    skinImageBtn.bind(
                        Event.MouseLefClick,
                        utils.eventAdaptor(self.clickSelectSkin, dirName=fileDir),
                    )
                    skinImageBtn.bind(
                        Event.MouseWheel,
                        utils.eventAdaptor(
                            self.scrollVerticalCanvas, widget=roleListCanvas
                        ),
                    )
                    skinImageLabel.bind(
                        Event.MouseWheel,
                        utils.eventAdaptor(
                            self.scrollVerticalCanvas, widget=roleListCanvas
                        ),
                    )
                    self.addSkinImage(image)

                    self.addWidgetInPool(skinImageFrame, "skinList")
                    self.addWidgetInPool(skinImageFrame, "skinList")
                    self.addWidgetInPool(skinImageFrame, "skinList")

                    indexCount += 1

        roleListFrame = self.getWidgetFromPool("roleList")
        self.updateScrollFrame(roleListFrame, roleListCanvas, roleContentFrame)

    ####################getter&setter#####################

    def getMainFrame(self) -> tk.Tk:
        """主窗口"""
        return self.mainWindow

    def getSkinPathText(self) -> str:
        """获取皮肤路径"""
        path = self.manager.getSkinPath()
        return path if path != None else "请选择皮肤库路径"

    def getModPathText(self) -> str:
        """获取mods文件夹路径"""
        path = self.manager.getModsPath()
        return path if path != None else "请选择3Dmigoto Mods路径"

    def getRoleImage(self, key: str, path: str) -> tk.PhotoImage:
        """获取该文件夹下的第一张图片作为角色图片"""
        if key in self.roleImagePool:
            return self.roleImagePool[key]
        for fileName in os.listdir(path):
            filePath = os.path.join(path, fileName)
            if os.path.isfile(filePath) and utils.isPhoto(filePath):
                image = Image.open(filePath).resize(FrameConfig.roleIconSize)
                image = ImageTk.PhotoImage(image)
                self.addRoleImage(image, key)
                return image
        return self.getDefaultRoleImage()

    def getSkinImages(self, path: str) -> list[tk.PhotoImage]:
        """获取该文件夹下的所有皮肤图片"""
        images = []
        for filename in os.listdir(path):
            if utils.isPhoto(filename):
                filePath = os.path.join(path, filename)
                image = Image.open(filePath).resize(FrameConfig.roleSkinSize)
                images.append(ImageTk.PhotoImage(image))
        if len(images) <= 0:
            images.append(self.getDefaultSkinImage())
        return images

    def getDefaultSkinImage(self) -> tk.PhotoImage:
        """获取默认皮肤图片"""
        filePath = os.path.join(os.getcwd(), FrameConfig.defaultSkin)
        image = Image.open(filePath).resize(FrameConfig.roleSkinSize)
        return ImageTk.PhotoImage(image)

    def getModsUseSkinText(self, key: str) -> str:
        """获取当前角色正在使用的皮肤文本"""
        modPath = self.manager.getModsPath()
        if modPath != None and os.path.exists(modPath):
            rolePath = os.path.join(modPath, key)
            if os.path.exists(rolePath):
                for fileDir in os.listdir(rolePath):
                    skinPath = os.path.join(rolePath, fileDir)
                    if os.path.isdir(skinPath):
                        return fileDir
        return ""

    def getWidgetFromPool(self, key: str) -> tk.Widget:
        """默认返回key对应的第一个控件"""
        widgets = self.widgetPool[key]
        return widgets[0]

    def getDefaultRoleImage(self) -> tk.PhotoImage:
        """获取默认的角色图片"""
        if FrameConfig.defaultRoleKey not in self.roleImagePool:
            path = os.path.join(os.getcwd(), FrameConfig.defaultRole)
            image = Image.open(path).resize(FrameConfig.roleIconSize)
            image = ImageTk.PhotoImage(image)
            self.addRoleImage(image, FrameConfig.defaultRoleKey)
        return self.roleImagePool[FrameConfig.defaultRoleKey]

    # #####################Add&Modify&Delete##############

    def addWidgetInPool(self, widget: tk.Widget, key: str):
        """缓存控件"""
        if key not in self.widgetPool:
            self.widgetPool[key] = []
        self.widgetPool[key].append(widget)

    def addRoleImage(self, image: tk.PhotoImage, key: str):
        """缓存角色图片"""
        self.roleImagePool[key] = image

    def addSkinImage(self, image: tk.PhotoImage):
        """缓存皮肤图片"""
        self.skinImagePool.append(image)

    def clearWidgetByList(self, keys: list[str]):
        """通过Key列表清空控件池"""
        for key in keys:
            self.clearWidgetByKey(key)

    def clearWidgetByKey(self, key: str):
        """通过Key清空控件池"""
        if key in self.widgetPool:
            for widget in self.widgetPool[key]:
                if utils.isWidget(widget, tk.Widget):
                    widget.destroy()

    def cleaerSkinContent(self):
        """清空roleList,skinList页面内的控件"""
        self.clearWidgetByKey("singleRole")
        self.clearWidgetByKey("roleListContent")
        self.skinImagePool = []

    ####################event###########################

    def close(self, event):
        """关闭事件"""
        self.getMainFrame().destroy()
        sys.exit()

    def scrollHoriCanvas(self, event, widget: tk.Canvas):
        """画布左右滚动事件"""
        widget.xview_scroll(-1 * (event.delta // 5), tk.UNITS)

    def scrollVerticalCanvas(self, event, widget: tk.Canvas):
        """画布上下滚动事件"""
        widget.yview_scroll(-1 * (event.delta // 5), tk.UNITS)

    def switchSideBar(self, event):
        """展开、关闭侧边栏"""
        sideBarCanvas = self.getWidgetFromPool("sideBarCanvas")
        if sideBarCanvas != None:
            if self.sideBarSwitch:
                sideBarCanvas.pack_forget()
            else:
                sideBarFrame = self.getWidgetFromPool("sideBar")
                sideBarContentFrame = self.getWidgetFromPool("sideBarFrame")
                sideBarCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
                self.updateScrollFrame(sideBarFrame, sideBarCanvas, sideBarContentFrame)
            self.sideBarSwitch = not self.sideBarSwitch

    def selectSkinSource(self, event):
        """选择皮肤库路径"""
        filePath = askdirectory()
        skinSouce = self.getWidgetFromPool("skinSource")
        if not utils.isEmpty(filePath) and utils.isWidget(skinSouce, tk.Label):
            skinSouce.config(text=filePath)
            self.manager.setSkinPath(filePath)
            self.updateRoleList()

    def selectModSource(self, event):
        """选择Mods路径"""
        filePath = askdirectory()
        modSource = self.getWidgetFromPool("modSource")
        if not utils.isEmpty(filePath) and utils.isWidget(modSource, tk.Label):
            modSource.config(text=filePath)
            self.manager.setModsPath(filePath)

    def clickSelectRole(self, event, key: str):
        """点击某一角色图标"""
        self.selectRoleKey = key
        self.page = "skinListPage"
        displayRoleLabel = self.getWidgetFromPool("skinDisplay")  # 更新所选角色
        if utils.isWidget(displayRoleLabel, tk.Label):
            path = os.path.join(self.manager.getSkinPath(), key)
            image = self.getRoleImage(key, path)
            displayRoleLabel.config(image=image)
        displayRoleText = self.getWidgetFromPool("skinDisplayText")  # 更新所选角色信息
        if utils.isWidget(displayRoleText, tk.Label):
            displayRoleText.config(text=RoleKey.getRoleText(self.selectRoleKey))
        skinSelectText = self.getWidgetFromPool("skinSelectText")  # 清空原选择的信息
        if utils.isWidget(skinSelectText, tk.Label):
            skinSelectText.config(text="")
        modUseRoleText = self.getWidgetFromPool("modsUseText")  # mods正在使用角色
        if utils.isWidget(modUseRoleText, tk.Label):
            modUseRoleText.config(text=self.getModsUseSkinText(self.selectRoleKey))
        self.displaySkinControl()
        self.updateSkinListPage()

    def clickSelectSkin(self, event, dirName: str):
        """点击选择皮肤"""
        skinSelectLabel = self.getWidgetFromPool("skinSelectText")
        if utils.isWidget(skinSelectLabel, tk.Label):
            skinSelectLabel.config(text=dirName)

    def clickUpdateFile(self, event, btn: tk.Button):
        """点击更新到文件"""
        btn.config(text="更新中...")
        self.manager.writeToFile()
        btn.config(text="更新成功", fg=FrameConfig.colorSuccess)
        Thread(target=self.replaceText, args=(btn, "更新"), daemon=False).start()

    def backPage(self, event):
        """返回上一页"""
        if not utils.isEmpty(self.selectRoleKey) and not self.skinThreadStopSymbol:
            self.stopThread()  # 终止线程

            self.selectRoleKey = ""
            self.page = "roleListPage"
            skinSelectText = self.getWidgetFromPool("skinSelectText")  # 清空原选择的信息
            if utils.isWidget(skinSelectText, tk.Label):
                skinSelectText.config(text="")
            modUseRoleText = self.getWidgetFromPool("modsUseText")  # mods正在使用角色
            if utils.isWidget(modUseRoleText, tk.Label):
                modUseRoleText.config(text="")
            self.cleaerSkinContent()
            self.hideSkinControl()
            self.updateRoleList()

    def clickReplaceSkin(self, event):
        """点击替换皮肤"""
        replaceBtn = self.getWidgetFromPool("skinDisplayReplace")
        replaceText = self.getWidgetFromPool("skinSelectText")
        if not utils.isWidget(replaceBtn, tk.Button) or not utils.isWidget(
            replaceText, tk.Label
        ):
            return
        if replaceBtn != None and replaceBtn["text"] == "替换":
            pathName = replaceText["text"]
            if utils.isEmpty(pathName):
                replaceBtn.config(text="替换(未选择皮肤)", fg=FrameConfig.colorFail)
                Thread(
                    target=self.replaceText, args=(replaceBtn, "替换"), daemon=True
                ).start()
                return
            modsPath = self.manager.getModsPath()
            if utils.isEmpty(modsPath) or modsPath == "请选择3dmigoto Mods文件夹":
                replaceBtn.config(text="替换(未选择Mods文件夹)", fg=FrameConfig.colorFail)
                Thread(
                    target=self.replaceText, args=(replaceBtn, "替换"), daemon=True
                ).start()
                return
            if not os.path.exists(modsPath):
                replaceBtn.config(text="替换(Mods文件夹不存在)", fg=FrameConfig.colorFail)
                Thread(
                    target=self.replaceText, args=(replaceBtn, "替换"), daemon=True
                ).start()
                return
            replaceBtn.config(text="替换中......")
            Thread(
                target=self.replaceSkin, args=(modsPath, pathName), daemon=False
            ).start()

    def replaceSkin(self, modsPath: str, pathName: str) -> bool:
        """替换皮肤"""
        modRolePath = os.path.join(modsPath, self.selectRoleKey)  # mods角色路径
        if os.path.exists(modRolePath):
            shutil.rmtree(modRolePath)  # 清空当前角色正当使用的mod
        modFileDir = os.path.join(modRolePath, pathName)  # 创建目标文件夹
        rolePath = os.path.join(self.manager.getSkinPath(), self.selectRoleKey)
        skinPath = os.path.join(rolePath, pathName)
        replaceBtn = self.getWidgetFromPool("skinDisplayReplace")
        if utils.isWidget(replaceBtn, tk.Button) and os.path.exists(skinPath):
            shutil.copytree(skinPath, modFileDir)
            replaceBtn.config(text="替换成功！！", fg=FrameConfig.colorSuccess)
            Thread(
                target=self.replaceText, args=(replaceBtn, "替换"), daemon=True
            ).start()
            modUseRoleText = self.getWidgetFromPool("modsUseText")  # mods正在使用角色
            if utils.isWidget(modUseRoleText, tk.Label):
                modUseRoleText.config(text=self.getModsUseSkinText(self.selectRoleKey))
        else:
            replaceBtn.config(text="替换失败(未知原因)", fg=FrameConfig.colorFail)
            Thread(
                target=self.replaceText, args=(replaceBtn, "替换"), daemon=True
            ).start()

    def replaceText(self, btn: tk.Button, text: str):
        """替换按钮文本"""
        sleep(2)
        btn.config(text=text, fg=FrameConfig.colorDefault)

    def clickDeleteModSkin(self, event):
        """点击删除mods路径对应角色的皮肤文件"""
        deleteBtn = self.getWidgetFromPool("skinDisplayDelete")
        if utils.isWidget(deleteBtn, tk.Button) and deleteBtn["text"] == "删除":
            useModsLabel = self.getWidgetFromPool("modsUseText")
            if utils.isWidget(useModsLabel, tk.Label):
                modPath = self.manager.getModsPath()
                if utils.isEmpty(modPath):
                    deleteBtn.config(text="未选择Mods路径", fg=FrameConfig.colorFail)
                    Thread(
                        target=self.replaceText, args=(deleteBtn, "删除"), daemon=True
                    ).start()
                    return
                elif not os.path.exists(modPath):
                    deleteBtn.config(text="Mods路径不存在", fg=FrameConfig.colorFail)
                    Thread(
                        target=self.replaceText, args=(deleteBtn, "删除"), daemon=True
                    ).start()
                    return
                dirName = useModsLabel["text"]
                rolePath = os.path.join(modPath, self.selectRoleKey)
                skinPath = os.path.join(rolePath, dirName)
                if (
                    utils.isEmpty(self.selectRoleKey)
                    or not os.path.exists(rolePath)
                    or utils.isEmpty(dirName)
                    or not os.path.exists(skinPath)
                ):
                    deleteBtn.config(text="未有使用皮肤", fg=FrameConfig.colorFail)
                    Thread(
                        target=self.replaceText, args=(deleteBtn, "删除"), daemon=True
                    ).start()
                    return
                Thread(
                    target=self.deleteModSkin,
                    args=(deleteBtn, skinPath, useModsLabel),
                    daemon=False,
                ).start()

    def deleteModSkin(self, deleteBtn: tk.Button, skinPath: str, useLabel: tk.Label):
        """删除正在使用的皮肤"""
        deleteBtn.config(text="删除中...", fg=FrameConfig.colorDefault)
        shutil.rmtree(skinPath)
        useLabel.config(text="")
        deleteBtn.config(text="删除成功", fg=FrameConfig.colorSuccess)
        Thread(target=self.replaceText, args=(deleteBtn, "删除"), daemon=True).start()

    def stopThread(self):
        """停止当前运行的线程"""
        utils.stopThread(self.skinThread)

    def clickCreateSkinImage(self, event):
        """点击制作预览皮肤"""
        selectLabel = self.getWidgetFromPool("skinSelectText")
        createReviewBtn = self.getWidgetFromPool("catchScreen")
        if utils.isWidget(selectLabel, tk.Label) and utils.isWidget(
            createReviewBtn, tk.Button
        ):
            if createReviewBtn["text"] != "截图制作预览":
                return
            createReviewBtn.config(text="处理中", fg=FrameConfig.colorDefault)
            selectSkinName = selectLabel["text"]  # 选择皮肤名称
            skinSourcePath = self.manager.getSkinPath()  # 皮肤源路径
            if not utils.isPathExist(skinSourcePath):
                createReviewBtn.config(text="皮肤路径不存在", fg=FrameConfig.colorFail)
                Thread(
                    target=self.replaceText,
                    args=(createReviewBtn, "截图制作预览"),
                    daemon=False,
                ).start()
                return
            rolePath = os.path.join(skinSourcePath, self.selectRoleKey)
            skinPath = os.path.join(rolePath, selectSkinName)
            if not utils.isPathExist(skinPath):
                createReviewBtn.config(text="皮肤路径不存在", fg=FrameConfig.colorFail)
                Thread(
                    target=self.replaceText,
                    args=(createReviewBtn, "截图制作预览"),
                    daemon=False,
                ).start()
                return
            createReviewBtn.config(text="截图中", fg=FrameConfig.colorDefault)
            tempPath = os.path.join(os.getcwd, FrameConfig.tempDir)
            utils.createDir(tempPath)  # 临时图片存储位置

            fileName = "%d.png" % datetime.datetime.now().timestamp()
            tempFilePath = os.path.join(tempPath, fileName)
            generater = mss.mss().save(mon=2, output=tempFilePath)  # 截图
            next(generater)
            createReviewBtn.config(text="制作预览中", fg=FrameConfig.colorDefault)

            filePath = os.path.join(skinPath, fileName)
            image = Image.open(tempFilePath)
            regionStage = utils.getCropStage(image.width, image.height)
            if regionStage != None:
                regoinImage = image.crop(regionStage)
                regoinImage.save(filePath)
            shutil.rmtree(tempPath)
            createReviewBtn.config(text="操作成功", fg=FrameConfig.colorSuccess)
            Thread(
                target=self.replaceText, args=(createReviewBtn, "截图制作预览"), daemon=False
            ).start()
            self.stopThread()
            self.updateSkinListPage()


if __name__ == "__main__":
    MainFrame()
