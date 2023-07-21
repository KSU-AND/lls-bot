from enum import Enum, IntEnum, auto

class States(IntEnum):
    U_START = auto()
    U_ROLE = auto()
    S_NAME = auto()
    S_NICKNAME = auto()
    S_ROOM = auto()
    S_FULL = auto()
    A_CODE = auto()
    A_FULL = auto()
    S_FIX_NAME = auto()
    S_FIX_NICKNAME = auto()
    S_FIX_ROOM = auto()

class Answers(Enum):
    STUDENT = "Я участник"
    ADMIN = "Я организатор"
    NICKNAME = "Напомни мой псевдоним"
    FRIEND = "Кто мой друг по переписке?"
    TOTAL = "Узнать общее количество участников"
    DOC = "Скачать документ с данными"
    TOSS = "Провести жеребьевку"

class Roles(Enum):
    STUDENT = "student"
    ADMIN = "admin"