import threading

from setup import *
import macros
from coordinate import *
import wrapping
from exception import *


def syukaiQuest(questTimes, useQuestNavi=False):
    def syukaiQuestThread():

        findWindow()
        # image = "resizedImages/navi.png"
        # items = wrapping.locateAllOnScreen(image, region=appWindow.region, confidence=0.65)
        # imgrecg.drawLocatedItems(items)

        try:
            questLoop(questTimes, useQuestNavi)
        except FinishButtonException as e:
            print(e)
            print("スレッドを終了")

    print("makeMainThread")
    mainThread = threading.Thread(target=syukaiQuestThread)
    mainThread.start()
    return mainThread


# def questLoop(questTimes, useQuestNavi):
#     for questTime in range(questTimes):
#         # クエスト開始
#         print("startQuest")
#
#         # クエストナビ検出
#         if useQuestNavi is True:
#             navi = findNavi()
#         else:
#             navi = None
#
#         # 初回敵検出
#         print("locateEnemy")
#         enemylist = macros.locateEnemy(limitRange=useQuestNavi, locateRange=150, locateCenter=navi)
#         while len(enemylist) == 0:
#             print("a")
#             macros.wait(0.5)
#             enemylist = macros.locateEnemy(limitRange=useQuestNavi, locateRange=150, locateCenter=navi)
#         # print(enemylist)
#
#         # クエストクリアまで
#         while True:
#             # 敵追跡
#             print("traceEnemy")
#             macros.traceEnemy(enemylist)
#
#             macros.wait(1)
#
#             # 戦闘開始
#             macros.startBattle()
#             macros.wait(12)
#             while macros.isInBattle():
#                 # print(macros.isInBattle())
#                 macros.wait(1)
#
#             # 戦闘終了
#             print("waitfield")
#             macros.waitField()
#             macros.wait(1.5)
#             if macros.questCleared():
#                 break
#
#             macros.wait(1.5)
#             if macros.questCleared():
#                 break
#             # 敵検出
#             enemylist = macros.locateEnemy(limitRange=True, locateRange=150, locateCenter=appWindow.center)
#             while len(enemylist) == 0:
#                 print("notFoundEnemy")
#                 macros.wait(0.5)
#                 enemylist = macros.locateEnemy(limitRange=True, locateRange=150, locateCenter=appWindow.center)
#             if macros.questCleared():
#                 break
#
#         # クエストクリア
#         macros.wait(0.5)
#         print("questclear")
#         macros.goToNextQuest()
#         macros.wait(4)
#         macros.waitField()
#         print("next")
#         macros.wait(4)

def questLoop(questTimes, useQuestNavi):
    for questTime in range(questTimes):
        enemyList = firstLocateEnemy(useQuestNavi)

        while True:
            traceEnemy(enemyList)

            battle()

            if checkQuestClear() is True:
                break

            enemyList = locateEnemy()

        nextQuest()


def firstLocateEnemy(useQuestNavi):
    try:
        print("firstLocateEnemy")

        def findNavi():
            navi = macros.locateQuestNavi()
            while navi is None:
                print("navi not Found")
                macros.wait(1)
                navi = macros.locateQuestNavi()
            macros.wait(1.5)
            return (navi)

        # クエストナビ検出
        if useQuestNavi is True:
            navi = findNavi()
        else:
            navi = None

        # 初回敵検出
        enemylist = macros.locateEnemy(limitRange=useQuestNavi, locateRange=150, locateCenter=navi)
        while len(enemylist) == 0:
            print("a")
            macros.wait(0.5)
            enemylist = macros.locateEnemy(limitRange=useQuestNavi, locateRange=150, locateCenter=navi)

        return enemylist
    except SkipException:
        return None


def traceEnemy(enemyList):
    try:
        if enemyList is None:
            raise SkipException
        # 敵追跡
        print("traceEnemy")
        macros.traceEnemy(enemyList)

        macros.wait(1)
    except SkipException:
        return


def battle():
    try:
        print("battle")
        # 戦闘開始
        macros.startBattle()
        macros.wait(12)
        while macros.isInBattle():
            # print(macros.isInBattle())
            macros.wait(1)

        # 戦闘終了
        # print("waitfield")
        macros.waitField()
        macros.wait(1.5)
    except SkipException:
        return


def checkQuestClear():
    try:
        print("checkQuestClear")
        if macros.questCleared():
            print("questclear")
            return True

        macros.wait(1.5)
        if macros.questCleared():
            print("questclear")
            return True
        return False
    except SkipException as e:
        if hasattr(e, "cleared"):
            return e.cleared
        else:
            return False


def locateEnemy():
    try:
        print("LocateEnemy")
        # 敵検出
        enemyList = macros.locateEnemy(limitRange=True, locateRange=150, locateCenter=appWindow.center)
        while len(enemyList) == 0:
            print("notFoundEnemy")
            macros.wait(0.5)
            enemyList = macros.locateEnemy(limitRange=True, locateRange=150, locateCenter=appWindow.center)

        return enemyList
    except SkipException:
        return None


def nextQuest():
    try:
        print("nextQuest")
        macros.wait(0.5)
        macros.goToNextQuest()
        macros.wait(4)
        macros.waitField()
        macros.wait(4)
    except SkipException:
        return
