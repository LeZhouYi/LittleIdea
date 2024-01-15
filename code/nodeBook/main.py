import tkinter as tk
from config.config import Config
from control.widgetControl import WidgetController as wc


class MainFrame:
    def __init__(self) -> None:
        self.__initBaseData()

    def __initBaseData(self):
        """初始化必要数据"""
        self.config = Config()  # 本地数据设置
        self.widgetController = wc.WidgetController()  # 控件池

        self.mainWindow = tk.Tk()  # 主窗口
        self.mainWindow.geometry(self.config.getGeometry())
        self.mainWindow.title(self.config.getTitle())  # 标题

        self.cacheWidget(self.mainWindow, None, "BaseWindow", None)  # 缓存主窗

    def cacheWidget(
        self, widget: tk.Widget, parentKey: str, key: str, cnf: dict
    ) -> None:
        """缓存控件"""
        self.widgetController.cacheWidget(widget, parentKey, key, cnf)


if __name__ == "__main__":
    MainFrame()
