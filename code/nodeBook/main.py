import tkinter as tk
from config.config import Config
from control.widgetControl import WidgetController
from control.event import WmEvent


class MainFrame:
    def __init__(self) -> None:
        self.__initBaseData()
        self.mainWindow.mainloop()  # 显示窗口

    def __initBaseData(self):
        """初始化必要数据"""
        # 本地数据配置/缓存池
        self.config = Config()
        self.widgetController = WidgetController()

        # 初始化主窗口
        self.mainWindow = tk.Tk()
        self.mainWindow.geometry(self.config.getGeometry())
        self.mainWindow.title(self.config.getTitle())
        self.mainWindow.protocol(WmEvent.WindowClose, self.onWindowClose)

        # 缓存控件
        self.cacheWidget(self.mainWindow, None, "BaseWindow", None)

    def cacheWidget(
        self, widget: tk.Widget, parentKey: str, key: str, cnf: dict
    ) -> None:
        """缓存控件"""
        self.widgetController.cacheWidget(widget, parentKey, key, cnf)

    ###############控件事件###################

    def onWindowClose(self):
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


if __name__ == "__main__":
    MainFrame()
