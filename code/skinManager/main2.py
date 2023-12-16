import os
import sys
import utils
import data
import shutil
import tkinter as tk
from tkinter.filedialog import askdirectory
from manager import Manager
from PIL import Image, ImageTk
from tkinter import ttk
from threading import Thread
from time import sleep


class MainFrame:
    def __init__(self):
        self.manager = Manager()  # 数据
        self.mainWindow = tk.Tk()  # 主窗口

        # 基本配置
        self.initWindow()
        self.initWidgetPool()  # 初始化控件池
        self.initSideBar()  # 初始化侧边栏
        self.initSideBarContent() #初始化侧边栏内容
        self.initPage()  # 初始化页面
        self.mainWindow.mainloop()  # 显示窗口

    ####################init############################

    def initWindow(self):
        """初始化窗口"""
        self.mainWindow.title(data.TITLE)
        self.mainWindow.attributes("-fullscreen", True)  # 全屏
        self.mainWindow.bind("<Key-F4>", self.close)  # F4退出程序

    def initWidgetPool(self):
        """初始化控件池"""
        self.baseWidgetPool = []  # 基础控件缓存
        self.scrollCanvasPool = {}  # 可滚动画布缓存，用于绑定画布的滚动事件
        self.baseFramePool = {}  # 框架主组件缓存
        self.sideBarPool = []  # 侧边栏控件缓存
        self.testWidgetPool = []  # 测试用缓存

    def initSideBar(self):
        """初始化侧边栏"""
        self.sideBarFrame = tk.Frame(self.getMainFrame(), background="yellow")  # 侧边栏基础框
        self.sideBarFrame.pack(side=tk.LEFT, fill=tk.Y, ipady=3)

        sideBarCanvas = tk.Canvas(self.sideBarFrame, background="blue")  # 侧边栏画布
        sideBarScroll = tk.Scrollbar(
            self.sideBarFrame, orient=tk.VERTICAL, width=2, background="pink"
        )  # 侧边栏竖向滚动条
        sideBarCanvas.config(
            yscrollcommand=sideBarScroll.set, yscrollincrement=1
        )  # 侧边栏画布关联竖直滚动条
        sideBarScroll.config(command=sideBarCanvas.yview)  # 滚动条关联画布y轴
        sideBarCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        sideBarScroll.pack(side=tk.RIGHT, fill=tk.Y)

        sideBarScrollFrame = tk.Frame(sideBarCanvas, background="pink", borderwidth=5)
        # self.testVerticalScrollBar(sideBarScrollFrame,3,20,3)
        sideBarCanvas.create_window(0, 0, window=sideBarScrollFrame, anchor=tk.NW)
        self.sideBarFrame.update()
        sideBarCanvas.config(
                    scrollregion=sideBarScrollFrame.bbox(tk.ALL),
                    width=sideBarScrollFrame.winfo_width(),
                )  # 设定画布可滚区域及自适应内容
        sideBarScrollFrame.bind(
            "<MouseWheel>",
            utils.eventAdaptor(self.scrollVerticalCanvas, widget=sideBarCanvas),
        )  # 绑定画布的滚动事件

        self.addBaseWidget(sideBarScroll)
        self.addScrollCanvas(sideBarCanvas,'sideBar',tk.Y) #缓存滚动画布
        self.addBaseFrame(sideBarScrollFrame,'sideBar') #缓存动态主组件
        # self.updateSideFrame()

    def initSideBarContent(self):
        """初始化侧边栏动态控件"""
        mainFrame = self.getBaseFrame('sideBar')
        skinManagerBtn = tk.Button(mainFrame,text="皮肤管理",font=data.FONT,width=15)
        skinManagerBtn.pack(side=tk.BOTTOM,fill=tk.X)
        self.addSideBarWidget(skinManagerBtn)
        self.updateSideFrame()

    def updateSideFrame(self):
        '''更新侧边栏'''
        self.getSideBarFrame().update()
        canvasInfo = self.getScrollCanvas('sideBar')
        frame = self.getBaseFrame('sideBar')
        if canvasInfo!=None and frame!=None:
            canvas = canvasInfo["canvas"]
            if canvas!=None and isinstance(canvas,tk.Canvas):
                canvas.config(
                    scrollregion=frame.bbox(tk.ALL),
                    width=frame.winfo_width(),
                )  # 设定画布可滚区域及自适应内容

    def initPage(self):
        """初始化内容页面"""
        pageFrame = tk.Frame(self.getMainFrame(), background="green")  # 页面栏基础框
        pageFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.addBaseWidget(pageFrame)

    ####################getter&setter#####################

    def getMainFrame(self) -> tk.Tk:
        """主窗口"""
        return self.mainWindow

    #####################Add&Modify&Delete##############

    def addBaseWidget(self, widget: tk.Widget):
        """缓存基础控件"""
        self.baseWidgetPool.append(widget)

    def addScrollCanvas(self, widget: tk.Canvas, key: str, scroll: str):
        """缓存可滚动的画布"""
        self.scrollCanvasPool[key] = {"canvas": widget, "scroll": scroll}

    def addBaseFrame(self, widget: tk.Frame, key: str):
        """缓存动态变化的主组件"""
        self.baseFramePool[key] = widget

    def addSideBarWidget(self,widget:tk.Widget):
        """缓存侧边栏动态的控件"""
        self.sideBarPool.append(widget)
        self.bindScrollEvent(widget,'sideBar')

    def getScrollCanvas(self,key:str)->dict|None:
        """获取对应的滚动画布"""
        if key in self.scrollCanvasPool:
            return self.scrollCanvasPool[key]
        return None

    def getBaseFrame(self,key:str)->tk.Frame|None:
        """获取动态变化主组件"""
        if key in self.baseFramePool:
            return self.baseFramePool[key]
        return None

    def getSideBarFrame(self)->tk.Frame:
        """获取侧边栏基础框架"""
        return self.sideBarFrame

    ####################Function#########################
    def bindScrollEvent(self,widget:tk.Widget,key:str):
        """为控件绑定画布滚动事件"""
        canvasInfo = self.getScrollCanvas(key)
        if canvasInfo!=None:
            scrollType = canvasInfo["scroll"]
            canvas = canvasInfo["canvas"]
            if canvas!=None and isinstance(canvas,tk.Canvas):
                if scrollType==tk.X:
                    widget.bind('<MouseWheel>',utils.eventAdaptor(self.scrollHoriCanvas,widget=canvas))
                elif scrollType==tk.Y:
                    widget.bind('<MouseWheel>',utils.eventAdaptor(self.scrollVerticalCanvas,widget=canvas))
                elif scrollType==tk.BOTH:
                    widget.bind('<MouseWheel>',utils.eventAdaptor(self.scrollHoriCanvas,widget=canvas))
                    widget.bind('<MouseWheel>',utils.eventAdaptor(self.scrollVerticalCanvas,widget=canvas))


    ####################event###########################

    def close(self, event):
        """关闭事件"""
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
        widget.yview_scroll(10, "units")
        print("tset")


if __name__ == "__main__":
    MainFrame()
