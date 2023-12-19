import os
import sys
import utils
import shutil
import tkinter as tk
from tkinter.filedialog import askdirectory
from manager import Manager
from PIL import Image, ImageTk
from tkinter import ttk
from threading import Thread
from time import sleep
from data2 import RoleKey, FrameConfig, FrameKey, Event


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
        self.mainWindow.attributes("-fullscreen", True)  # 全屏
        self.mainWindow.bind(Event.F4, self.close)  # F4退出程序
        self.mainWindow.bind(Event.Escape, self.close)
        self.mainWindow.bind(Event.Tab, self.switchSideBar)  # 切换侧边栏

    def initFrameData(self):
        """初始化框架相关数据"""
        self.sideBarSwitch = True  # 默认展开侧边栏
        self.roleImagePool = {}  # 角色图片池
        self.selectRoleKey = None  # 当前选择的角色
        self.skinImagePool = []  # 角色皮肤图片池

    def initWidgetPool(self):
        """初始化控件池"""
        self.widgetPool = {}

    def initMainFrame(self):
        """初始化第一层控件"""
        sideBarFrame = tk.Frame(self.getMainFrame(), background="yellow")  # 侧边栏
        sideBarFrame.pack(side=tk.LEFT, fill=tk.Y, ipady=3)

        contentFrame = tk.Frame(self.getMainFrame(), background="green")  # 内容页
        contentFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.addWidgetInPool(sideBarFrame, "sideBar")  # 缓存
        self.addWidgetInPool(contentFrame, "content")

    def initSideBar(self):
        """初始化侧边栏"""
        sideBarFrame = self.getWidgetFromPool("sideBar")  # 侧边栏框架

        sideBarCanvas = tk.Canvas(sideBarFrame, background="blue")  # 侧边栏画布
        sideBarScroll = tk.Scrollbar(
            sideBarFrame, orient=tk.VERTICAL, width=2, background="pink"
        )  # 侧边栏竖向滚动条
        sideBarCanvas.config(
            yscrollcommand=sideBarScroll.set, yscrollincrement=1
        )  # 侧边栏画布关联竖直滚动条
        sideBarScroll.config(command=sideBarCanvas.yview)  # 滚动条关联画布y轴
        sideBarCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        sideBarScroll.pack(side=tk.RIGHT, fill=tk.Y)

        sideBarScrollFrame = tk.Frame(sideBarCanvas, background="pink", borderwidth=5)
        sideBarCanvas.create_window(0, 0, window=sideBarScrollFrame, anchor=tk.NW)
        sideBarScrollFrame.bind(
            "<MouseWheel>",
            utils.eventAdaptor(self.scrollVerticalCanvas, widget=sideBarCanvas),
        )  # 绑定画布的滚动事件

        skinManagerBtn = tk.Button(
            sideBarScrollFrame, text="皮肤管理", font=FrameConfig.font, width=15
        )
        skinManagerBtn.pack(side=tk.TOP, fill=tk.X)

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

        skinTitleFrame = tk.Frame(contentFrame)  # 显示皮肤标题一栏
        skinTitleFrame.pack(side=tk.TOP, fill=tk.X)
        skinSourceFrame = tk.Frame(skinTitleFrame)  # 皮肤标题第一行
        skinSourceFrame.pack(side=tk.TOP, fill=tk.X)
        skinSourceLabel = tk.Label(skinSourceFrame, text="皮肤库", font=FrameConfig.font)
        skinSourceLabel.pack(side=tk.LEFT)
        skinSourceSetBtn = tk.Button(skinSourceFrame, text="更新", font=FrameConfig.font)
        skinSourceSetBtn.pack(side=tk.RIGHT)
        skinSource = tk.Label(
            skinSourceFrame, text=self.getSkinPathText(), font=FrameConfig.font
        )
        skinSource.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        skinSource.bind(Event.MouseLefClick, self.selectSkinSource)  # 选择皮肤路径事件

        self.addWidgetInPool(skinTitleFrame, "skinTitle")
        self.addWidgetInPool(skinSourceFrame, "skinTitleFrame")
        self.addWidgetInPool(skinSourceLabel, "skinTitleLabel")
        self.addWidgetInPool(skinSourceSetBtn, "skinSourceBtn")
        self.addWidgetInPool(skinSource, "skinSource")

        modSourceFrame = tk.Frame(skinTitleFrame)  # 皮肤标题第二行
        modSourceFrame.pack(side=tk.TOP, fill=tk.X)
        modSourceLabel = tk.Label(modSourceFrame, text="Mods", font=FrameConfig.font)
        modSourceLabel.pack(side=tk.LEFT)
        modSourceBtn = tk.Button(modSourceFrame, text="更新", font=FrameConfig.font)
        modSourceBtn.pack(side=tk.RIGHT)
        modSource = tk.Label(
            modSourceFrame, text=self.getModPathText(), font=FrameConfig.font
        )  # 3dmigoto目标路径
        modSource.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.addWidgetInPool(modSourceFrame, "skinTitleFrame")
        self.addWidgetInPool(modSourceLabel, "skinTitleLabel")
        self.addWidgetInPool(modSourceBtn, "modSourceBtn")
        self.addWidgetInPool(modSource, "modSource")

        skinControlFrame = tk.Frame(contentFrame, background="yellow")  # 显示皮肤操作一栏
        skinControlFrame.pack(side=tk.LEFT, fill=tk.Y)
        roleSelectDisplay = tk.Label(
            skinControlFrame,
            image=self.getDefaultRoleImage(),
            background="blue",
            width=FrameConfig.skinControlWidth,
        )  # 显示当前选择的角色图标
        roleSelectDisplay.pack(side=tk.TOP, fill=tk.X)
        roleSelectText = tk.Label(
            skinControlFrame,
            text=RoleKey.getRoleText(FrameConfig.defaultRoleKey),
            background="pink",
            font=FrameConfig.font,
        )  # 显示当前选择的角色文本
        roleSelectText.pack(side=tk.TOP, fill=tk.X)
        skinSelectFrame = tk.Frame(skinControlFrame)  # 已选皮肤一栏
        skinSelectFrame.pack(side=tk.TOP, fill=tk.X)
        skinSelectLabel = tk.Label(
            skinSelectFrame, text="当前选择：", anchor=tk.NW, font=FrameConfig.font
        )  # 已选皮肤标签
        skinSelectLabel.pack(side=tk.TOP, fill=tk.X)
        skinSelectText = tk.Label(
            skinSelectFrame, text="", font=FrameConfig.font
        )  # 已选皮肤文件名
        skinSelectText.pack(side=tk.TOP, fill=tk.X)
        skinReplaceBtn = tk.Button(
            skinControlFrame, text="替换", font=FrameConfig.font
        )  # 替换皮肤
        skinReplaceBtn.pack(side=tk.TOP, fill=tk.X)
        skinBeSetFrame = tk.Frame(skinControlFrame)  # 当前使用的皮肤
        skinBeSetFrame.pack(side=tk.TOP, fill=tk.X)
        skinBeSetLabel = tk.Label(
            skinBeSetFrame, text="当前使用：", anchor=tk.NW, font=FrameConfig.font
        )  # 已使用皮肤标签
        skinBeSetLabel.pack(side=tk.TOP, fill=tk.X)
        skinBeSetText = tk.Label(
            skinBeSetFrame,
            text=self.getModsUseSkinText(FrameConfig.defaultRoleKey),
            font=FrameConfig.font,
        )  # 已使用皮肤文件名
        skinBeSetText.pack(side=tk.TOP, fill=tk.X)
        skinUseDeleteBtn = tk.Button(
            skinControlFrame, text="删除", font=FrameConfig.font
        )  # 删除正在使用的皮肤
        skinUseDeleteBtn.pack(side=tk.TOP, fill=tk.X)

        self.addWidgetInPool(skinControlFrame, "skinControl")
        self.addWidgetInPool(roleSelectDisplay, "skinDisplay")
        self.addWidgetInPool(roleSelectText, "skinDisplayText")
        self.addWidgetInPool(skinSelectFrame,"skinDisplayFrame")
        self.addWidgetInPool(skinSelectLabel,"skinSelectLabel")
        self.addWidgetInPool(skinSelectText,"skinSelectText")
        self.addWidgetInPool(skinReplaceBtn,"skinDisplayBtn")
        self.addWidgetInPool(skinBeSetFrame,"skinDisplayFrame")
        self.addWidgetInPool(skinBeSetLabel,"skinSelectLabel")
        self.addWidgetInPool(skinBeSetText,"modsUseText")
        self.addWidgetInPool(skinUseDeleteBtn,"skinDisplayBtn")

        # skinControlFrame.pack_forget()

        roleListFrame = tk.Frame(contentFrame, background="brown")  # 显示皮肤内容一栏
        roleListFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.addWidgetInPool(roleListFrame,"roleList")

    def initRoleListPage(self):
        """初始化角色列表页面"""
        roleListFrame = self.getWidgetFromPool("roleList")

        roleListCanvas = tk.Canvas(roleListFrame, background="pink")  # 角色选择页面画布
        roleListScrollX = tk.Scrollbar(
            roleListFrame, orient=tk.HORIZONTAL, width=2, background="green"
        )  # 横向滚动条
        roleListScrollY = tk.Scrollbar(
            roleListFrame, orient=tk.VERTICAL, width=2, background="blue"
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

        roleListContentFrame = tk.Frame(roleListCanvas, background="white", borderwidth=5)
        roleListCanvas.create_window(0, 0, window=roleListContentFrame, anchor=tk.NW)

        self.updateScrollFrame(roleListFrame,roleListCanvas,roleListContentFrame)

        self.addWidgetInPool(roleListCanvas,"roleListCanvas")
        self.addWidgetInPool(roleListScrollX,"roleListScroll")
        self.addWidgetInPool(roleListScrollY,"roleListScroll")
        self.addWidgetInPool(roleListContentFrame,"roleListContent")

    def updateRoleList(self):
        """更新角色列表控件"""
        self.clearWidgetByKey("singleRole")
        self.clearWidgetByKey("roleListContent")
        roleListCanvas = self.getWidgetFromPool("roleListCanvas")
        roleContentFrame = tk.Frame(roleListCanvas, background="white", borderwidth=5)
        roleListCanvas.create_window(0, 0, window=roleContentFrame, anchor=tk.NW)
        self.addWidgetInPool(roleContentFrame,"roleListContent")

        skinSourcePath = self.manager.getSkinPath()  # 皮肤库路径
        if skinSourcePath != None and os.path.exists(skinSourcePath):
            roleIndex = 0
            for roleDir in os.listdir(skinSourcePath):
                rolePath = os.path.join(skinSourcePath, roleDir)
                if os.path.isdir(rolePath) and RoleKey.existRole(roleDir):
                    imageIcon = self.getRoleImage(roleDir, rolePath)
                    rowIndex = (roleIndex // 10) + 1
                    columnIndex = (roleIndex % 10) + 1
                    imageFrame = tk.Frame(roleContentFrame)  # 单个角色框架
                    imageFrame.grid(row=rowIndex, column=columnIndex)
                    imageBtn = tk.Button(imageFrame, image=imageIcon)  # 角色图片按钮
                    imageBtn.pack(side=tk.TOP)
                    imageBtn.bind(
                        Event.MouseLefClick,
                        utils.eventAdaptor(self.clickSelectRole, key=roleDir),
                    )
                    imageLabel = tk.Label(
                        imageFrame,
                        text=RoleKey.getRoleText(roleDir),
                        font=FrameConfig.font,
                    )  # 角色名
                    imageLabel.pack(side=tk.TOP)
                    self.addWidgetInPool(imageFrame,"singleRole")
                    self.addWidgetInPool(imageBtn,"singleRole")
                    self.addWidgetInPool(imageLabel,"singleRole")
                    roleIndex += 1

        roleListFrame = self.getWidgetFromPool("roleList")
        self.updateScrollFrame(roleListFrame,roleListCanvas,roleContentFrame)

    # def updateSkinListPage(self):
    #     """更新单个角色的皮肤列表"""
    #     self.clearWidgetPool(FrameKey.SkinContentFrame)  # 清空角色内容页
    #     # skinListFrame = self.getBaseFrame(FrameKey.SkinContentFrame)
    #     # if self.selectRoleKey != None:
    #     #     skinPath = os.path.join(
    #     #         self.getSkinPathText(), self.selectRoleKey
    #     #     )  # 角色皮肤路径
    #     #     for fileDir in os.listdir(skinPath):
    #     #         filePath = os.path.join(skinPath, fileDir)
    #     #         if os.path.isdir(filePath):
    #     #             images = self.getSkinImages(filePath)
    #     #             for image in images:
    #     #                 pass
    #     self.updateScrollFrame(FrameKey.SkinContent, FrameKey.SkinContentFrame)

    ####################getter&setter#####################

    def getMainFrame(self) -> tk.Tk:
        """主窗口"""
        return self.mainWindow

    def addWidgetInPool(self, widget: tk.Widget, key: str):
        """缓存控件"""
        if key not in self.widgetPool:
            self.widgetPool[key] = []
        self.widgetPool[key].append(widget)

    # def getScrollCanvas(self, key: str) -> dict | None:
    #     """获取对应的滚动画布"""
    #     if key in self.scrollCanvasPool:
    #         return self.scrollCanvasPool[key]
    #     return None

    # def getBaseFrame(self, key: str) -> tk.Frame | None:
    #     """获取动态变化主组件"""
    #     if key in self.baseFramePool:
    #         return self.baseFramePool[key]
    #     return None

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
        for fileName in os.listdir(path):
            filePath = os.path.join(path, fileName)
            if os.path.isfile(filePath) and utils.isPhoto(filePath):
                image = Image.open(filePath).resize(FrameConfig.roleIconSize)
                image = ImageTk.PhotoImage(image)
                self.addRoleImage(image, key)
                return image
        return self.getDefaultRoleImage()

    # def getSkinImages(self, path: str) -> list[tk.PhotoImage]:
    #     """获取该文件夹下的所有皮肤图片"""
    #     images = []
    #     for filename in os.listdir(path):
    #         if utils.isPhoto(filename):
    #             filePath = path + "/" + filename
    #             image = Image.open(filePath).resize(FrameConfig.roleSkinSize)
    #             images.append(ImageTk.PhotoImage(image))
    #     return images

    # def getReferWidget(self, key: str) -> tk.Widget | None:
    #     """获取动态控件"""
    #     if key in self.referPool:
    #         return self.referPool[key]
    #     return None

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

    # #####################Add&Modify&Delete##############

    def getDefaultRoleImage(self) -> tk.PhotoImage:
        """获取默认的角色图片"""
        if FrameConfig.defaultRoleKey not in self.roleImagePool:
            path = os.path.join(sys.path[0], FrameConfig.defaultRole)
            image = Image.open(path).resize(FrameConfig.roleIconSize)
            image = ImageTk.PhotoImage(image)
            self.addRoleImage(image, FrameConfig.defaultRoleKey)
        return self.roleImagePool[FrameConfig.defaultRoleKey]

    def addRoleImage(self, image: tk.PhotoImage, key: str):
        """缓存角色图片"""
        self.roleImagePool[key] = image

    # def addBaseWidget(self, widget: tk.Widget):
    #     """缓存基础控件"""
    #     self.baseWidgetPool.append(widget)

    # def addScrollCanvas(self, widget: tk.Canvas, key: str, scroll: str):
    #     """缓存可滚动的画布"""
    #     self.scrollCanvasPool[key] = {
    #         FrameKey.InfoCanvas: widget,
    #         FrameKey.InfoScroll: scroll,
    #     }

    # def addBaseFrame(self, widget: tk.Frame, key: str):
    #     """缓存动态变化的主组件"""
    #     self.baseFramePool[key] = widget

    # def addNoReferWidget(self, widget: tk.Widget, key: str):
    #     """缓存不会被引用的控件"""
    #     if key not in self.noReferPool:
    #         self.noReferPool[key] = []
    #     self.noReferPool[key].append(widget)
    #     if key in self.scrollCanvasPool:
    #         self.bindScrollEvent(widget, key)  # 绑定控件事件

    # def addReferWidget(self, widget: tk.Widget, key: str):
    #     """缓存被引用的控件"""
    #     self.referPool[key] = widget

    def clearWidgetByList(self, keys: list[str]):
        """通过Key列表清空控件池"""
        for key in keys:
            self.clearWidgetByKey(key)

    def clearWidgetByKey(self,key:str):
        """通过Key清空控件池"""
        if key in self.widgetPool:
                for widget in self.widgetPool[key]:
                    if isinstance(widget, tk.Widget):
                        widget.destroy()

    # ####################Function#########################
    # def bindScrollEvent(self, widget: tk.Widget, key: str):
    #     """为控件绑定画布滚动事件"""
    #     canvasInfo = self.getScrollCanvas(key)
    #     if canvasInfo != None:
    #         scrollType = canvasInfo[FrameKey.InfoScroll]
    #         canvas = canvasInfo[FrameKey.InfoCanvas]
    #         if canvas != None and isinstance(canvas, tk.Canvas):
    #             if scrollType == tk.X:
    #                 widget.bind(
    #                     Event.MouseWheel,
    #                     utils.eventAdaptor(self.scrollHoriCanvas, widget=canvas),
    #                 )
    #             elif scrollType == tk.Y:
    #                 widget.bind(
    #                     Event.MouseWheel,
    #                     utils.eventAdaptor(self.scrollVerticalCanvas, widget=canvas),
    #                 )
    #             elif scrollType == tk.BOTH:
    #                 widget.bind(
    #                     Event.MouseWheel,
    #                     utils.eventAdaptor(self.scrollHoriCanvas, widget=canvas),
    #                 )
    #                 widget.bind(
    #                     Event.MouseWheel,
    #                     utils.eventAdaptor(self.scrollVerticalCanvas, widget=canvas),
    #                 )

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
        # canvasInfo = self.getScrollCanvas(FrameKey.SideBar)
        # if canvasInfo != None:
        #     canvas = canvasInfo[FrameKey.InfoCanvas]
        #     if canvas != None and isinstance(canvas, tk.Canvas):
        #         if self.sideBarSwitch:
        #             canvas.pack_forget()
        #         else:
        #             canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        #             self.updateScrollFrame(FrameKey.SideBarParent, FrameKey.SideBar)
        #         self.sideBarSwitch = not self.sideBarSwitch

    def selectSkinSource(self, event):
        """选择皮肤库路径"""
        filePath = askdirectory()
        skinSouce = self.getWidgetFromPool("skinSource")
        if (
            not utils.isEmpty(filePath)
            and skinSouce != None
            and isinstance(skinSouce, tk.Label)
        ):
            skinSouce.config(text=filePath)
            self.manager.setSkinPath(filePath)
            self.updateRoleList()

    def clickSelectRole(self, event, key: str):
        """点击某一角色图标"""
        self.selectRoleKey = key
        # displayRoleLabel = self.getReferWidget(FrameKey.RoleDisplay)  # 更新所选角色
        # if displayRoleLabel != None and isinstance(displayRoleLabel, tk.Label):
        #     path = os.path.join(self.manager.getSkinPath(), key)
        #     print(path)
        #     image = self.getRoleImage(key, path)
        #     displayRoleLabel.config(image=image)
        # skinCanvas = self.getScrollCanvas(FrameKey.SkinContentFrame)
        # if skinCanvas != None and isinstance(skinCanvas, tk.Canvas):
        #     skinCanvas.pack_forget()

        # skinControlFrame = self.getBaseFrame(FrameKey.SkinControl)  # 显示控制角色页面
        # if skinControlFrame != None and isinstance(skinControlFrame, tk.Frame):
        #     print("test")
        #     skinControlFrame.pack(side=tk.LEFT, fill=tk.Y)
        #     skinControlFrame.update()
        # if skinCanvas != None and isinstance(skinCanvas, tk.Canvas):
        #     skinCanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        # self.updateSkinListPage()

    # ####################debugger########################

    # def testVerticalScrollBar(
    #     self, widget: tk.Widget, amount: int, width: int, height: int
    # ):
    #     """测试竖直方式的滚动条"""
    #     for i in range(amount):
    #         button = tk.Button(
    #             widget, background="gray", text=str(i), width=width, height=height
    #         )
    #         button.pack(side=tk.TOP, fill=tk.X, expand=1)

    # def testHoriScrollBar(
    #     self, widget: tk.Widget, amount: int, width: int, height: int
    # ):
    #     """测试竖直方式的滚动条"""
    #     for i in range(amount):
    #         button = tk.Button(
    #             widget, background="gray", text=str(i), width=width, height=height
    #         )
    #         button.pack(side=tk.LEFT, fill=tk.Y, expand=1)

    # def addTestWidget(self, widget: tk.Widget):
    #     """添加测试控件"""
    #     self.testWidgetPool.append(widget)

    # def testEvent(self, event, widget: tk.Canvas):
    #     """测试事件"""
    #     widget.yview_scroll(10, tk.UNITS)


if __name__ == "__main__":
    MainFrame()
