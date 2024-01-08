class FrameConfig:
    font = ("微软雅黑", 12)  # 默认字体
    colorSuccess = "cyan" #操作成功的字体颜色
    colorFail = "red" #操作失败的字体颜色
    colorDefault = "black" #默认字体颜色

    dataFile = "data.json"  # 默认数据储存位置
    tempDir = "temp" #临时储存位置
    frameTitle = "Genshin Skin Manager @Skily_Leyu"  # 窗体标题

    roleIconSize = (120, 160)  # 角色图标尺寸
    roleSkinSize = (245, 490)  # 默认角色皮肤尺寸
    skinControlWidth = 220  # 皮肤操作界面宽度

    defaultRole = "src/default_role.jpeg"  # 默认角色图片路径
    defaultSkin = "src/default_skin.png" #默认皮肤图片路径
    defaultRoleKey = "defalut"  # 默认角色Key


class FrameKey:
    mainKeys = ["sideBar", "content"]  # 第一层:侧边栏+内容页
    sideBarKeys = [
        "sideBarScroll",
        "sideBarCanvas",
        "sideBarFrame",
        "sideBarBtn",
    ]  # 侧边栏
    contentKeys = ["skinManager"]
    skinManagerKeys = ["skinTitle", "skinControl", "skinControlCanvas", "roleList"]
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
        "skinSelectText",
        "skinDisplayReplace"
        "skinDisplayDelete",
        "modsUseText",
        "catchScreen"
    ]
    roleListKeys = ["roleListCanvas", "roleListScroll", "roleListContent", "singleRole"]
    skinListKeys = ["skinList"]

class Event:
    # 键盘事件
    F4 = "<Key-F4>"
    Escape = "<Escape>"
    Tab = "<Tab>"

    # 鼠标事件
    MouseWheel = "<MouseWheel>"  # 滚轮滚动
    MouseLefClick = "<Button-1>"  # 鼠标左键
