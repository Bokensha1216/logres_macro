import time
import threading
from enum import Flag, auto

from coordinate import *
from exception import *
import macros


class Observer(threading.Thread):
    def __init__(self):
        super().__init__()

        self.eventQueue = queue.Queue()
        self.macroList = []

    def run(self):
        try:
            self.observe()
        except FinishButtonException:
            print("finish observer")

    def observe(self):
        loopCount = 0
        nextQuestCount = 0
        while True:
            event = self.eventQueue.get()
            if isinstance(event, FinishButtonException):
                raise event
            else:
                if event == Macro.FIRST_LOCATE_ENEMY:
                    print(event.name)
                    loopCount = 0
                    nextQuestCount = 0
                    time_sta = time.time()
                    while True:
                        try:
                            self.checkEvent()
                        except HasEvent:
                            break
                        else:
                            time.sleep(1)
                            time_end = time.time()
                            keika = time_end - time_sta
                            if keika > 20:
                                appWindow.eventQueue.put(CannotFindException())

                if event == Macro.TRACE_ENEMY:
                    print(event.name)
                    time_sta = time.time()
                    while True:
                        try:
                            self.checkEvent()
                        except HasEvent:
                            break
                        else:
                            time.sleep(1)
                            time_end = time.time()
                            keika = time_end - time_sta
                            if keika > 20:
                                appWindow.eventQueue.put(CannotFindException())

                if event == Macro.BATTLE:
                    print(event.name)
                    time_sta = time.time()
                    while True:
                        try:
                            self.checkEvent()
                        except HasEvent:
                            break
                        else:
                            time.sleep(1)
                            time_end = time.time()
                            keika = time_end - time_sta
                            if keika > 100:
                                if not macros.isInBattle():
                                    appWindow.eventQueue.put(NotInBattle())
                                else:
                                    appWindow.eventQueue.put(BattleNotFinish())

                if event == Macro.CHECK_QUEST_CLEAR:
                    print(event.name)
                    loopCount += 1
                    if loopCount >= 30:
                        appWindow.eventQueue.put(QuestNotFinish())

                if event == Macro.LOCATE_ENEMY:
                    print(event.name)
                    time_sta = time.time()
                    while True:
                        try:
                            self.checkEvent()
                        except HasEvent:
                            break
                        else:
                            time.sleep(1)
                            time_end = time.time()
                            keika = time_end - time_sta
                            if keika > 40:
                                appWindow.eventQueue.put(CannotFindException())

                if event == Macro.NEXT_QUEST:
                    print(event.name)
                    time_sta = time.time()
                    while True:
                        try:
                            self.checkEvent()
                        except HasEvent:
                            break
                        else:
                            time.sleep(1)
                            time_end = time.time()
                            keika = time_end - time_sta
                            if keika > 40:
                                nextQuestCount += 1
                                if nextQuestCount <= 2:
                                    appWindow.eventQueue.put(NextQuestNotStart())
                                else:
                                    appWindow.eventQueue.put(NextQuestNotStart(raiseExcept=True))

    def checkEvent(self):
        if self.eventQueue.qsize() != 0:
            raise HasEvent


class Macro(Flag):
    FIRST_LOCATE_ENEMY = auto()
    TRACE_ENEMY = auto()
    BATTLE = auto()
    CHECK_QUEST_CLEAR = auto()
    LOCATE_ENEMY = auto()
    NEXT_QUEST = auto()
