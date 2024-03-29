import tkinter as tk
import inspect
import ctypes
import threading
import os

def isEmpty(valueStr:str)->bool:
    """判断字符串为空"""
    return valueStr == None or valueStr == ""

def isNotEmpty(valueStr:str)->bool:
    """判断字符串非空"""
    return valueStr != None and valueStr!=""

def isPhoto(fileName:str)->bool:
    """判断当前文件为图片"""
    return fileName.endswith(".png") or fileName.endswith(".PNG") or fileName.endswith(".jpg")

def centerWindow(window:tk.Tk,width:int,height:int):
    """
    使当前的窗口居中
    window:当前窗体
    width:当前窗体的宽
    heigth:当前窗体的高
    """
    maxWindowWidth,maxWindowHeight = window.winfo_screenwidth(),window.winfo_screenheight()
    centerWindowSize = f"{width}x{height}+{round((maxWindowWidth-width)/2)}+{round((maxWindowHeight-height)/2)}"
    window.geometry(centerWindowSize)

def eventAdaptor(fun, **kwds):
    """
    fun:当前要绑定的方法
    kwds:要传入的额外参数，需带参数名(eg. sudoku=sudoku)
    """
    return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you"re in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def stopThread(thread:threading.Thread):
    """停止线程"""
    if thread!=None and thread.is_alive():
        _async_raise(thread.ident, SystemExit)

def isWidget(widget: tk.Widget, widgetClass):
    """判断当前是否对应的控件"""
    return widget != None and isinstance(widget, widgetClass)

def isPathExist(path:str)->bool:
    """判断路径是否存在"""
    return isNotEmpty(path) and os.path.exists(path) and os.path.isdir(path)

def createDir(path:str):
    """创建文件夹"""
    if not os.path.exists(path):
        os.mkdir(path)

def getCropStage(width:int,height:int)->tuple|None:
    """获取剪切策略"""
    if width == 1920 and height== 1080:
        return (715,100,1205,1080)
    elif width == 3840 and height == 2160:
        return (1430,200,2410,2160)
    return None