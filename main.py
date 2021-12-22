import pyautogui

from setup import *
import imgrecg
import macros

if __name__ == "__main__":
    findWindow()
    # image = "images/navi.png"
    # items = imgrecg.locateAll(image, confidence=0.995)
    # imgrecg.drawLocatedItems(items)

    # enemylist = macros.locateEnemy(limitRange=True, locateRange=150, locateCenter=(macros.locateQuestNavi()))
    # while len(enemylist) == 0:
    #     time.sleep(0.5)
    #     enemylist = macros.locateEnemy(limitRange=True, locateRange=150)
    # # print(enemylist)
    # macros.goToNearestEnemy(enemylist)
    #
    # battleStarted = macros.isInBattle()
    # while not battleStarted:
    #     time.sleep(1)
    #     battleStarted = macros.isInBattle()
    #
    # time.sleep(1)

    # macros.startBattle()
    # time.sleep(1)
    while macros.isInBattle():
        print(macros.isInBattle())
        time.sleep(1)

    print("waitfield")
    macros.waitField()
    time.sleep(3)
    enemylist = macros.locateEnemy(limitRange=True, locateRange=150, locateCenter=Screen.center)
    while len(enemylist) == 0:
        time.sleep(0.5)
        enemylist = macros.locateEnemy(limitRange=True, locateRange=150)
    macros.goToNearestEnemy(enemylist)

