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
        self.initSideBar()  # 初始化侧边栏
        self.initSideBarContent()  # 初始化侧边栏内容
        self.initPage()  # 初始化页面
        self.initSkinManagerPage()  # 初始化皮肤管理页面
        self.initRoleListPage()  # 初始化角色选择列表页面
        self.updateRoleList()  # 更新角色列表页面
        self.mainWindow.mainloop()  # 显示窗口

    ####################init&update############################
    #Init表示只会执行一次
    #Update表示会清空相关页面内容并重新渲染

    def initWindow(self):
        """初始化窗口"""
        self.mainWindow.title(FrameConfig.frameTitle)
        self.mainWindow.attributes("-fullscreen", True)  # 全屏
        self.mainWindow.bind(Event.F4, self.close)  # F4退出程序
        self.mainWindow.bind(Event.Escape, self.close)
        self.mainWindow.bind(Event.Tab, self.switchSideBar)  # 切换侧边栏
        self.baseFont = FrameConfig.font  # 设置字体

    def initFrameData(self):
        """初始化框架相关数据"""
        self.sideBarSwitch = True  # 默认展开侧边栏
        self.roleImagePool = {}  # 角色图片池

    def initWidgetPool(self):
        """初始化控件池"""
        self.baseWidgetPool = []  # 基础控件缓存(不会变化，不会被引用)
        self.baseFramePool = {}  # 框架主组件缓存(会变化，且被引用)

        self.scrollCanvasPool = {}  # 可滚动画布缓存，用于绑定画布的滚动事件(被引用)
        self.noReferPool = {}  # 动态缓存控件（会被清空，不会被引用）
        self.referPool = {}  # 动态缓存控件（会被清空，会被引用）

        self.testWidgetPool = []  # 测试用缓存

    def initSideBar(self):
        """初始化侧边栏"""
        sideBarFrame = tk.Frame(self.getMainFrame(), background="yellow")  # 侧边栏基础框
        sideBarFrame.pack(side=tk.LEFT, fill=tk.Y, ipady=3)

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

        self.addBaseWidget(sideBarScroll)
        self.addScrollCanvas(sideBarCanvas, FrameKey.SideBar, tk.Y)  # 缓存滚动画布
        self.addBaseFrame(sideBarScrollFrame, FrameKey.SideBar)  # 缓存动态主组件
        self.addBaseFrame(sideBarFrame, FrameKey.SideBarParent)

    def initSideBarContent(self):
        """初始化侧边栏动态控件"""
        mainFrame = self.getBaseFrame(FrameKey.SideBar)
        skinManagerBtn = tk.Button(mainFrame, text="皮肤管理", font=self.baseFont, width=15)
        skinManagerBtn.pack(side=tk.BOTTOM, fill=tk.X)
        self.addNoReferWidget(skinManagerBtn, FrameKey.SideBar)
        self.updateScrollFrame(FrameKey.SideBarParent, FrameKey.SideBar)

    def updateScrollFrame(self, parentKey: str, framekey: str):
        """更新侧边栏,内容框架与其父组件的画布应所属同一FrameKey"""
        self.getBaseFrame(parentKey).update()
        canvasInfo = self.getScrollCanvas(framekey)
        frame = self.getBaseFrame(framekey)
        if canvasInfo != None and frame != None:
            canvas = canvasInfo[FrameKey.InfoCanvas]
            if canvas != None and isinstance(canvas, tk.Canvas):
                canvas.config(
                    scrollregion=frame.bbox(tk.ALL),
                    width=frame.winfo_width(),
                    height=frame.winfo_height(),
                )  # 设定画布可滚区域及自适应内容

    def initPage(self):
        """初始化内容页面"""
        pageFrame = tk.Frame(self.getMainFrame(), background="green")  # 页面栏基础框
        pageFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.addBaseFrame(pageFrame, FrameKey.Page)

    def initSkinManagerPage(self):
        """初始化皮肤管理页面"""
        pageFrame = self.getBaseFrame(FrameKey.Page)
        skinTitleFrame = tk.Frame(pageFrame)  # 显示皮肤标题一栏
        skinTitleFrame.pack(side=tk.TOP, fill=tk.X)
        self.addNoReferWidget(skinTitleFrame, FrameKey.SkinTitle)

        skinSourceFrame = tk.Frame(skinTitleFrame)  # 皮肤标题第一行
        skinSourceFrame.pack(side=tk.TOP, fill=tk.X)
        self.addNoReferWidget(skinSourceFrame, FrameKey.SkinTitle)
        skinSourceLabel = tk.Label(skinSourceFrame, text="皮肤库", font=FrameConfig.font)
        skinSourceLabel.pack(side=tk.LEFT)
        self.addNoReferWidget(skinSourceLabel, FrameKey.SkinTitle)
        skinSourceSetBtn = tk.Button(skinSourceFrame, text="更新", font=FrameConfig.font)
        skinSourceSetBtn.pack(side=tk.RIGHT)
        self.addNoReferWidget(skinSourceSetBtn, FrameKey.SkinTitle)
        skinSource = tk.Label(
            skinSourceFrame, text=self.getSkinPathText(), font=FrameConfig.font
        )
        skinSource.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        skinSource.bind(Event.MouseLefClick, self.selectSkinSource)  # 选择皮肤路径事件
        self.addReferWidget(skinSource, FrameKey.SkinSourcePath)

        modSourceFrame = tk.Frame(skinTitleFrame)  # 皮肤标题第二行
        modSourceFrame.pack(side=tk.TOP, fill=tk.X)
        self.addNoReferWidget(modSourceFrame, FrameKey.SkinTitle)
        modSourceLabel = tk.Label(modSourceFrame, text="Mods", font=FrameConfig.font)
        modSourceLabel.pack(side=tk.LEFT)
        self.addNoReferWidget(skinSourceLabel, FrameKey.SkinTitle)
        modSourceBtn = tk.Button(modSourceFrame, text="更新", font=FrameConfig.font)
        modSourceBtn.pack(side=tk.RIGHT)
        self.addNoReferWidget(modSourceBtn, FrameKey.SkinTitle)
        modSource = tk.Label(
            modSourceFrame, text=self.getModPathText(), font=FrameConfig.font
        )  # 3dmigoto目标路径
        modSource.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.addReferWidget(modSource, FrameKey.ModSourcePath)

        skinContentFrame = tk.Frame(pageFrame, background="brown")  # 显示皮肤内容一栏
        skinContentFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.addBaseFrame(skinContentFrame, FrameKey.SkinContent)

    def initRoleListPage(self):
        """初始化角色列表页面"""
        skincontentFrame = self.getBaseFrame(FrameKey.SkinContent)

        roleListCanvas = tk.Canvas(skincontentFrame, background="pink")  # 角色选择页面画布
        roleListScrollX = tk.Scrollbar(
            skincontentFrame, orient=tk.HORIZONTAL, width=2, background="green"
        )  # 横向滚动条
        roleListScrollY = tk.Scrollbar(
            skincontentFrame, orient=tk.VERTICAL, width=2, background="blue"
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

        roleListFrame = tk.Frame(roleListCanvas, background="white", borderwidth=5)
        roleListCanvas.create_window(0, 0, window=roleListFrame, anchor=tk.NW)
        self.addNoReferWidget(roleListScrollX, FrameKey.SkinContent)
        self.addNoReferWidget(roleListScrollY, FrameKey.SkinContent)
        self.addScrollCanvas(
            roleListCanvas, FrameKey.SkinContentFrame, tk.BOTH
        )  # 缓存滚动画布
        self.addBaseFrame(roleListFrame, FrameKey.SkinContentFrame)  # 缓存动态主组件

    def updateRoleList(self):
        """更新角色列表控件"""
        self.clearWidgetPool(FrameKey.SkinContentFrame)  # 清空角色内容页

        skinSourcePath = self.manager.getSkinPath()  # 皮肤库路径
        if skinSourcePath != None and os.path.exists(skinSourcePath):
            roleIndex = 0
            roleListFrame = self.getBaseFrame(FrameKey.SkinContentFrame)
            for roleDir in os.listdir(skinSourcePath):
                rolePath = os.path.join(skinSourcePath, roleDir)
                if os.path.isdir(rolePath) and RoleKey.existRole(roleDir):
                    imageIcon = self.getRoleImage(roleDir, rolePath)
                    rowIndex = (roleIndex // 10) + 1
                    columnIndex = (roleIndex % 10) + 1

                    imageFrame = tk.Frame(roleListFrame)  # 单个角色框架
                    imageFrame.grid(row=rowIndex, column=columnIndex)
                    self.addNoReferWidget(imageFrame, FrameKey.SkinContentFrame)

                    imageBtn = tk.Button(imageFrame, image=imageIcon)  # 角色图片按钮
                    imageBtn.pack(side=tk.TOP)
                    imageBtn.bind(Event.MouseLefClick,utils.eventAdaptor(self.clickSelectRole,key=roleDir))
                    self.addNoReferWidget(imageFrame, FrameKey.SkinContentFrame)

                    imageLabel = tk.Label(
                        imageFrame,
                        text=RoleKey.getRoleText(roleDir),
                        font=FrameConfig.font,
                    )  # 角色名
                    imageLabel.pack(side=tk.TOP)
                    self.addNoReferWidget(imageFrame, FrameKey.SkinContentFrame)

                    roleIndex += 1

        self.updateScrollFrame(FrameKey.SkinContent, FrameKey.SkinContentFrame)

    def updateSkinListPage(self):
        """更新单个角色的皮肤列表"""
        self.clearWidgetPool(FrameKey.SkinContentFrame)  # 清空角色内容页
        self.updateScrollFrame(FrameKey.SkinContent, FrameKey.SkinContentFrame)

    ####################getter&setter#####################

    def getMainFrame(self) -> tk.Tk:
        """主窗口"""
        return self.mainWindow

    def getScrollCanvas(self, key: str) -> dict | None:
        """获取对应的滚动画布"""
        if key in self.scrollCanvasPool:
            return self.scrollCanvasPool[key]
        return None

    def getBaseFrame(self, key: str) -> tk.Frame | None:
        """获取动态变化主组件"""
        if key in self.baseFramePool:
            return self.baseFramePool[key]
        return None

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

    def getReferWidget(self, key: str) -> tk.Widget | None:
        """获取动态控件"""
        if key in self.referPool:
            return self.referPool[key]
        return None

    #####################Add&Modify&Delete##############

    def getDefaultRoleImage(self) -> tk.PhotoImage:
        """获取默认的角色图片"""
        if FrameConfig.defaultRoleKey not in self.roleImagePool:
            image = Image.open(sys.path[0] + "/" + FrameConfig.defaultRole).resize(
                FrameConfig.roleIconSize
            )
            image = ImageTk.PhotoImage(image)
            self.addRoleImage(image, FrameConfig.defaultRoleKey)
        return self.roleImagePool[FrameConfig.defaultRoleKey]

    def addRoleImage(self, image: tk.PhotoImage, key: str):
        """缓存角色图片"""
        self.roleImagePool[key] = image

    def addBaseWidget(self, widget: tk.Widget):
        """缓存基础控件"""
        self.baseWidgetPool.append(widget)

    def addScrollCanvas(self, widget: tk.Canvas, key: str, scroll: str):
        """缓存可滚动的画布"""
        self.scrollCanvasPool[key] = {
            FrameKey.InfoCanvas: widget,
            FrameKey.InfoScroll: scroll,
        }

    def addBaseFrame(self, widget: tk.Frame, key: str):
        """缓存动态变化的主组件"""
        self.baseFramePool[key] = widget

    def addNoReferWidget(self, widget: tk.Widget, key: str):
        """缓存不会被引用的控件"""
        if key not in self.noReferPool:
            self.noReferPool[key] = []
        self.noReferPool[key].append(widget)
        if key in self.scrollCanvasPool:
            self.bindScrollEvent(widget, key)  # 绑定控件事件

    def addReferWidget(self, widget: tk.Widget, key: str):
        """缓存被引用的控件"""
        self.referPool[key] = widget

    def clearWidgetPool(self, key: str):
        """清空控件池"""
        if key in self.referPool:
            referWidgets = self.referPool[key]
            for widget in referWidgets:
                if isinstance(widget, tk.Widget):
                    widget.destroy()
            self.referPool[key] = []
        if key in self.noReferPool:
            noReferWidgets = self.noReferPool[key]
            for widget in noReferWidgets:
                if isinstance(widget, tk.Widget):
                    widget.destroy()
            self.noReferPool[key] = []

    ####################Function#########################
    def bindScrollEvent(self, widget: tk.Widget, key: str):
        """为控件绑定画布滚动事件"""
        canvasInfo = self.getScrollCanvas(key)
        if canvasInfo != None:
            scrollType = canvasInfo[FrameKey.InfoScroll]
            canvas = canvasInfo[FrameKey.InfoCanvas]
            if canvas != None and isinstance(canvas, tk.Canvas):
                if scrollType == tk.X:
                    widget.bind(
                        Event.MouseWheel,
                        utils.eventAdaptor(self.scrollHoriCanvas, widget=canvas),
                    )
                elif scrollType == tk.Y:
                    widget.bind(
                        Event.MouseWheel,
                        utils.eventAdaptor(self.scrollVerticalCanvas, widget=canvas),
                    )
                elif scrollType == tk.BOTH:
                    widget.bind(
                        Event.MouseWheel,
                        utils.eventAdaptor(self.scrollHoriCanvas, widget=canvas),
                    )
                    widget.bind(
                        Event.MouseWheel,
                        utils.eventAdaptor(self.scrollVerticalCanvas, widget=canvas),
                    )

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
        canvasInfo = self.getScrollCanvas(FrameKey.SideBar)
        if canvasInfo != None:
            canvas = canvasInfo[FrameKey.InfoCanvas]
            if canvas != None and isinstance(canvas, tk.Canvas):
                if self.sideBarSwitch:
                    canvas.pack_forget()
                else:
                    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
                    self.updateScrollFrame(FrameKey.SideBarParent, FrameKey.SideBar)
                self.sideBarSwitch = not self.sideBarSwitch

    def selectSkinSource(self, event):
        """选择皮肤库路径"""
        filePath = askdirectory()
        skinLabel = self.getReferWidget(FrameKey.SkinSourcePath)
        if (
            not utils.isEmpty(filePath)
            and skinLabel != None
            and isinstance(skinLabel, tk.Label)
        ):
            skinLabel.config(text=filePath)
            self.manager.setSkinPath(filePath)
            self.updateRoleList()

    def clickSelectRole(self, event, key:str):
        """点击某一角色图标"""
        self.updateSkinListPage()

    ####################debugger########################

    def testVerticalScrollBar(
        self, widget: tk.Widget, amount: int, width: int, height: int
    ):
        """测试竖直方式的滚动条"""
        for i in range(amount):
            button = tk.Button(
                widget, background="gray", text=str(i), width=width, height=height
            )
            button.pack(side=tk.TOP, fill=tk.X, expand=1)

    def testHoriScrollBar(
        self, widget: tk.Widget, amount: int, width: int, height: int
    ):
        """测试竖直方式的滚动条"""
        for i in range(amount):
            button = tk.Button(
                widget, background="gray", text=str(i), width=width, height=height
            )
            button.pack(side=tk.LEFT, fill=tk.Y, expand=1)

    def addTestWidget(self, widget: tk.Widget):
        """添加测试控件"""
        self.testWidgetPool.append(widget)

    def testEvent(self, event, widget: tk.Canvas):
        """测试事件"""
        widget.yview_scroll(10, tk.UNITS)


if __name__ == "__main__":
    MainFrame()
