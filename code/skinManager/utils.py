import tkinter as tk

def isPhoto(fileName:str)->bool:
    return fileName.endswith(".png") or fileName.endswith(".PNG")

def centerWindow(window:tk.Tk,width:int,height:int):
    '''
    使当前的窗口居中
    window:当前窗体
    width:当前窗体的宽
    heigth:当前窗体的高
    '''
    maxWindowWidth,maxWindowHeight = window.winfo_screenwidth(),window.winfo_screenheight()
    centerWindowSize = f'{width}x{height}+{round((maxWindowWidth-width)/2)}+{round((maxWindowHeight-height)/2)}'
    print(centerWindowSize)
    window.geometry(centerWindowSize)

def eventAdaptor(fun, **kwds):
    '''
    fun:当前要绑定的方法
    kwds:要传入的额外参数，需带参数名(eg. sudoku=sudoku)
    '''
    return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)