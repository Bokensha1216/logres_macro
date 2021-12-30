import threading

from setup import *
import macros
from coordinate import *
import wrapping
from exception import *
from observer import *


def syukaiQuest(questTimes, useQuestNavi=False):
    def syukaiQuestThread():
        findWindow()

        try:
            questLoop(questTimes, useQuestNavi)
        except FinishButtonException as e:
            print(e)
            print("スレッドを終了")
        except Exception as e:
            print(e)
            sendMessage(FinishButtonException())
            print("スレッドを終了")

    print("makeMainThread")
    mainThread = threading.Thread(target=syukaiQuestThread)
    mainThread.start()
    return mainThread


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
        sendMessage(Macro.FIRST_LOCATE_ENEMY)

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
    except CannotFindException as e:
        raise e


def traceEnemy(enemyList):
    try:
        if enemyList is None:
            raise SkipException
        # 敵追跡
        print("traceEnemy")
        sendMessage(Macro.TRACE_ENEMY)
        macros.traceEnemy(enemyList)

        macros.wait(1)
    except SkipException:
        return

    except CannotFindException as e:
        print(e, end="")
        print(" : 範囲を広げます")
        enemyList = locateEnemy(limitRange=False)
        traceEnemy(enemyList)


def battle():
    try:
        print("battle")
        sendMessage(Macro.BATTLE)
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
    except BattleNotFinish as e:
        print(e, end="")
        print(" : 逃げます")
        macros.run()
        macros.wait(3)
    except NotInBattle:
        print("a")
        return


def checkQuestClear():
    try:
        print("checkQuestClear")
        sendMessage(Macro.CHECK_QUEST_CLEAR)
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


def locateEnemy(limitRange=True):
    try:
        print("LocateEnemy")
        sendMessage(Macro.LOCATE_ENEMY)
        # 敵検出
        enemyList = macros.locateEnemy(limitRange, locateRange=150, locateCenter=appWindow.center)
        while len(enemyList) == 0:
            print("notFoundEnemy")
            macros.wait(0.5)
            enemyList = macros.locateEnemy(limitRange, locateRange=150, locateCenter=appWindow.center)

        return enemyList
    except SkipException:
        return None
    except CannotFindException as e:
        raise e
    except TransitionError as e:
        raise e
    except SceneError as e:
        return None


def nextQuest():
    try:
        print("nextQuest")
        sendMessage(Macro.NEXT_QUEST)
        macros.wait(0.5)
        macros.goToNextQuest()
        macros.wait(4)
        macros.waitField()
        macros.wait(4)
    except SkipException:
        return
    except NextQuestNotStart as e:
        if hasattr(e, "raiseExcept"):
            raise e
        else:
            nextQuest()
    except NextAlreadyStarted:
        return
    except SceneError as e:
        raise e


def sendMessage(msg):
    appWindow.observer.eventQueue.put(msg)
