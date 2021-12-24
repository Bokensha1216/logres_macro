import threading

from setup import *
import macros
from coordinate import *
import wrapping


def syukaiQuest(questTimes):
    def syukaiQuestThread():

        findWindow()
        # image = "resizedImages/navi.png"
        # items = wrapping.locateAllOnScreen(image, region=appWindow.region, confidence=0.65)
        # imgrecg.drawLocatedItems(items)

        for questTime in range(questTimes):
            # クエスト開始
            print("startQuest")
            navi = macros.locateQuestNavi()
            while navi is None:
                print("navi not Found")
                time.sleep(1)
                navi = macros.locateQuestNavi()

            time.sleep(1.5)
            print("locateEnemy")
            enemylist = macros.locateEnemy(limitRange=True, locateRange=150, locateCenter=(navi))
            while len(enemylist) == 0:
                print("a")
                time.sleep(0.5)
                enemylist = macros.locateEnemy(limitRange=True, locateRange=150, locateCenter=(navi))
            # print(enemylist)

            # クエストクリアまで
            while True:
                print("traceEnemy")
                macros.traceEnemy(enemylist)

                time.sleep(1)

                macros.startBattle()
                time.sleep(12)
                while macros.isInBattle():
                    # print(macros.isInBattle())
                    time.sleep(1)

                # 戦闘終了
                print("waitfield")
                macros.waitField()
                time.sleep(1.5)
                if macros.questCleared():
                    break

                time.sleep(1.5)
                if macros.questCleared():
                    break
                enemylist = macros.locateEnemy(limitRange=True, locateRange=150, locateCenter=appWindow.center)
                while len(enemylist) == 0:
                    print("notFoundEnemy")
                    time.sleep(0.5)
                    enemylist = macros.locateEnemy(limitRange=True, locateRange=150, locateCenter=appWindow.center)
                if macros.questCleared():
                    break

            time.sleep(0.5)
            print("questclear")
            macros.goToNextQuest()
            time.sleep(4)
            macros.waitField()
            print("next")
            time.sleep(4)

    print("makeMainThread")
    mainThread = threading.Thread(target=syukaiQuestThread)
    mainThread.start()
    return mainThread

