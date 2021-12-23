import threading

from setup import *
import macros


def syukaiQuest(questTimes):
    def syukaiQuestThread():

        findWindow()
        # image = "images/navi.png"
        # items = imgrecg.locateAll(image, confidence=0.65)
        # imgrecg.drawLocatedItems(items)

        for questTime in range(questTimes):
            # クエスト開始
            print("startQuest")
            navi = macros.locateQuestNavi()
            while navi is None:
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
                enemylist = macros.locateEnemy(limitRange=True, locateRange=150, locateCenter=Screen.center)
                while len(enemylist) == 0:
                    time.sleep(0.5)
                    enemylist = macros.locateEnemy(limitRange=True, locateRange=150, locateCenter=Screen.center)

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

