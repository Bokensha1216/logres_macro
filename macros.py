import _queue
import time

from wrapping import *
import numpy as np
import imgrecg
from imageProcessing import *


def locateQuestNavi():
    try:
        x, y, w, h = locateOnScreen("resizedImages/navi.bmp", region=appWindow.regionWithoutStatus, confidence=0.65)
    except TypeError:
        return None
    else:
        return x - 30, y + 56


# def locateEnemy(limitRange=True, locateRange=100, locateCenter=None):
#     enemies = locateAllOnScreen("resizedImages/lv.bmp", appWindow.regionWithoutStatus, confidence=0.7, grayscale=True)
#
#     enemyList = []
#     for enemy in enemies:
#         if limitRange:
#             naviX, naviY = locateCenter
#             region = (naviX - locateRange, naviY - locateRange, 2 * locateRange, 2 * locateRange)
#             eX, eY = enemy[0], enemy[1]
#             if isInRegion(eX, eY, region):
#                 enemyList.append((eX + 11, eY + 39))
#         else:
#             eX, eY = enemy[0], enemy[1]
#             enemyList.append((eX + 11, eY + 39))
#
#     return enemyList

def locateEnemy(limitRange=True, locateRange=100, locateCenter=None, show=False):
    img = screenshot(appWindow.regionWithoutStatus)
    low, upper = (105, 70, 0), (240, 200, 5)
    offset = (0, appWindow.Status_y)
    ret = ContourRectangle(img, low, upper, show=False, offset=offset)
    region = (0, 140, 500, 683)
    excRegion = (0, 181, 65, 54)
    enemies = filterDetectedRec(ret, region, excRegion=excRegion)

    if limitRange is True:
        naviX, naviY = locateCenter
        region = (naviX - locateRange, naviY - locateRange, 2 * locateRange, 2 * locateRange)

        # img = screenshot()
        # drawSingleOnImage(img, region)

        enemies = filterDetectedRec(enemies, region)

    if show:
        img = screenshot()
        drawOnImage(img, enemies)

    enemyList = [(eX + 15, eY + 50) for eX, eY, _, _ in enemies]

    return enemyList


def goToNearestEnemy(enemyList):
    pX, pY = appWindow.center
    pPos = np.array([pX, pY])
    distances = {}
    for enemy in enemyList:
        ePos = np.array(enemy)
        distance = np.linalg.norm(ePos - pPos, ord=2)
        distances[enemy] = distance

    nearestEnemy = min(distances, key=distances.get)
    # print(distances, nearestEnemy)
    direction = imgrecg.direction_vec(appWindow.center, nearestEnemy)
    keisu = 0
    if distances[nearestEnemy] <= 50:
        keisu = 10
        if distances[nearestEnemy] <= 10:
            keisu = 30
    clickPoint = (nearestEnemy + direction * keisu)

    # img = screenshot()
    # imgrecg.drawVecOnImage(img, appWindow.center, nearestEnemy)
    # imgrecg.drawVecOnImage(img, nearestEnemy, clickPoint)

    click(int(clickPoint[0]), int(clickPoint[1]))
    return nearestEnemy


def traceEnemy(enemyList):
    clickedPoint = goToNearestEnemy(enemyList)
    wait(1)

    while not isInBattle():
        enemyList = locateEnemy(limitRange=True, locateRange=140, locateCenter=clickedPoint)
        while len(enemyList) == 0:
            wait(0.5)
            enemyList = locateEnemy(limitRange=True, locateRange=140, locateCenter=clickedPoint)
            if isInBattle():
                return

        clickedPoint = goToNearestEnemy(enemyList)
        wait(1)


def isInBattle():
    region = convToRegion(367, 45, 446, 110)
    image = "resizedImages/clock.bmp"
    clock = locateOnScreen(image, region=region, grayscale=True, confidence=0.7)
    return clock is not None


def startBattle(checkClick=False):
    wait(4.5)
    while isInBattle():
        try:
            enemyPos = EnemyPosOnBattle()
        except IndexError:
            wait(1)
        else:
            x, y = enemyPos[0][0], enemyPos[0][1] - 15
            click(x, y)
            wait(0.5)
            x2, y2 = 440, 790
            pix = getPixel(x2, y2)
            while pix[0] < 10:
                click(x, y)
                wait(0.5)
                pix = getPixel(x2, y2)

                if not isInBattle():
                    return
            break

    wait(1.0)
    for i in range(5):
        wait(0.1)
        clickPosX, clickPosY = 50 + 80 * i, 760
        click(clickPosX, clickPosY)
        if i == 0 and checkClick is True:
            wait(0.5)
            region = (13, 721, 68, 71)
            img = screenshot(region)
            lower, upper = (150, 255, 255), (255, 255, 255)
            cnts = detectContour(img, lower, upper)
            while isSelected(cnts) is False:
                print(isSelected(cnts))
                click(clickPosX, clickPosY)
                wait(0.5)
                img = screenshot(region)
                cnts = detectContour(img, lower, upper)


