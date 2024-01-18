from config.config import Config
from config.style import Style
from config.page import Page
from control.widgetControl import WidgetController
from control.threadControl import ThreadController

"""控制模块集"""
class Controller:

    def __init__(self) -> None:
        self.config = Config()
        self.style = Style(self.config.getStylePath())  # 样式配置
        self.page = Page(self.config.getPagePath(),self.config.getNowPage())
        self.widgetController = WidgetController()
        self.threadController = ThreadController()#线程池

    def getConfig(self)->Config:
        return self.config

    def getWidgetController(self)->WidgetController:
        return self.widgetController

    def getStyle(self)->Style:
        return self.style

    def getPage(self)->Page:
        return self.page

    def getThreadController(self)->ThreadController:
        return self.threadController