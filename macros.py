import numpy as np
import pyautogui

import imgrecg
from setup import *


def locateQuestNavi():
    x, y, w, h = pyautogui.locateOnScreen("images/navi.png", region=Screen.regionWithoutStatus, confidence=0.995,
                                          grayscale=True)
    return x - 10, y + 50


def locateEnemy(limitRange=True, locateRange=100):
    enemies = imgrecg.locateAll("images/lv.png")

    enemyList = []
    for enemy in enemies:
        if limitRange:
            naviX, naviY = locateQuestNavi()
            region = (naviX - locateRange, naviY - locateRange, 2 * locateRange, 2 * locateRange)
            eX, eY = enemy[0], enemy[1]
            if isInRegion(eX, eY, region):
                enemyList.append((eX + 10, eY + 30))
        else:
            eX, eY = enemy[0], enemy[1]
            enemyList.append((eX + 10, eY + 30))

    return enemyList


def isInRegion(x, y, region):
    if region[0] <= x <= region[0] + region[2]:
        if region[1] <= y <= region[1] + region[3]:
            return True

    return False


def goToNearestEnemy(enemyList):
    pX, pY = Screen.center
    pPos = np.array([pX, pY])
    distances = {}
    for enemy in enemyList:
        ePos = np.array(enemy)
        distance = np.linalg.norm(ePos - pPos, ord=2)
        distances[enemy] = distance

    nearestEnemy = min(distances)
    pyautogui.click(nearestEnemy)


def battleStarted():
    region = imgrecg.convToRegion(380, 79, 420, 110)
    print(region)
    image = "images/clock.png"
    clock = pyautogui.locateOnScreen(image, region=region, grayscale=True, confidence=0.9)
    return clock is not None
