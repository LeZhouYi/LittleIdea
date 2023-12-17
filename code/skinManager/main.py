import os
import sys
import tkinter as tk
import utils
import data
from tkinter.filedialog import askdirectory
from manager import Manager
from PIL import Image, ImageTk
from tkinter import ttk
from threading import Thread
from time import sleep
import shutil


class MainFrame:
    def __init__(self):
        self.manager = Manager()  # 数据
        self.mainWindow = tk.Tk()  # 主窗口
        self.roleIconPool = {}  # 角色图示池
        self.btnSkinPool = []  # 皮肤控件池
        self.skinImagePool = []  # 皮肤预览图片池
        self.nowSelectRole = None  # 当前查看的角色

        # 基本配置
        self.initWindow()
        self.initBaseFrame()
        self.initRolesFrame()
        self.initRolesContent()
        self.mainWindow.mainloop()  # 显示窗口

    ####################init############################

    def initWindow(self):
        """初始化窗口"""
        self.mainWindow.title("Skin Manager")
        self.mainWindow.attributes("-fullscreen", True)
        self.mainWindow.bind("<Key-F4>", self.close)
        self.mainWindow.bind("<Escape>", self.back)

    def initBaseFrame(self):
        """初始化界面的大框架"""
        self.frame0 = tk.Frame(self.mainWindow)  # 侧边栏
        self.frame0.pack(side=tk.LEFT, fill=tk.Y, ipadx=80)

        self.margin0 = ttk.Separator(self.mainWindow, orient=tk.VERTICAL)  # 分隔线
        self.margin0.pack(side=tk.LEFT, fill=tk.Y, ipadx=3, ipady=3)

        self.frame1 = tk.Frame(self.mainWindow, bg="blue")  # 标题栏
        self.frame1.pack(side=tk.TOP, anchor=tk.NW, fill=tk.X)

        self.initContentFrame(True)

    def initContentFrame(self, isFirst: bool):
        """isFirst为True表示初始化，False表示清空"""
        if not isFirst and self.frame2 != None:
            self.frame2.destroy()  # 初始化
        self.frame2 = tk.Frame(self.mainWindow)  # 内容栏
        self.frame2.pack(fill=tk.BOTH, expand=1)

    def initRolesFrame(self):
        """初始化角色列表页面框架"""
        self.margin10 = ttk.Separator(self.frame1, orient=tk.HORIZONTAL)
        self.margin10.pack(side=tk.TOP, fill=tk.X, ipadx=3, ipady=2)
        self.frame10 = tk.Frame(self.frame1)  # 皮肤库一行
        self.frame10.pack(side=tk.TOP, fill=tk.X)
        self.label100 = tk.Label(
            self.frame10,
            height=1,
            text="皮肤库",
            font=data.FONT,
            anchor=tk.N,
            width=3,
        )
        self.label100.pack(side=tk.LEFT, anchor=tk.NW, ipadx=30, fill=tk.NONE)
        self.margin100 = ttk.Separator(self.frame10, orient=tk.VERTICAL)
        self.margin100.pack(side=tk.LEFT, fill=tk.Y, ipadx=3, ipady=3)
        self.label101 = tk.Label(
            self.frame10,
            height=1,
            text=self.getSkinPathTxt(),
            font=data.FONT,
            anchor=tk.W,
        )
        self.label101.pack(side=tk.TOP, anchor=tk.NW, fill=tk.X)
        self.label101.bind("<Button-1>", utils.eventAdaptor(self.chooseSkinPath))

        self.margin11 = ttk.Separator(self.frame1, orient=tk.HORIZONTAL)
        self.margin11.pack(side=tk.TOP, fill=tk.X, ipadx=3, ipady=3)

        self.frame11 = tk.Frame(self.frame1)  # mods一行
        self.frame11.pack(side=tk.TOP, fill=tk.X)
        self.lable110 = tk.Label(
            self.frame11,
            height=1,
            text="Mods",
            font=data.FONT,
            anchor=tk.N,
            width=3,
        )
        self.lable110.pack(side=tk.LEFT, anchor=tk.NW, ipadx=30, fill=tk.NONE)
        self.margin110 = ttk.Separator(self.frame11, orient=tk.VERTICAL)
        self.margin110.pack(side=tk.LEFT, fill=tk.Y, ipadx=3, ipady=3)
        self.label111 = tk.Label(
            self.frame11,
            height=1,
            text=self.getModPathTxt(),
            font=data.FONT,
            anchor=tk.W,
        )
        self.label111.pack(side=tk.TOP, anchor=tk.NW, fill=tk.X)
        self.label111.bind("<Button-1>", utils.eventAdaptor(self.chooseModsPath))

        self.margin12 = ttk.Separator(self.frame1, orient=tk.HORIZONTAL)
        self.margin12.pack(side=tk.TOP, fill=tk.X, ipadx=3, ipady=3)

    def initRolesContent(self):
        """初始化角色选择内容页"""
        self.clearContent()
        skinPath = self.manager.getSkinPath()
        if skinPath == None or not os.path.exists(skinPath):
            return
        for dirpath, dirnames, filenames in os.walk(skinPath):
            count = 0
            for dirname in dirnames:
                if data.existRole(dirname):
                    self.addSkinIconBtn(dirname, count)
                    count += 1

    def initRoleSkinFrame(self, key: str):
        """初始化单个角色皮肤选择界面"""
        self.clearContent()
        self.frame20 = tk.Frame(self.getContentFrame())  # 皮肤选择页面左侧栏
        self.frame20.pack(side=tk.LEFT, fill=tk.Y)
        roleIcon = self.getIconImage(key)  # 添加ICON
        if roleIcon != None:
            btn200 = tk.Label(self.frame20, image=roleIcon)
            btn200.pack(side=tk.TOP, anchor=tk.NW, ipadx=80)
            self.addBtnPool(btn200)

        margin20 = ttk.Separator(self.getContentFrame(), orient=tk.VERTICAL)
        margin20.pack(fill=tk.Y, side=tk.LEFT, ipadx=3)
        self.addBtnPool(margin20)

        self.frame21 = tk.Frame(self.getContentFrame())  # 皮肤列选择栏
        self.frame21.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.initSkinLines(key)

        margin201 = ttk.Separator(self.frame20, orient=tk.HORIZONTAL)
        margin201.pack(fill=tk.X, side=tk.TOP, ipady=1)
        self.addBtnPool(margin201)

        self.label200 = tk.Label(
            self.frame20, text="已选择皮肤:", height=1, font=data.FONT, anchor=tk.W
        )
        self.label201 = tk.Label(self.frame20, text="empty", height=1, font=data.FONT)
        self.label200.pack(side=tk.TOP, fill=tk.X)
        self.label201.pack(side=tk.TOP, fill=tk.X)
        margin202 = ttk.Separator(self.frame20, orient=tk.HORIZONTAL)
        margin202.pack(fill=tk.X, side=tk.TOP, ipady=1)
        self.addBtnPool(margin202)

        self.btn200 = tk.Button(self.frame20, text="替换", font=data.FONT)
        self.btn200.pack(side=tk.TOP, fill=tk.X)
        self.btn200.bind("<Button-1>", utils.eventAdaptor(self.clickReplaceSkin))

    def initSkinLines(self, key: str):
        """初始化该角色的所有皮肤的预览页面"""
        if self.frame21 != None:
            skinPath = self.getRoleFilePath(key)  # 获取角色文件夹
            for dirTemp in os.listdir(skinPath):  # 获取所有文件名
                pathTemp = os.path.join(skinPath, dirTemp)  # 构造完整 路径
                if os.path.isdir(pathTemp):  # 判断是否是路径
                    images = self.getSkinImages(pathTemp)  # 加载该路径所有图片
                    for image in images:
                        self.addSkinImageBtn(dirTemp, image)
            # for filename in os.listdir(skinPath):
            #     if utils.isPhoto(filename):
            #         pathStr = os.path.join(skinPath,filename)
            #         images = self.getSkinImages(skinPath + "/" + pathStr)
            #         for image in images:
            #             self.addSkinImageBtn(pathStr, image)

    def addSkinImageBtn(self, dirname: str, image: tk.PhotoImage):
        """将图片及文件名制作成相框添加"""
        frame21x = tk.Frame(self.frame21)  # 单个图片做一个分组
        btn21xx = tk.Button(frame21x, image=image)
        label21xx = tk.Label(frame21x, text=dirname, height=1)

        btn21xx.bind("<Button-1>", utils.eventAdaptor(self.chooseSkin, dirname=dirname))

        frame21x.pack(side=tk.LEFT, anchor=tk.NW)
        btn21xx.pack(side=tk.TOP, anchor=tk.NW)
        label21xx.pack(side=tk.TOP)

        self.addBtnPools(label21xx, btn21xx, frame21x)
        self.skinImagePool.append(image)

    def addSkinIconBtn(self, key: str, index: int):
        """添加皮肤按钮"""
        image = self.getIconImage(key)
        if image != None:
            rowIndex = (int)(index / 9) + 1
            columnIndex = (int)(index % 9 * 2) + 1

            btn2x = tk.Button(self.getContentFrame(), image=image)
            btn2x.grid(row=rowIndex, column=columnIndex, pady=5)
            btn2x.bind(
                "<Button-1>", utils.eventAdaptor(self.clickInputRoleSkins, key=key)
            )
            self.addBtnPool(btn2x)
            label2x = ttk.Label(self.getContentFrame(), width=3)
            label2x.grid(row=rowIndex, column=columnIndex + 1)
            self.addBtnPool(label2x)

    ####################event###########################

    def close(self, event):
        """关闭事件"""
        sys.exit()

    def back(self, event):
        """返回上一页"""
        if self.nowSelectRole == None:
            return
        elif self.nowSelectRole != None:
            self.nowSelectRole = None
            self.clearContent()
            self.initRolesContent()
            self.skinImagePool = []

    def clickInputRoleSkins(self, event, key: str):
        """点击进入单个角色皮肤选择页面"""
        self.nowSelectRole = key
        self.initRoleSkinFrame(key)

    def chooseSkinPath(self, event):
        """选择皮肤路径"""
        filePath = askdirectory()
        if not utils.isEmpty(filePath):
            self.label101.config(text=filePath)
            self.manager.setSkinPath(filePath)
            self.initRolesContent()

    def chooseModsPath(self, evnent):
        """选择3dmigoto mods 文件夹"""
        filePath = askdirectory()
        if not utils.isEmpty(filePath):
            self.label111.config(text=filePath)
            self.manager.setModsPath(filePath)

    def chooseSkin(self, event, dirname: str):
        """选择皮肤"""
        if self.label201 != None:
            self.label201.config(text=dirname)

    def clickReplaceSkin(self, event):
        """点击替换皮肤事件"""
        if self.btn200 != None and self.btn200["text"] == "替换":
            pathName = self.label201["text"]
            if utils.isEmpty(pathName) or pathName == "empty":
                self.btn200.config(text="替换(未选择皮肤)", fg="red")
                Thread(
                    target=self.replaceText, args=(self.btn200, "替换"), daemon=True
                ).start()
                return
            modsPath = self.label111["text"]
            if utils.isEmpty(modsPath) or modsPath == "请选择3dmigoto Mods文件夹":
                self.btn200.config(text="替换(未选择Mods文件夹)", fg="red")
                Thread(
                    target=self.replaceText, args=(self.btn200, "替换"), daemon=True
                ).start()
                return
            if not os.path.exists(modsPath):
                self.btn200.config(text="替换(Mods文件夹不存在)", fg="red")
                Thread(
                    target=self.replaceText, args=(self.btn200, "替换"), daemon=True
                ).start()
                return
            self.btn200.config(text="替换中......")
            Thread(
                target=self.replaceSkin, args=(modsPath, pathName), daemon=False
            ).start()

    def replaceSkin(self, modsPath: str, pathName: str) -> bool:
        """替换皮肤"""
        rolePath = modsPath + "/" + self.nowSelectRole
        if os.path.exists(rolePath):
            shutil.rmtree(rolePath)
        skinPath = self.getRoleFilePath(self.nowSelectRole) + "/" + pathName
        if os.path.exists(skinPath):
            print(skinPath)
            print(rolePath)
            shutil.copytree(skinPath, rolePath)
            self.btn200.config(text="替换成功！！", fg="cyan")
            Thread(
                target=self.replaceText, args=(self.btn200, "替换"), daemon=True
            ).start()
        else:
            self.btn200.config(text="替换失败(未知原因)", fg="red")
            Thread(
                target=self.replaceText, args=(self.btn200, "替换"), daemon=True
            ).start()

    def replaceText(self, btn: tk.Button, text: str):
        """替换按钮文本"""
        sleep(3)
        btn.config(text=text, fg="black")

    ####################getter&setter#####################
    def getSkinImages(self, path: str) -> list[tk.PhotoImage]:
        """获取该文件夹下所有图片"""
        images = []
        for filename in os.listdir(path):
            if utils.isPhoto(filename):
                filePath = os.path.join(path, filename)
                image = Image.open(filePath).resize((230, 450))
                images.append(ImageTk.PhotoImage(image))
        return images

    def getIconImage(self, key: str) -> tk.PhotoImage | None:
        """根据key获取对应角色的icon"""
        skinPath = self.getRoleFilePath(key)
        if key not in self.roleIconPool:
            for filename in os.listdir(skinPath):
                if utils.isPhoto(filename):
                    self.addRoleImage(key, skinPath + "/" + filename)
                    return self.roleIconPool[key]
        else:
            return self.roleIconPool[key]
        return None

    def getRoleFilePath(self, key: str):
        """获取角色图标路径"""
        return self.manager.getSkinPath() + "/" + key

    def getSkinPathTxt(self) -> str:
        """获取皮肤路径相关文本"""
        filePathTxt = self.manager.getSkinPath()
        if filePathTxt == None:
            filePathTxt = "请选择皮肤文件夹"
        return filePathTxt

    def getModPathTxt(self) -> str:
        """获取mods路径相关文本"""
        filePathTxt = self.manager.getModsPath()
        if filePathTxt == None:
            filePathTxt = "请选择3dmigoto Mods文件夹"
        return filePathTxt

    def getContentFrame(self) -> tk.Frame:
        """内容框"""
        return self.frame2

    def getTitleFrame(self) -> tk.Frame:
        """标题框"""
        return self.frame1

    ###################Modify&Delete&Add########################
    def addBtnPool(self, widget: tk.Widget):
        """把控件添加进临时缓存池"""
        self.btnSkinPool.append(widget)

    def addBtnPools(self, *args: tk.Widget):
        """把控件添加进临时缓存池"""
        for widget in args:
            self.btnSkinPool.append(widget)

    def clearContent(self):
        """清空Content的内容"""
        self.initContentFrame(False)
        self.btnSkinPool = []

    def addRoleImage(self, key: str, filePath: str):
        """添加角色的图片进缓存池"""
        if key not in self.roleIconPool:
            image = Image.open(filePath).resize((120, 160))
            self.roleIconPool[key] = ImageTk.PhotoImage(image)


if __name__ == "__main__":
    MainFrame()
