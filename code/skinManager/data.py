ROLE_KEYS = ["KeQing", "Furina"]

FONT = ("软体雅黑", 16, "overstrike")

FILE = "./data.json"


def existRole(fileName: str) -> bool:
    return fileName in ROLE_KEYS
