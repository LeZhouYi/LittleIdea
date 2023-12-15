import os
import tkinter as tk
import utils
import data
from tkinter.filedialog import askdirectory
from manager import Manager
from PIL import Image, ImageTk


class MainFrame:
    def __init__(self):
        self.manager = Manager()
        self.mainWindow = tk.Tk()
        self.imagePool = {}

        # 基本配置
        self.mainWindow.title("Skin Manager")
        utils.centerWindow(self.mainWindow, 960, 540)
        self.initFrame()
        self.initSkinFrame()
        self.initSkinContent()
        self.mainWindow.mainloop()  # 显示窗口

    def initFrame(self):
        self.leftBarFrame = tk.Frame(self.mainWindow, bg="black", borderwidth=4)  # 侧边栏
        self.leftBarFrame.pack(side=tk.LEFT, fill=tk.Y, ipadx=80)
        self.rightTitleFrame = tk.Frame(self.mainWindow, bg="blue")  # 标题栏
        self.rightTitleFrame.pack(side=tk.TOP, anchor=tk.NW, fill=tk.X)
        self.contentFrame = tk.Frame(self.mainWindow, bg="green")  # 内容栏
        self.contentFrame.pack(fill=tk.BOTH, expand=1)

    def getSkinPathTxt(self) -> str:
        filePathTxt = self.manager.getSkinPath()
        if filePathTxt == None:
            filePathTxt = "请选择皮肤文件夹"
        return filePathTxt

    def getModPathTxt(self) -> str:
        filePathTxt = self.manager.getModsPath()
        if filePathTxt == None:
            filePathTxt = "请选择3dmigoto Mods文件夹"
        return filePathTxt

    def initSkinFrame(self):
        self.titleFrame0 = tk.Frame(self.rightTitleFrame)
        self.titleFrame0.pack(side=tk.TOP, fill=tk.X)
        self.skinPathLabel = tk.Label(
            self.titleFrame0,
            height=1,
            text="皮肤库",
            font=data.FONT,
            anchor=tk.N,
            width=3,
        )
        self.skinPathLabel.pack(side=tk.LEFT, anchor=tk.NW, ipadx=30, fill=tk.NONE)
        self.skinPathText = tk.Label(
            self.titleFrame0,
            height=1,
            text=self.getSkinPathTxt(),
            font=data.FONT,
            anchor=tk.W,
        )
        self.skinPathText.pack(side=tk.TOP, anchor=tk.NW, fill=tk.X)
        self.skinPathText.bind("<Button-1>", utils.eventAdaptor(self.chooseSkinPath))

        self.titleFrame1 = tk.Frame(self.rightTitleFrame)
        self.titleFrame1.pack(side=tk.TOP, fill=tk.X)
        self.modPathLabel = tk.Label(
            self.titleFrame1,
            height=1,
            text="Mods",
            font=data.FONT,
            anchor=tk.N,
            width=3,
        )
        self.modPathLabel.pack(side=tk.LEFT, anchor=tk.NW, ipadx=30, fill=tk.NONE)
        self.modPathText = tk.Label(
            self.titleFrame1,
            height=1,
            text=self.getModPathTxt(),
            font=data.FONT,
            anchor=tk.W,
        )
        self.modPathText.pack(side=tk.TOP, anchor=tk.NW, fill=tk.X)

    def initSkinContent(self):
        """初始化皮肤主界面"""
        skinPath = self.manager.getSkinPath()
        if skinPath == None or not os.path.exists(skinPath):
            return
        for dirpath, dirnames, filenames in os.walk(skinPath):
            for dirname in dirnames:
                if data.existRole(dirname):
                    self.addSkinIconBtn(dirname)

    def loadImage(self, key: str, filePath: str):
        image = Image.open(filePath)
        image = image.resize((120, 120))
        photo = ImageTk.PhotoImage(image)
        self.imagePool[key] = photo

    def getImage(self, key: str) -> tk.PhotoImage | None:
        return self.imagePool[key]

    def addSkinIconBtn(self, key: str):
        """添加皮肤按钮"""
        skinPath = self.manager.getSkinPath() + "/" + key
        for dirpath, dirnames, filenames in os.walk(skinPath):
            icons = list(filter(utils.isPhoto, filenames))
            if len(icons) > 0:
                self.loadImage(key, skinPath + "/" + icons[0])
                image = self.getImage(key)
                if image != None:
                    skinBtn = tk.Button(self.contentFrame, image=self.imagePool[key])
                    skinBtn.pack(side=tk.LEFT, anchor=tk.NW)

    def chooseSkinPath(self, event):
        """选择皮肤路径"""
        filePath = askdirectory()
        print(filePath)
        if filePath != None and filePath != "":
            self.skinPathText.config(text=filePath)
            self.manager.setSkinPath(filePath)
            self.initSkinContent()


if __name__ == "__main__":
    MainFrame()
