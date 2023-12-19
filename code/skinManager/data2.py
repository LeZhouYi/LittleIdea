class RoleKey:
    roleKey = [
        "Amber",
        "Barbara",
        "Charlotte",
        "Collei",
        "Fischl",
        "Furina",
        "HuTao",
        "Kirara",
        "Lisa",
        "Lumine",
        "Lynette",
        "Noelle",
        "QiQi",
        "Sucrose",
        "XiangLing",
        "XingQiu",
        "YanFei",
    ]

    roleKeyText = {
        "Amber": "安柏",
        "Barbara": "芭芭拉",
        "Charlotte": "夏洛蒂",
        "Collei": "柯莱",
        "Fischl": "菲谢尔",
        "Furina": "芙宁娜",
        "HuTao": "胡桃",
        "Kirara": "绮良良",
        "Lisa": "丽莎",
        "Lumine": "荧",
        "Lynette": "琳妮特",
        "Noelle": "诺艾尔",
        "QiQi": "七七",
        "Sucrose": "砂糖",
        "XiangLing": "香菱",
        "XingQiu": "行秋",
        "YanFei": "烟绯",
    }

    def existRole(fileName: str) -> bool:
        """判断是否存在角色"""
        return fileName in RoleKey.roleKey

    def getRoleText(fileName: str) -> str:
        """返回当前角色对应角色名"""
        if fileName in RoleKey.roleKeyText:
            return RoleKey.roleKeyText[fileName]
        return "Empty"


class FrameConfig:
    font = ("微软雅黑", 12)  # 默认字体
    dataFile = "./data.json"  # 默认数据储存位置
    frameTitle = "Genshin Skin Manager @Skily_Leyu"  # 窗体标题
    roleIconSize = (120, 160)  # 角色图标尺寸
    roleSkinSize = (230, 450)  # 默认角色皮肤尺寸
    defaultRole = "src/default_role.jpeg"  # 默认角色图片路径
    defaultRoleKey = "defalut"  # 默认角色Key
    skinControlWidth = 220  # 皮肤操作界面宽度


class FrameKey:
    mainKeys = ["sideBar", "content"]  # 第一层:侧边栏+内容页
    sideBarKeys = [
        "sideBarScroll",
        "sideBarCanvas",
        "sideBarFrame",
        "sideBarBtn",
    ]  # 侧边栏
    contentKeys = ["skinManager"]
    skinManagerKeys = ["skinTitle", "skinControl", "roleList"]
    skinTitleKeys = [
        "skinTitleFrame",
        "skinTitleLabel",
        "skinSourceBtn",
        "skinSource",
        "modSource",
        "modSourceBtn",
    ]
    skinControlKeys = [
        "skinDisplay",
        "skinDisplayText",
        "skinDisplayFrame",
        "skinDisplayLabel",
        "skinSelectText" "skinDisplayBtn",
        "modsUseText",
    ]
    roleListKeys = ["roleListCanvas","roleListScroll","roleListContent","singleRole"]

    SideBar = "sideBar"  # 侧边栏
    SideBarParent = "sideBarParent"  # 侧边栏主框架，用于刷新滚动区域

    Page = "page"  # 内容页
    SkinTitle = "skinTitle"  # 皮肤管理页，标题栏
    SkinSourcePath = "skinSourcePath"  # 皮肤管理页，标题栏，皮肤库
    ModSourcePath = "modSourcePath"  # 皮肤管理页，标题栏，Mods文件夹
    SkinContent = "skinContent"  # 皮肤内容页，主框架
    SkinContentFrame = "skinContentFrame"  # 皮肤内容页，用于添加皮肤控件
    SkinControl = "skinControl"  # 皮肤操作页，主框架
    RoleDisplay = "roleDisplay"  # 已选角色展示图标
    RoleDisplayText = "roleDisplayText"  # 已选角色文本
    SkinSelectText = "skinSelectText"  # 已选皮肤文本
    SkinReplace = "skinReplace"  # 替换皮肤
    ModsUseSkin = "modsUseSkin"  # 正在使用的皮肤

    InfoCanvas = "canvas"  # 滚动画布关键字
    InfoScroll = "scroll"  # 滚动画布滚动方向关键字


class Event:
    # 键盘事件
    F4 = "<Key-F4>"
    Escape = "<Escape>"
    Tab = "<Tab>"

    # 鼠标事件
    MouseWheel = "<MouseWheel>"  # 滚轮滚动
    MouseLefClick = "<Button-1>"  # 鼠标左键
