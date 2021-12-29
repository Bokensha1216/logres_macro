import time
import threading
from enum import Flag, auto

from coordinate import *
from exception import *


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
        while True:
            loopCount = 0
            event = self.eventQueue.get()
            if isinstance(event, FinishButtonException):
                raise event
            else:
                if event == Macro.FIRST_LOCATE_ENEMY:
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
                            if keika > 90:
                                appWindow.eventQueue.put(BattleNotFinish())

                if event == Macro.CHECK_QUEST_CLEAR:
                    print(event.name)
                    loopCount += 1
                    if loopCount >= 30:
                        appWindow.eventQueue.put(QuestNotFinish())

                if event == Macro.LOCATE_ENEMY:
                    print(event.name)

                if event == Macro.NEXT_QUEST:
                    print(event.name)

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
