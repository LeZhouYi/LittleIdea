ROLE_KEYS =[
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

FONT = ("微软雅黑", 12)

FILE = "./data.json"

def existRole(fileName: str) -> bool:
    return fileName in ROLE_KEYS
