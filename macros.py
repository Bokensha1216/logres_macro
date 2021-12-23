import numpy as np
import pyautogui

import imgrecg
from setup import *


def locateQuestNavi():
    try:
        x, y, w, h = pyautogui.locateOnScreen("images/navi.png", region=Screen.regionWithoutStatus, confidence=0.65,
                                          grayscale=True)
    except TypeError:
        return None
    else:
        return x - 10, y + 50


def locateEnemy(limitRange=True, locateRange=100, locateCenter=None):
    enemies = imgrecg.locateAll("images/lv.png", confidence=0.64)

    enemyList = []
    for enemy in enemies:
        if limitRange:
            # naviX, naviY = locateQuestNavi()
            naviX, naviY = locateCenter
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
    direction = imgrecg.direction_vec(Screen.center, nearestEnemy)
    clickPoint = nearestEnemy + direction*10
    pyautogui.click(clickPoint[0], clickPoint[1])
    return nearestEnemy


def traceEnemy(enemyList):
    clickedPoint = goToNearestEnemy(enemyList)
    time.sleep(0.5)

    while not isInBattle():
        enemyList = locateEnemy(limitRange=True, locateRange=140, locateCenter=clickedPoint)
        while len(enemyList) == 0:
            time.sleep(0.5)
            enemyList = locateEnemy(limitRange=True, locateRange=140, locateCenter=clickedPoint)
            if isInBattle():
                return

        clickedPoint = goToNearestEnemy(enemyList)
        time.sleep(0.5)




def isInBattle():
    region = imgrecg.convToRegion(380, 79, 420, 110)
    image = "images/clock.png"
    clock = pyautogui.locateOnScreen(image, region=region, grayscale=True, confidence=0.9)
    return clock is not None


def startBattle():
    pyautogui.click(imgrecg.convToAbs(328, 226))
    time.sleep(1.5)
    pix = imgrecg.getPixel(435, 785)
    while pix[0] < 10:
        time.sleep(0.5)
        pyautogui.click(imgrecg.convToAbs(328, 226))
        pix = imgrecg.getPixel(435, 785)

    for i in range(5):
        pyautogui.click(imgrecg.convToAbs(50 + 80 * i, 750))
        if i == 0:
            pix = imgrecg.getPixel(50 + 80 * i, 750)
            print(pix)
            while pix != (255, 255, 255):
                time.sleep(0.2)
                pyautogui.click(imgrecg.convToAbs(50 + 80 * i, 750))
                pix = imgrecg.getPixel(50 + 80 * i, 750)


# フィールド画面に戻るまで待つ
def waitField(sec=0.2):
    pix = imgrecg.getPixel(314, 40)
    while pix[2] > 10:
        time.sleep(sec)
        pix = imgrecg.getPixel(314, 40)


def questCleared():
    q = pyautogui.locateOnScreen("images/ku.jpg", region=Screen.regionWithoutStatus, confidence=0.6,
                                 grayscale=True)

    return q is not None


def goToNextQuest():
    # もう一回ボタン
    pyautogui.click(imgrecg.convToAbs(157, 541))
    time.sleep(5)

    # 出発ボタン
    x, y = (371, 763)
    pix = imgrecg.getPixel(x, y)
    while pix != (255, 255, 255):
        # 次ボタン
        x2, y2 = (385, 827)
        pix2 = imgrecg.getPixel(x2, y2)
        if pix2 == (255, 255, 255):
            pyautogui.click(imgrecg.convToAbs(x2, y2))
            time.sleep(1)
            
        # 開封ボタン
        kaihu = pyautogui.locateCenterOnScreen("images/kaihu.jpg", region=Screen.regionWithoutStatus, confidence=0.6,
                                     grayscale=True)
        if kaihu is not None:
            pyautogui.click(kaihu)
            time.sleep(1)

        time.sleep(1)
        pix = imgrecg.getPixel(x, y)
    pyautogui.click(imgrecg.convToAbs(x, y))
