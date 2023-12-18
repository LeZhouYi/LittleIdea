
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
        "YanFei"
    ]

    def existRole(fileName: str) -> bool:
        return fileName in RoleKey.roleKey

class FrameConfig:
    font = ("微软雅黑", 12)
    dataFile = "./data.json"
    frameTitle = "Genshin Skin Manager @Skily_Leyu"

class FrameKey:
    SideBar = 'sideBar'
    SideBarParent = 'sideBarParent'

    Page = 'page'
    SkinTitle = 'skinTitle'
    SkinSourcePath = 'skinSourcePath'

    InfoCanvas = 'canvas'
    InfoScroll = 'scroll'

class Event:
    F4 = "<Key-F4>"
    Escape = "<Escape>"
    MouseWheel = "<MouseWheel>"
    Tab = "<Tab>"