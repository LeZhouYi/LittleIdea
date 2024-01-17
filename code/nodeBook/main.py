import tkinter as tk
from config.config import Config
from config.style import Style
from control.widgetControl import WidgetController
from control.event import WmEvent
from config.pwdbook import PwdBook

class MainFrame:
    def __init__(self) -> None:
        self.__initBaseData()
        self.loadBaseFrame()  # 基础框架
        self.loadSideBar() #侧边栏
        self.loadPasswordNote() #密码本页面
        self.mainWindow.mainloop()  # 显示窗口

    def __initBaseData(self) -> None:
        """初始化必要数据"""
        # 本地数据配置/缓存池
        self.config = Config()
        self.style = Style(self.config.getStylePath())  # 样式配置
        self.widgetController = WidgetController()

        # 初始化主窗口
        self.mainWindow = tk.Tk()
        self.mainWindow.geometry(self.config.getGeometry())
        self.mainWindow.title(self.config.getTitle())
        self.mainWindow.protocol(WmEvent.WindowClose, self.onWindowClose)

        # 缓存控件
        self.cacheWidget(self.mainWindow, None, "baseWindow")

    def cacheWidget(self, widget: tk.Widget, parentKey: str, key: str) -> None:
        """缓存控件"""
        self.widgetController.cacheWidget(
            widget, parentKey, key, self.style.getPackCnf(key)
        )

    def getWidget(self, key: str) -> tk.Widget:
        """获取控件"""
        return self.widgetController.getWidget(key)

    def updateCanvas(self,canvas:tk.Canvas,frame:tk.Frame,parentKey:str):
        """更新滚动画布控件"""
        self.getWidget(parentKey).update()
        canvas.config(
            scrollregion=frame.bbox(tk.ALL),
            width=frame.winfo_width(),
            height=frame.winfo_height(),
        )

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

    #######渲染页面相关############
    def loadBaseFrame(self) -> None:
        """渲染基础框"""
        sideBarFrame = tk.Frame(self.mainWindow, self.style.getCnf("sideBarFrame"))
        contentFrame = tk.Frame(self.mainWindow, self.style.getCnf("contentFrame"))

        self.cacheWidget(sideBarFrame, "baseWindow", "sideBarFrame")
        self.cacheWidget(contentFrame, "baseWindow", "contentFrame")

    def loadSideBar(self) -> None:
        """侧边栏"""
        sideBarFrame = self.getWidget("sideBarFrame")
        passwordBookBtn = tk.Button(sideBarFrame, self.style.getCnf("passwordBookBtn"))

        self.cacheWidget(passwordBookBtn,"sideBarFrame","passwordBookBtn")

    def loadPasswordNote(self)->None:
        """密码本页面"""
        self.passwordBook = PwdBook(self.config.getPwdBook())

        contentFrame = self.getWidget("contentFrame")
        pwdDispalyFrame = tk.Frame(contentFrame,self.style.getCnf("pwdDispalyFrame"))
        pwdScrollCanvas = tk.Canvas(pwdDispalyFrame,self.style.getCnf("pwdScrollCanvas"))
        pwdContentFrame = tk.Frame(pwdScrollCanvas,self.style.getCnf("pwdContentFrame"))

        for groupKey in self.passwordBook.getGroupKeys():
            group = self.passwordBook.getGroup(groupKey)
            pwdSingleFrame = tk.Frame()

        pwdScrollCanvas.create_window(0, 0, window=pwdContentFrame, anchor=tk.NW)

        self.cacheWidget(pwdDispalyFrame,"contentFrame","pwdDispalyFrame")
        self.cacheWidget(pwdScrollCanvas,"pwdDispalyFrame","pwdScrollCanvas")
        self.cacheWidget(pwdContentFrame,"pwdScrollCanvas","pwdContentFrame")

        self.updateCanvas(pwdScrollCanvas,pwdContentFrame,"pwdDispalyFrame") #更新


if __name__ == "__main__":
    MainFrame()
