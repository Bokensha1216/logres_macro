import pyautogui

from setup import *
import imgrecg
import macros

if __name__ == "__main__":
    findWindow()
    # image = "images/navi.png"
    # items = imgrecg.locateAll(image, confidence=0.995)
    # imgrecg.drawLocatedItems(items)

    enemylist = macros.locateEnemy(limitRange=True, locateRange=150)
    while len(enemylist) == 0:
        time.sleep(0.5)
        enemylist = macros.locateEnemy(limitRange=True, locateRange=150)
    # print(enemylist)
    macros.goToNearestEnemy(enemylist)

    battleStarted = macros.battleStarted()
    while not battleStarted:
        time.sleep(1)
        battleStarted = macros.battleStarted()

    print("start")