import tkinter as tk

def centerWindow(window:tk.Tk,width:int,height:int):
    '''
    使当前的窗口居中
    window:当前窗体
    width:当前窗体的宽
    heigth:当前窗体的高
    '''
    maxWindowWidth,maxWindowHeight = window.winfo_screenwidth(),window.winfo_screenheight()
    centerWindowSize = f'{width}x{height}+{round((maxWindowWidth-width)/2)}+{round((maxWindowHeight-height)/2)}'
    window.geometry(centerWindowSize)

def eventAdaptor(fun, **kwds):
    '''
    fun:当前要绑定的方法
    kwds:要传入的额外参数，需带参数名(eg. sudoku=sudoku)
    '''
    return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)

class MainFrame(object):

    def __init__(self) -> None:

        self.mainWindow = tk.Tk()
        #基本配置
        self.mainWindow.title("繁简体转换@Skily_Leyu")
        # centerWindow(self.mainWindow,500,500)
        self.mainWindow.resizable(0,0)

        self.inputEntry = tk.Text(self.mainWindow,undo=True,autoseparators=False)
        self.inputEntry.grid(column=0,row=0,padx='4px',columnspan=2)
        self.transButton1 = tk.Button(self.mainWindow,text="简转繁")
        self.transButton1.grid(column=0,row=1)
        self.transButton1 = tk.Button(self.mainWindow,text="繁转简")
        self.transButton1.bind('<1>',eventAdaptor(self.toSimple))
        self.transButton1.grid(column=1,row=1)

        self.mainWindow.mainloop() #显示窗口

    def toSimple(self,event):
        text = self.getInputText()

    def getInputText(self)->str:
        return self.inputEntry.get(1.0, tk.END)

if __name__ == '__main__':
    MainFrame()