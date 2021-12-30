import time
import threading
from enum import Flag, auto

import numpy as np

from coordinate import *
from exception import *
import macros
from imageProcessing import *
from wrapping import *


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
                            if keika > 30:
                                appWindow.eventQueue.put(CannotFindException())
                                break

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
                                break

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
                                    break
                                else:
                                    appWindow.eventQueue.put(BattleNotFinish())
                                    break

                if event == Macro.CHECK_QUEST_CLEAR:
                    print(event.name)
                    loopCount += 1
                    if loopCount >= 30:
                        appWindow.eventQueue.put(QuestNotFinish())

                if event == Macro.LOCATE_ENEMY:
                    print(event.name)

                    if macros.questCleared():
                        appWindow.eventQueue.put(TransitionError("クエストクリアしています"))

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
                                if macros.isInBattle():
                                    appWindow.eventQueue.put(SceneError("戦闘中です"))
                                    break
                                else:
                                    appWindow.eventQueue.put(CannotFindException())
                                    break

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
                            if keika > 30:
                                if macros.isInField():
                                    if macros.isInHome():
                                        appWindow.eventQueue.put(SceneError("城下町に戻っています"))
                                        break
                                    else:
                                        appWindow.eventQueue.put(NextAlreadyStarted())
                                        break
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


# class ClickChecker(threading.Thread):
#     def __init__(self, clickPos, range=(50, 50)):
#         super().__init__()
#         self.clickPos = clickPos
#         self.range = range
#
#     def run(self):
#         x1 = int(self.clickPos[0] - self.range[0] / 2)
#         y1 = int(self.clickPos[1] - self.range[1] / 2)
#         region = (x1, y1, self.range[0], self.range[1])
#         img1 = macros.screenshot(region).convert("L")
#         time.sleep(0.1)
#         img2 = macros.screenshot(region).convert("L")
#
#         img1 = pil2cv(img1)
#         img2 = pil2cv(img2)
#         im_diff = np.abs(img1.astype(int) - img2.astype(int))
#         if im_diff.max() < 100:
#             print(im_diff.max())
#             click(self.clickPos[0], self.clickPos[1])