def run():
    click(440, 865)
    wait(1)
    click(250, 538)


# 武器が選択されているか
def isSelected(contours, areaThr=25):
    areaThr = convAreaToScreen(areaThr)
    if len(contours) >= 40:
        return False
    else:
        for cnt in contours:
            # area = cv2.contourArea(cnt)
            # print(convAreaToVirtual(area))
            if cv2.contourArea(cnt) > areaThr:
                return True
        return False


def EnemyPosOnBattle():
    img = screenshot(region=appWindow.regionWithoutStatus)
    low, upper = (0, 0, 0), (255, 0, 255)
    offset = (0, appWindow.Status_y)
    lines = detectLine(img, low, upper, offset=offset, show=False)
    region = (244, 163, 275, 513)
    lines = filterDetectedRec(lines, region)
    lines = mergeLines(lines)
    return [RegionCenter(line) for line in lines]


# フィールド画面に戻るまで待つ
def waitField(sec=0.2):
    region = convToRegion(263, 0, 378, 104)
    friendIcon = locateOnScreen("resizedImages/people.bmp", region=region, confidence=0.65,
                                grayscale=True)
    while friendIcon is None:
        print("notpeople")
        wait(sec)
        if questCleared():
            break
        friendIcon = locateOnScreen("resizedImages/people.bmp", region=region, confidence=0.65,
                                    grayscale=True)


def isInField():
    region = convToRegion(263, 0, 378, 104)
    friendIcon = locateOnScreen("resizedImages/people.bmp", region=region, confidence=0.65,
                                grayscale=True)
    if friendIcon is None:
        return False
    else:
        return True


def isInHome():
    region = (360, 0, 69, 51)
    takara = locateOnScreen("resizedImages/takara.bmp", region=region, confidence=0.65,
                                grayscale=True)
    if takara is None:
        return False
    else:
        return True


def questCleared():
    img = screenshot(region=appWindow.regionWithoutStatus)
    lower, upper = (100, 70, 0), (110, 90, 0)
    offset = (0, appWindow.Status_y)
    recs = ContourRectangle(img, lower, upper, offset=offset)
    for rec in recs:
        if rec[2] * rec[3] > 10000:
            return True

    return False


def goToNextQuest():
    # もう一回ボタン
    click(157, 541)
    wait(5)

    # 出発ボタン
    syuppatuRegion = convToRegion(289, 716, 474, 815)
    syuppatu = locateCenterOnScreen("resizedImages/syuppatu.bmp", region=syuppatuRegion, confidence=0.7,
                                    grayscale=True)

    while syuppatu is None:
        # もう一度挑戦ボタン
        mouichidoRegion = convToRegion(262, 762, 477, 881)
        print("checkmouichido")
        mouichido = locateCenterOnScreen("resizedImages/mouichido.bmp", region=mouichidoRegion, confidence=0.7,
                                         grayscale=True)
        if mouichido is not None:
            click(mouichido[0], mouichido[1])
            wait(3)

        # 開封ボタン
        kaihu = locateCenterOnScreen("resizedImages/kaihu.bmp", region=appWindow.regionWithoutStatus, confidence=0.7,
                                     grayscale=True)
        if kaihu is not None:
            click(kaihu[0], kaihu[1])
            wait(1)

        wait(1)
        syuppatu = locateCenterOnScreen("resizedImages/syuppatu.bmp", region=syuppatuRegion, confidence=0.7,
                                        grayscale=True)
    wait(0.5)
    # print(syuppatu, syuppatuRegion)
    click(393, 773)


def wait(sec):
    if sec <= 1:
        checkEvent()
        time.sleep(sec)
    elif sec <= 10:
        for i in range(int(sec / 0.5)):
            checkEvent()
            time.sleep(0.5)
    else:
        for i in range(int(sec)):
            checkEvent()
            time.sleep(1)


def checkEvent():
    try:
        event = appWindow.eventQueue.get(block=False)
        if isinstance(event, Exception):
            raise event
    except _queue.Empty:
        pass
