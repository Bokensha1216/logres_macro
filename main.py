import pyautogui

from setup import *
import imgrecg
import macros

if __name__ == "__main__":
    findWindow()
    # image = "images/navi.png"
    # items = imgrecg.locateAll(image, confidence=0.995)
    # imgrecg.drawLocatedItems(items)

    # クエスト開始
    enemylist = macros.locateEnemy(limitRange=True, locateRange=150, locateCenter=(macros.locateQuestNavi()))
    while len(enemylist) == 0:
        time.sleep(0.5)
        enemylist = macros.locateEnemy(limitRange=True, locateRange=150, locateCenter=(macros.locateQuestNavi()))
    # print(enemylist)

    #繰り返し部分
    while True:
        macros.goToNearestEnemy(enemylist)

        battleStarted = macros.isInBattle()
        while not battleStarted:
            time.sleep(1)
            battleStarted = macros.isInBattle()

        time.sleep(1)

        macros.startBattle()
        time.sleep(12)
        while macros.isInBattle():
            # print(macros.isInBattle())
            time.sleep(1)

        print("waitfield")
        macros.waitField()
        time.sleep(1.5)
        if macros.questCleared():
            break

        time.sleep(3)
        if macros.questCleared():
            break
        enemylist = macros.locateEnemy(limitRange=True, locateRange=150, locateCenter=Screen.center)
        while len(enemylist) == 0:
            time.sleep(0.5)
            enemylist = macros.locateEnemy(limitRange=True, locateRange=150)

    print("questclear")

