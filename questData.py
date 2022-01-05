from enum import Flag, auto


class Stage(Flag):
    DAY = auto()
    NIGHT = auto()


class QuestData:
    dayOrNight = Stage.DAY
