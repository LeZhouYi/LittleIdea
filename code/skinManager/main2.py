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
from data2 import RoleKey,FrameConfig,FrameKey,Event


class MainFrame:
    def __init__(self):
        self.manager = Manager()  # 数据
        self.mainWindow = tk.Tk()  # 主窗口

        # 基本配置
        self.initWindow()
        self.initWidgetPool()  # 初始化控件池
        self.initSideBar()  # 初始化侧边栏
        self.initSideBarContent()  # 初始化侧边栏内容
        self.initPage()  # 初始化页面
        self.initSkinManagerPage() #初始化皮肤管理页面
        self.mainWindow.mainloop()  # 显示窗口

    ####################init############################

    def initWindow(self):
        """初始化窗口"""
        self.mainWindow.title(FrameConfig.frameTitle)
        self.mainWindow.attributes("-fullscreen", True)  # 全屏
        self.mainWindow.bind(Event.F4, self.close)  # F4退出程序
        self.mainWindow.bind(Event.Escape, self.close)
        self.baseFont = FrameConfig.font #设置字体

    def initWidgetPool(self):
        """初始化控件池"""
        self.baseWidgetPool = []  # 基础控件缓存(不会变化，不会被引用)
        self.baseFramePool = {}  # 框架主组件缓存(会变化，且被引用)

        self.scrollCanvasPool = {}  # 可滚动画布缓存，用于绑定画布的滚动事件(被引用)
        self.noReferPool = {}  # 动态缓存控件（会被清空，不会被引用）
        self.referPool = {} #动态缓存控件（会被清空，会被引用）

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
        self.addBaseFrame(sideBarFrame,FrameKey.SideBarParent)

    def initSideBarContent(self):
        """初始化侧边栏动态控件"""
        mainFrame = self.getBaseFrame(FrameKey.SideBar)
        skinManagerBtn = tk.Button(mainFrame, text="皮肤管理", font=self.baseFont, width=15)
        skinManagerBtn.pack(side=tk.BOTTOM, fill=tk.X)
        self.addNoReferWidget(skinManagerBtn,FrameKey.SideBar)
        self.updateSideFrame()

    def updateSideFrame(self):
        """更新侧边栏"""
        self.getBaseFrame(FrameKey.SideBarParent).update()
        canvasInfo = self.getScrollCanvas(FrameKey.SideBar)
        frame = self.getBaseFrame(FrameKey.SideBar)
        if canvasInfo != None and frame != None:
            canvas = canvasInfo[FrameKey.InfoCanvas]
            if canvas != None and isinstance(canvas, tk.Canvas):
                canvas.config(
                    scrollregion=frame.bbox(tk.ALL),
                    width=frame.winfo_width(),
                )  # 设定画布可滚区域及自适应内容

    def initPage(self):
        """初始化内容页面"""
        pageFrame = tk.Frame(self.getMainFrame(), background="green")  # 页面栏基础框
        pageFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.addBaseFrame(pageFrame,FrameKey.Page)

    def initSkinManagerPage(self):
        """初始化皮肤管理页面"""
        pageFrame = self.getBaseFrame(FrameKey.Page)
        skinTitleFrame = tk.Frame(pageFrame)#显示皮肤标题一栏
        skinTitleFrame.pack(side=tk.TOP,fill=tk.X)
        self.addNoReferWidget(skinTitleFrame,FrameKey.SkinTitle)

        skinSourceFrame = tk.Frame(skinTitleFrame) #皮肤标题第一行
        skinSourceFrame.pack(side=tk.TOP,fill=tk.X)
        self.addNoReferWidget(skinSourceFrame,FrameKey.SkinTitle)
        skinSourceLabel = tk.Label(skinSourceFrame,text="皮肤库",font=FrameConfig.font)
        skinSourceLabel.pack(side=tk.LEFT)
        self.addNoReferWidget(skinSourceLabel,FrameKey.SkinTitle)
        skinSource = tk.Label(skinSourceFrame,text="请选择皮肤库路径",font=FrameConfig.font)
        skinSource.pack(side=tk.LEFT,fill=tk.X)
        self.addReferWidget(skinSource,FrameKey.SkinSourcePath)
        skinSourceSetBtn = tk.Button(skinSourceFrame,text="更新",font=FrameConfig.font)
        skinSourceSetBtn.pack(side=tk.LEFT)
        self.addNoReferWidget(skinSourceSetBtn,FrameKey.SkinTitle)

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

    #####################Add&Modify&Delete##############

    def addBaseWidget(self, widget: tk.Widget):
        """缓存基础控件"""
        self.baseWidgetPool.append(widget)

    def addScrollCanvas(self, widget: tk.Canvas, key: str, scroll: str):
        """缓存可滚动的画布"""
        self.scrollCanvasPool[key] = {FrameKey.InfoCanvas: widget, FrameKey.InfoScroll: scroll}

    def addBaseFrame(self, widget: tk.Frame, key: str):
        """缓存动态变化的主组件"""
        self.baseFramePool[key] = widget

    def addNoReferWidget(self,widget:tk.Widget,key:str):
        """缓存不会被引用的控件"""
        if key not in self.noReferPool:
            self.noReferPool[key] = []
        self.noReferPool[key].append(widget)
        if key in self.scrollCanvasPool:
            self.bindScrollEvent(widget,key) #绑定控件事件

    def addReferWidget(self,widget:tk.Widget,key:str):
        """缓存被引用的控件"""
        self.referPool[key]=widget

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

    def addTestWidget(self, widget: tk.Widget):
        """添加测试控件"""
        self.testWidgetPool.append(widget)

    def testEvent(self, event, widget: tk.Canvas):
        """测试事件"""
        widget.yview_scroll(10,tk.UNITS)


if __name__ == "__main__":
    MainFrame()