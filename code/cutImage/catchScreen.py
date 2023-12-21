import sys
import os
import datetime
from pynput import keyboard
from mss import mss

def createDir(path:str):
    """创建文件夹"""
    if not os.path.exists(path):
        os.mkdir(path)

class CatchScreen:

    def onActived(self):
        print("start catch screen")
        path = sys.path[0]
        sourcePath = os.path.join(path,"sources")
        fileName = "%d.png"%datetime.datetime.now().timestamp()
        filePath = os.path.join(sourcePath,fileName)
        generater = mss().save(mon=2,output=filePath)
        next(generater)

    def stop(self):
        self.thread.stop()

    def listener(self):
        with keyboard.GlobalHotKeys({'<ctrl>+<alt>+z':self.onActived,
                                    '<ctrl>+<alt>+q':self.stop}) as self.thread:
            self.thread.join()

if __name__ == '__main__':
    CatchScreen().listener()