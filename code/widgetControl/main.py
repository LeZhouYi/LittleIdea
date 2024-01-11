import os
import utils
import threading
import shutil
import tkinter as tk
import widgetControl as wc
import threadControl as tc
import soruceControl as sc
from time import sleep
from PIL import Image, ImageTk
from config import Config
from data import Event
from tkinter.filedialog import askdirectory


class MainFrame:
    def __init__(self):
        self.__initBaseData()  # 初始化必要数据
        self.initRoleListFrame()  # 初始化角色列表页面
        self.mainWindow.mainloop()  # 显示窗口

    def __initBaseData(self):
        """初始化必要数据"""
        self.config = Config()  # 本地数据设置
        self.sourceController = sc.SourceController()#资源池
        self.threadController = tc.ThreadController()#线程池
        self.widgetController = wc.WidgetController()#控件池

        self.selectRoleKey = None #当前选择角色
        self.nowPage = "roleList" #当前页面

        self.mainWindow = tk.Tk()  # 主窗口
        self.mainWindow.geometry(self.getGeometry())
        self.mainWindow.title(self.config.getTitle())#标题
        self.cacheWidget(self.mainWindow, None, "BaseWindow", None)  # 缓存主窗

#######################具体布局################################

    def initRoleListFrame(self):
        """初始化角色列表界面"""
        mainWindow = self.getWidget("BaseWindow")
        contentFrame = tk.Frame(mainWindow, cnf=self.widgetCnf())#基础内容页
        skinPathFrame = tk.Frame(contentFrame,cnf=self.widgetCnf()) #皮肤路径
        skinPathLabel = tk.Label(skinPathFrame,text="皮肤路径",width=10,cnf=self.textCnf())
        skinSourceLabel = tk.Label(skinPathFrame,text=self.config.getSkinPath(),cnf=self.textCnf()) #显示皮肤路径
        skinPathUpateBtn = tk.Button(skinPathFrame,text="更新",cnf=self.textCnf())#更新
        modPathFrame = tk.Frame(contentFrame,cnf=self.widgetCnf()) #Mods路径
        modPathLabel = tk.Label(modPathFrame,text="Mods路径",width=10,cnf=self.textCnf())
        modSourceLabel = tk.Label(modPathFrame,text=self.config.getModsPath(),cnf=self.textCnf())#显示Mods路径
        modPathUpdateBtn = tk.Button(modPathFrame,text="更新",cnf=self.textCnf())#更新
        contentPageCanvas = tk.Canvas(contentFrame,cnf=self.widgetCnf())#内容页框架
        contentPageScroll = tk.Scrollbar(contentFrame,cnf=self.scrollCnf())#滚动条

        skinSourceLabel.bind(Event.MouseLefClick,self.clickSelectSkinPath)#选择皮肤路径
        skinPathUpateBtn.bind(Event.MouseLefClick,utils.eventAdaptor(self.clickUpdateConfig,btn=skinPathUpateBtn))#更新
        modSourceLabel.bind(Event.MouseLefClick,self.clickSelectModsPath)#选择mods路径
        modPathUpdateBtn.bind(Event.MouseLefClick,utils.eventAdaptor(self.clickUpdateConfig,btn=modPathUpdateBtn))#更新

        contentPageCanvas.config(yscrollcommand=contentPageScroll.set,yscrollincrement=1)
        contentPageScroll.config(command=contentPageCanvas.yview) #绑定滚动

        self.cacheWidget(contentFrame,"BaseWindow","contentFrame",self.packCnf(tk.BOTH, tk.TOP, tk.NW, 1))
        self.cacheWidget(skinPathFrame,"contentFrame","skinPathFrame",self.packCnf(tk.X,tk.TOP,tk.NW))
        self.cacheWidget(skinPathLabel,"skinPathFrame","skinPathLabel",self.packCnf(tk.NONE,tk.LEFT,tk.CENTER))
        self.cacheWidget(skinSourceLabel,"skinPathFrame","skinSourceLabel",self.packCnf(tk.BOTH,tk.LEFT,tk.CENTER,1))
        self.cacheWidget(skinPathUpateBtn,"skinPathFrame","skinPathUpdateBtn",self.packCnf(tk.NONE,tk.RIGHT,tk.CENTER))
        self.cacheWidget(modPathFrame,"contentFrame","modPathFrame",self.packCnf(tk.X,tk.TOP,tk.NW))
        self.cacheWidget(modPathLabel,"modPathFrame","modPathLabel",self.packCnf(tk.NONE,tk.LEFT,tk.CENTER))
        self.cacheWidget(modSourceLabel,"modPathFrame","modSourceLabel",self.packCnf(tk.BOTH,tk.LEFT,tk.CENTER,1))
        self.cacheWidget(modPathUpdateBtn,"modPathFrame","modPathUdateBtn",self.packCnf(tk.NONE,tk.RIGHT,tk.CENTER))
        self.cacheWidget(contentPageCanvas,"contentFrame","contentPageCanvas",self.packCnf(tk.BOTH,tk.LEFT,tk.NW,1))
        self.cacheWidget(contentPageScroll,"contentFrame","contentPageScroll",self.packCnf(tk.Y,tk.RIGHT,tk.E))

    def loadRoleListContent(self):
        """加载角色列表内容"""
        self.clearContentPage()
        skinPath = self.getSkinPath()
        if not utils.isPathExist(skinPath):
            return
        contentFrame = self.getWidget("contentFrame")
        contentPageCanvas = self.getWidget("contentPageCanvas") #内容画布
        contentPageFrame = self.getWidget("contentPageFrame") #内容主框架
        roleIndex = 0
        rolePageWidth = contentFrame.winfo_width() #当前内容页宽度
        columnMax = self.config.getRoleColoumnMax(rolePageWidth) #一行最多显示角色数
        border = self.config.getRoleBtnBorder(rolePageWidth,columnMax) #角色图标合适边距
        for fileDir in os.listdir(skinPath):
            filePath = os.path.join(skinPath,fileDir)
            rowIndex = (roleIndex // columnMax) + 1 #计算grid布局的行列
            columnIndex = (roleIndex % columnMax) + 1
            if utils.isPathExist(filePath) and self.config.existRole(fileDir):
                image = self.getRoleImage(fileDir,skinPath)

                roleSingleFrame = tk.Frame(contentPageFrame,borderwidth=border,cnf=self.widgetCnf()) #单个角色框架
                roleSingleBtn = tk.Button(roleSingleFrame,image=image,cnf=self.widgetCnf()) #角色图片
                roleSingleLabel = tk.Label(roleSingleFrame,text=self.config.getRoleText(fileDir),cnf=self.textCnf()) #角色名称

                roleSingleFrame.bind(Event.MouseWheel,utils.eventAdaptor(self.scrollVertical,widget=contentPageCanvas)) #绑定事件
                roleSingleBtn.bind(Event.MouseWheel,utils.eventAdaptor(self.scrollVertical,widget=contentPageCanvas))
                roleSingleBtn.bind(Event.MouseLefClick,utils.eventAdaptor(self.clickSelectRole,key=fileDir))
                roleSingleLabel.bind(Event.MouseWheel,utils.eventAdaptor(self.scrollVertical,widget=contentPageCanvas))

                self.cacheWidgetByGrid(roleSingleFrame,"contentPageFrame","roleSingleFrame_%d"%roleIndex,self.gridCnf(rowIndex,columnIndex))
                self.cacheWidget(roleSingleBtn,"roleSingleFrame_%d"%roleIndex,"roleSingleBtn_%d"%roleIndex,cnf=self.packCnf(tk.NONE,tk.TOP,tk.N))
                self.cacheWidget(roleSingleLabel,"roleSingleFrame_%d"%roleIndex,"roleSingleLabel_%d"%roleIndex,cnf=self.packCnf(tk.NONE,tk.TOP,tk.N))

                roleIndex+=1
        self.updateCanvas(contentPageCanvas,contentPageFrame,"contentFrame")

    def loadSkinListPage(self,key:str):
        """加载皮肤列表内容"""
        rolePath = os.path.join(self.getSkinPath(),key) #检查皮肤路径
        if not utils.isPathExist(rolePath):
            return
        self.clearContentPage() #清理缓存
        contentFrame = self.getWidget("contentFrame") #基础内容页
        contentPageCanvas = self.getWidget("contentPageCanvas") #内容画布
        contentPageFrame = self.getWidget("contentPageFrame") #内容主框架

        skinControlFrame = tk.Frame(contentFrame,cnf=self.widgetCnf()) #皮肤操作面板

        self.cacheWidget(skinControlFrame,"contentFrame","skinControlFrame",cnf=self.packCnf(tk.Y,tk.LEFT,tk.NW)) #缓存
        self.widgetController.repackWidget(["skinControlFrame","contentPageCanvas","contentPageScroll"]) #重新布局

        self.loadSkinControlPanel(key) #更新控制面板
        self.loadSkinListContent(key) #加载皮肤列表页面
        self.updateCanvas(contentPageCanvas,contentPageFrame,"contentFrame") #更新

    def loadSkinListContent(self,key:str):
        """加载皮肤列表页面"""
        rolePath = os.path.join(self.getSkinPath(),key)

        contentPageFrame = self.getWidget("contentPageFrame")
        skinIndex = 0
        for fileDir in os.listdir(rolePath):
            filePath = os.path.join(rolePath,fileDir)
            if utils.isPathExist(filePath):
                for image in self.getSkinImages(filePath):
                    rowIndex = (skinIndex // 5) + 1 #计算grid布局的行列
                    columnIndex = (skinIndex % 5) + 1

                    skinSingleFrame = tk.Frame(contentPageFrame,cnf=self.widgetCnf()) #单个皮肤
                    skinSingleBtn = tk.Button(skinSingleFrame,image=image,cnf=self.widgetCnf()) #皮肤按钮
                    skinSingleText = tk.Label(skinSingleFrame,text=fileDir,cnf=self.textCnf()) #皮肤文本

                    skinSingleBtn.bind(Event.MouseLefClick,utils.eventAdaptor(self.clickSelectSkin,skinPath=fileDir)) #绑定事件

                    self.cacheWidgetByGrid(skinSingleFrame,"contentPageFrame","skinSingleFrame_%d"%skinIndex,cnf=self.gridCnf(rowIndex,columnIndex))
                    self.cacheWidget(skinSingleBtn,"skinSingleFrame_%d"%skinIndex,"skinSingleBtn_%d"%skinIndex,cnf=self.packCnf(tk.NONE,tk.TOP,tk.N))
                    self.cacheWidget(skinSingleText,"skinSingleFrame_%d"%skinIndex,"skinSingleText_%d"%skinIndex,cnf=self.packCnf(tk.X,tk.TOP,tk.CENTER))
                    self.sourceController.cacheImage(image,"default","skinList")
                    skinIndex+=1

    def loadSkinControlPanel(self,key:str):
        """加载皮肤操作面板"""
        rolePath = os.path.join(self.getSkinPath(),key)

        skinControlFrame = self.getWidget("skinControlFrame")
        controlDisplayFrame = tk.Frame(skinControlFrame,cnf=self.widgetCnf())
        roleImage = self.getRoleImage(key,self.getSkinPath())
        controlDisplayLabel = tk.Label(controlDisplayFrame,width=self.config.getControlPanelWidth(),image=roleImage,cnf=self.widgetCnf()) #角色图标
        controlDisplayText = tk.Label(controlDisplayFrame,text=self.config.getRoleText(key),cnf=self.textCnf()) #角色名称
        controlSelectFrame = tk.Frame(skinControlFrame,cnf=self.widgetCnf()) #选择的皮肤操作
        controlSelectLabel = tk.Label(controlSelectFrame,text="当前选择:",cnf=self.textCnf())
        controlSelectText = tk.Label(controlSelectFrame,text="",cnf=self.textCnf())
        controlReplaceBtn = tk.Button(controlSelectFrame,text="替换",cnf=self.textCnf())
        controlCatchBtn = tk.Button(controlSelectFrame,text="截图制作预览",cnf=self.textCnf())
        controlNowFrame = tk.Frame(skinControlFrame,cnf=self.widgetCnf()) #当前使用的皮肤操作
        controlNowLabel = tk.Label(controlNowFrame,text="当前使用:",cnf=self.textCnf())
        controlNowText = tk.Label(controlNowFrame,text="",cnf=self.textCnf())
        controlNowDelete = tk.Button(controlNowFrame,text="删除",cnf=self.textCnf())

        controlReplaceBtn.bind(Event.MouseLefClick,self.clickReplaceSkin) #绑定事件

        self.cacheWidget(controlDisplayFrame,"skinControlFrame","controlDisplayFrame",cnf=self.packCnf(tk.X,tk.TOP,tk.N))
        self.cacheWidget(controlDisplayLabel,"controlDisplayFrame","controlDisplayLabel",cnf=self.packCnf(tk.NONE,tk.TOP,tk.N))
        self.cacheWidget(controlDisplayText,"controlDisplayFrame","controlDisplayText",cnf=self.packCnf(tk.X,tk.TOP,tk.CENTER))
        self.cacheWidget(controlSelectFrame,"skinControlFrame","controlSelectFrame",cnf=self.packCnf(tk.X,tk.TOP,tk.NW))
        self.cacheWidget(controlSelectLabel,"controlSelectFrame","controlSelectLabel",cnf=self.packCnf(tk.NONE,tk.TOP,tk.W))
        self.cacheWidget(controlSelectText,"controlSelectFrame","controlSelectText",cnf=self.packCnf(tk.X,tk.TOP,tk.W))
        self.cacheWidget(controlReplaceBtn,"controlSelectFrame","controlReplaceBtn",cnf=self.packCnf(tk.X,tk.TOP,tk.W))
        self.cacheWidget(controlCatchBtn,"controlSelectFrame","controlCatchBtn",cnf=self.packCnf(tk.X,tk.TOP,tk.W))
        self.cacheWidget(controlNowFrame,"skinControlFrame","controlNowFrame",cnf=self.packCnf(tk.X,tk.TOP,tk.NW))
        self.cacheWidget(controlNowLabel,"controlNowFrame","controlNowLabel",cnf=self.packCnf(tk.NONE,tk.TOP,tk.W))
        self.cacheWidget(controlNowText,"controlNowFrame","controlNowText",cnf=self.packCnf(tk.X,tk.TOP,tk.W))
        self.cacheWidget(controlNowDelete,"controlNowFrame","controlNowDelete",cnf=self.packCnf(tk.X,tk.TOP,tk.W))

    def updateCanvas(self,canvas:tk.Canvas,frame:tk.Frame,parentKey:str):
        """更新滚动画布控件"""
        self.getWidget(parentKey).update()
        canvas.config(
            scrollregion=frame.bbox(tk.ALL),
            width=frame.winfo_width(),
            height=frame.winfo_height(),
        )

#######################清理缓存################################
    def clearContentPage(self):
        """清空内容页及其内容相关缓存"""
        self.sourceController.clearImage("skinList") #清理皮肤缓存

        self.widgetController.destroyWidget("skinControlFrame")
        self.widgetController.clearWidget("contentPageCanvas")
        contentPageCanvas = self.getWidget("contentPageCanvas") #内容画布
        contentPageFrame = tk.Frame(contentPageCanvas,cnf=self.widgetCnf())#重建框架

        contentPageCanvas.delete(tk.ALL)#清除内容
        contentPageCanvas.create_window(0, 0, window=contentPageFrame, anchor=tk.NW) #显示框架
        contentPageFrame.bind(Event.MouseWheel,utils.eventAdaptor(self.scrollVertical,widget=contentPageCanvas))#绑定事件

        self.cacheWidget(contentPageFrame,"contentPageCanvas","contentPageFrame",None) #缓存
        self.widgetController.repackWidget(["contentPageCanvas","contentPageScroll"]) #重新布局

#######################控件事件################################
    def clickUpdateConfig(self,event,btn: tk.Button):
        """点击更新Config并写入本地"""
        self.config.writeToFile()
        btn.config(text="更新成功", fg=self.config.getColorSuccess())
        self.cacheThread(threading.Thread(target=self.replaceText,args=(btn, "更新"),daemon=True),"button")

    def clickSelectModsPath(self,event):
        """选择Mods路径"""
        filePath = askdirectory()
        modSourceLabel = self.getWidget("modSourceLabel")
        if not utils.isEmpty(filePath) and utils.isWidget(modSourceLabel, tk.Label):
            modSourceLabel.config(text=filePath)
            self.config.setModsPath(filePath)
            if self.isSkinListPage():
                #更新皮肤列表页面，只影响到皮肤控件面板
                self.cacheThread(threading.Thread(target=self.loadSkinListPage,args=(self.selectRoleKey,),daemon=True),"content")

    def clickSelectSkinPath(self, event):
        """选择皮肤库路径"""
        filePath = askdirectory()
        skinSourceLabel = self.getWidget("skinSourceLabel")
        if not utils.isEmpty(filePath) and utils.isWidget(skinSourceLabel, tk.Label):
            skinSourceLabel.config(text=filePath)
            self.config.setSkinPath(filePath)
            if self.isRoleListPage():
                #更新角色列表页面
                self.cacheThread(threading.Thread(target=self.loadRoleListContent,daemon=True),"content")
            elif self.isSkinListPage():
                #更新皮肤列表页面
                self.cacheThread(threading.Thread(target=self.loadSkinListPage,args=(self.selectRoleKey,),daemon=True),"content")

    def clickSelectSkin(self,event,skinPath:str):
        """点击选择皮肤"""
        controlSelectText = self.getWidget("controlSelectText")
        controlSelectText.config(text=skinPath)

    def clickReplaceSkin(self,event):
        """点击替换皮肤"""
        controlReplaceBtn = self.getWidget("controlReplaceBtn")
        controlSelectText = self.getWidget("controlSelectText")
        if not utils.isWidget(controlReplaceBtn, tk.Button) or not utils.isWidget(
            controlSelectText, tk.Label
        ):
            return
        if controlReplaceBtn != None and controlReplaceBtn["text"] == "替换":
            pathName = controlSelectText["text"]
            if utils.isEmpty(pathName):
                controlReplaceBtn.config(text="替换(未选择皮肤)", fg=self.config.getColorFail())
                self.cacheThread(threading.Thread(target=self.replaceText, args=(controlReplaceBtn, "替换"), daemon=True),"button")
                return
            modsPath = self.config.getModsPath()
            if utils.isEmpty(modsPath) or modsPath == "请选择3dmigoto Mods文件夹":
                controlReplaceBtn.config(text="替换(未选择Mods文件夹)", fg=self.config.getColorFail())
                self.cacheThread(threading.Thread(
                    target=self.replaceText, args=(controlReplaceBtn, "替换"), daemon=True
                ),"button")
                return
            if not os.path.exists(modsPath):
                controlReplaceBtn.config(text="替换(Mods文件夹不存在)", fg=self.config.getColorFail())
                self.cacheThread(threading.Thread(
                    target=self.replaceText, args=(controlReplaceBtn, "替换"), daemon=True
                ),"button")
                return
            controlReplaceBtn.config(text="替换中......")
            self.cacheThread(threading.Thread(
                target=self.replaceSkin, args=(modsPath, pathName), daemon=False
            ),"button")

    def clickSelectRole(self,event,key:str):
        """点击角色"""
        self.selectRoleKey = key #设置当前角色
        self.nowPage = "skinList" #进入皮肤列表页面
        self.cacheThread(threading.Thread(target=self.loadSkinListPage,args=(key,),daemon=True),"content")

    def scrollVertical(self, event, widget: tk.Widget):
        """画布上下滚动事件"""
        widget.yview_scroll(-1 * (event.delta // 5), tk.UNITS)

    def replaceText(self, btn: tk.Button, text: str):
        """替换按钮文本"""
        sleep(2)
        btn.config(text=text, fg=self.config.getColorDefault())

    def replaceSkin(self, modsPath: str, pathName: str) -> bool:
        """替换皮肤"""
        modRolePath = os.path.join(modsPath, self.selectRoleKey)  # mods角色路径
        if os.path.exists(modRolePath):
            shutil.rmtree(modRolePath)  # 清空当前角色正当使用的mod
        modFileDir = os.path.join(modRolePath, pathName)  # 创建目标文件夹
        rolePath = os.path.join(self.config.getSkinPath(), self.selectRoleKey)
        skinPath = os.path.join(rolePath, pathName)
        replaceBtn = self.getWidget("controlReplaceBtn")
        if utils.isWidget(replaceBtn, tk.Button) and os.path.exists(skinPath):
            shutil.copytree(skinPath, modFileDir)
            replaceBtn.config(text="替换成功！！", fg=self.config.getColorSuccess())
            self.cacheThread(threading.Thread(target=self.replaceText, args=(replaceBtn, "替换"), daemon=True),"button")
            modUseRoleText = self.getWidgetFromPool("modsUseText")  # mods正在使用角色
            if utils.isWidget(modUseRoleText, tk.Label):
                modUseRoleText.config(text=self.getModsUseSkinText(self.selectRoleKey))
        else:
            replaceBtn.config(text="替换失败(未知原因)", fg=self.config.getColorFail())
            self.cacheThread(threading.Thread(target=self.replaceText, args=(replaceBtn, "替换"), daemon=True),"button")

#######################基础方法################################

    def isSkinListPage(self)->bool:
        """当前页面是否是皮肤选择界面"""
        return self.nowPage=="skinList"

    def isRoleListPage(self)->bool:
        """当前页面是否停留在角色选择页面"""
        return self.nowPage=="roleList"

    def cacheThread(self,thread:threading.Thread,key:str):
        """缓存线程"""
        self.threadController.cacheThread(thread,key)

    def cacheWidget(
        self, widget: tk.Widget, parentKey: str, key: str, cnf: dict
    ) -> None:
        """缓存控件"""
        self.widgetController.cacheWidget(widget, parentKey, key, cnf)

    def cacheWidgetByGrid(self, widget: tk.Widget, parentKey: str, key: str, cnf: dict):
        """缓存控件，grid布局"""
        self.widgetController.cacheWidgetByGrid(widget, parentKey, key, cnf)

    def getWidget(self, key: str) -> tk.Widget:
        """获取控件"""
        return self.widgetController.getWidget(key)

    def packCnf(self, fill: str, side: str, anchor: str, expand: int = 0) -> dict:
        """布局配置"""
        return {"fill": fill, "side": side, "anchor": anchor, "expand": expand}

    def widgetCnf(self) -> dict:
        """基础控件属性"""
        return {"background": self.config.getBackGround()}

    def textCnf(self)->dict:
        """带字体的基础控件属性"""
        return {"background": self.config.getBackGround(),"font":self.config.getFont()}

    def scrollCnf(self)->dict:
        """滚动条基础属性"""
        return {"background": self.config.getBackGround(),"orient":tk.VERTICAL,"width":1}

    def gridCnf(self,row:int,column:int)->dict:
        """grid布局基础属性"""
        return {"row":row,"column":column}

    def getGeometry(self)->str:
        """获取窗口尺寸"""
        return "%dx%d"%(self.config.getWindowWidth(),self.config.getWindowHeight())

    def getSkinPath(self)->str:
        """获取皮肤路径"""
        return self.config.getSkinPath()

    def getSkinImages(self,path:str)->list[tk.PhotoImage]:
        """获得皮肤图片"""
        images = []
        for fileName in os.listdir(path):
            filePath = os.path.join(path,fileName)
            if utils.isPhoto(filePath):
                image = Image.open(filePath).resize(self.config.getRoleIconSize())
                image = ImageTk.PhotoImage(image)
                images.append(image)
        if len(images)==0:
            images.append(self.getDefaultSkinImage())
        return images

    def getDefaultSkinImage(self):
        """获取默认的皮肤图片"""
        filePath = os.path.join(os.getcwd(), self.config.getDefaultSkin())
        image = Image.open(filePath).resize(self.config.getRoleSkinSize())
        return ImageTk.PhotoImage(image)

    def getRoleImage(self, key: str, path: str) -> tk.PhotoImage:
        """获取该文件夹下的第一张图片作为角色图片"""
        if self.sourceController.isInImagePool(key,"roleList"):
            return self.sourceController.getImage(key,"roleList")
        skinPath = os.path.join(path,key)
        for fileName in os.listdir(skinPath):
            filePath = os.path.join(skinPath, fileName)
            if os.path.isfile(filePath) and utils.isPhoto(filePath):
                image = Image.open(filePath).resize(self.config.getRoleIconSize())
                image = ImageTk.PhotoImage(image)
                self.sourceController.cacheImage(image,key,"roleList")
                return image
        return self.getDefaultRoleImage()

    def getDefaultRoleImage(self) -> tk.PhotoImage:
        """获取默认的角色图片"""
        roleKey = self.config.getDefaultRoleKey()
        if not self.sourceController.isInImagePool(roleKey,"roleList"):
            path = os.path.join(os.getcwd(), self.config.getDefaultRoleIcon())
            image = Image.open(path).resize(self.config.getRoleIconSize())
            image = ImageTk.PhotoImage(image)
            self.sourceController.cacheImage(image,roleKey,"roleList")
        return self.sourceController.getImage(roleKey,"roleList")

if __name__ == "__main__":
    MainFrame()
