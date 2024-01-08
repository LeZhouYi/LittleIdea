import threading
import utils

"""
管理渲染线程
"""
class ThreadController:

    def __init__(self) -> None:
        self.threadPool = {} #线程池

    def cacheThread(self,thread:threading.Thread,key:str)->None:
        """缓存线程池并开始运行"""
        if key in self.threadPool:
            threadNow = self.threadPool[key]
            utils.stopThread(threadNow)
        self.threadPool[key]=thread
        thread.start()