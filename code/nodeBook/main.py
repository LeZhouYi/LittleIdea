import threading
import tkinter as tk
from config.config import Config
from config.style import Style
from config.page import Page
from control.widgetControl import WidgetController
from control.threadControl import ThreadController
from control.event import WmEvent, Event
from config.pwdbook import PwdBook


class MainFrame:
    def __init__(self) -> None:
        self.__initBaseData()
        self.loadBaseFrame()  # 基础框架
        self.loadSideBar()  # 侧边栏
        self.cacheThread(self.loadPasswordNote,"content")  # 密码本页面
        self.mainWindow.mainloop()  # 显示窗口

    def __initBaseData(self) -> None:
        """初始化必要数据"""
        # 本地数据配置/缓存池
        self.config = Config()
        self.style = Style(self.config.getStylePath())  # 样式配置
        self.page = Page(self.config.getPagePath(),self.config.getNowPage())
        self.widgetController = WidgetController()
        self.threadController = ThreadController()#线程池

        # 初始化主窗口
        self.mainWindow = tk.Tk()
        self.mainWindow.geometry(self.config.getGeometry())
        self.mainWindow.title(self.config.getTitle())
        self.mainWindow.protocol(WmEvent.WindowClose, self.onWindowClose)
        self.mainWindow.bind(Event.WindowResize,self.onWindowResize)

        # 缓存控件
        self.cacheWidget(self.mainWindow, None, "baseWindow")

    def createKey(self,key:str,*args)->str:
        """创建Key"""
        for value in args:
            key=key+"_"+str(value)
        return key

    def setNowPage(self,nowPage:str):
        """设置当前页面"""
        self.config.setNowPage(nowPage)
        self.page.setNowPage(nowPage)

    def cacheWidget(self, widget: tk.Widget, parentKey: str, key: str) -> None:
        """缓存控件"""
        self.widgetController.cacheWidget(
            widget, parentKey, key, self.style.getPackCnf(key)
        )

    def cacheThread(self,func,key:str,args:iter=[]):
        """缓存线程"""
        self.threadController.cacheThread(threading.Thread(target=func,args=args),key)

    def getWidget(self, key: str) -> tk.Widget:
        """获取控件"""
        return self.widgetController.getWidget(key)

    def updateCanvas(self, canvas: tk.Canvas, frame: tk.Frame, parentKey: str):
        """更新滚动画布控件"""
        self.getWidget(parentKey).update()
        canvas.config(
            scrollregion=frame.bbox(tk.ALL),
            width=frame.winfo_width(),
            height=frame.winfo_height(),
        )

    def refreshCanvas(self,pageKey:str=None):
        """刷新当前页面"""
        pageWidgetKeys = self.page.resizeKeys(pageKey)
        pwdScrollCanvas=self.getWidget(pageWidgetKeys[0])
        pwdContentFrame = self.getWidget(pageWidgetKeys[1])
        pwdScrollCanvas.create_window(
            0,
            0,
            width=self.config.getContentPageWidth()+self.page.resizeWidthOffset(),
            window=pwdContentFrame,
            anchor=tk.NW,
        )
        self.updateCanvas(pwdScrollCanvas, pwdContentFrame, pageWidgetKeys[2])  # 更新

    ###############控件事件###################

    def onWindowClose(self) -> None:
        """处理窗口关闭事件"""
        # 获取窗口的宽度和高度
        width = self.mainWindow.winfo_width()
        height = self.mainWindow.winfo_height()
        # 获取窗口左上角在屏幕上的位置
        x = self.mainWindow.winfo_rootx()
        y = self.mainWindow.winfo_rooty()
        # 备份窗口信息
        self.config.setGeometry(width, height, x, y)
        self.config.writeToFile()
        # 关闭窗口
        self.mainWindow.destroy()

    def onWindowResize(self,event) -> None:
        """处理窗口刷新事件"""
        # 获取窗口的宽度和高度
        width = self.mainWindow.winfo_width()
        height = self.mainWindow.winfo_height()
        # 获取窗口左上角在屏幕上的位置
        x = self.mainWindow.winfo_rootx()
        y = self.mainWindow.winfo_rooty()
        if self.config.hasWindowResize(width,height):
            # 备份窗口信息
            self.config.setGeometry(width, height, x, y)
            self.refreshCanvas()

    #######渲染页面相关############
    def loadBaseFrame(self) -> None:
        """渲染基础框"""
        sideBarFrame = tk.Frame(self.mainWindow, cnf=self.style.getCnf("sideBarFrame"))
        contentFrame = tk.Frame(self.mainWindow, self.style.getCnf("contentFrame"))

        self.cacheWidget(sideBarFrame, "baseWindow", "sideBarFrame")
        self.cacheWidget(contentFrame, "baseWindow", "contentFrame")

    def loadSideBar(self) -> None:
        """侧边栏"""
        sideBarFrame = self.getWidget("sideBarFrame")
        passwordBookBtn = tk.Button(
            sideBarFrame, cnf=self.style.getCnf("passwordBookBtn")
        )
        self.cacheWidget(passwordBookBtn, "sideBarFrame", "passwordBookBtn")

    def loadPasswordNote(self) -> None:
        """密码本页面"""
        self.setNowPage("passwordDisplay")
        self.passwordBook = PwdBook(self.config.getPwdBook())

        contentFrame = self.getWidget("contentFrame")
        pwdDispalyFrame = tk.Frame(
            contentFrame, cnf=self.style.getCnf("pwdDispalyFrame")
        )
        pwdScrollCanvas = tk.Canvas(
            pwdDispalyFrame, cnf=self.style.getCnf("pwdScrollCanvas")
        )
        pwdContentFrame = tk.Frame(
            pwdScrollCanvas, cnf=self.style.getCnf("pwdContentFrame")
        )

        self.cacheWidget(pwdDispalyFrame, "contentFrame", "pwdDispalyFrame")
        self.cacheWidget(pwdScrollCanvas, "pwdDispalyFrame", "pwdScrollCanvas")
        self.cacheWidget(pwdContentFrame, "pwdScrollCanvas", "pwdContentFrame")

        frameCount = 0
        for groupKey in self.passwordBook.getGroupKeys():
            pwdSingleFrameKey = self.createKey("pwdSingleFrame",frameCount)
            pwdGroupLabelKey = self.createKey("pwdGroupLabel",frameCount)

            pwdSingleFrame = tk.Frame(
                pwdContentFrame, cnf=self.style.getCnf(pwdSingleFrameKey)
            )
            pwdGroupLabel = tk.Label(
                pwdSingleFrame, text=groupKey, cnf=self.style.getCnf(pwdGroupLabelKey)
            )
            self.cacheWidget(pwdSingleFrame, "pwdContentFrame", pwdSingleFrameKey)
            self.cacheWidget(pwdGroupLabel, "pwdContentFrame", pwdGroupLabelKey)

            group = self.passwordBook.getGroup(groupKey)
            envconut = 0
            for envkey, pwdList in group.items():
                pwdEnvFrameKey =self.createKey("pwdEnvFrame",frameCount,envconut)
                pwdEmptyKey = self.createKey("pwdEmptyLabel",frameCount,envconut)
                pwdEnvKey = self.createKey("pwdEnvLabel",frameCount,envconut)

                pwdEnvFrame = tk.Frame(pwdSingleFrame,cnf=self.style.getCnf(pwdEnvFrameKey))
                pwdEmptyLabel = tk.Label(pwdEnvFrame,cnf=self.style.getCnf(pwdEmptyKey))
                pwdEnvLabel = tk.Label(pwdEnvFrame,text=envkey,cnf=self.style.getCnf(pwdEnvKey))

                self.cacheWidget(pwdEnvFrame,pwdSingleFrameKey,pwdEnvFrameKey)
                self.cacheWidget(pwdEmptyLabel,pwdEnvFrameKey,pwdEmptyKey)
                self.cacheWidget(pwdEnvLabel,pwdEnvFrameKey,pwdEnvKey)
                envconut+=1
            frameCount += 1

        self.refreshCanvas()

if __name__ == "__main__":
    MainFrame()
