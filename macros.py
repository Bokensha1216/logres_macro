import _queue
import time

from wrapping import *
import numpy as np


def locateQuestNavi():
    try:
        x, y, w, h = locateOnScreen("resizedImages/navi.bmp", region=appWindow.regionWithoutStatus, confidence=0.65)
    except TypeError:
        return None
    else:
        return x - 30, y + 56


def locateEnemy(limitRange=True, locateRange=100, locateCenter=None):
    enemies = locateAllOnScreen("resizedImages/lv.bmp", appWindow.regionWithoutStatus, confidence=0.7, grayscale=True)

    enemyList = []
    for enemy in enemies:
        if limitRange:
            naviX, naviY = locateCenter
            region = (naviX - locateRange, naviY - locateRange, 2 * locateRange, 2 * locateRange)
            eX, eY = enemy[0], enemy[1]
            if isInRegion(eX, eY, region):
                enemyList.append((eX + 11, eY + 39))
        else:
            eX, eY = enemy[0], enemy[1]
            enemyList.append((eX + 11, eY + 39))

    return enemyList


def isInRegion(x, y, region):
    if region[0] <= x <= region[0] + region[2]:
        if region[1] <= y <= region[1] + region[3]:
            return True

    return False


def goToNearestEnemy(enemyList):
    pX, pY = appWindow.center
    pPos = np.array([pX, pY])
    distances = {}
    for enemy in enemyList:
        ePos = np.array(enemy)
        distance = np.linalg.norm(ePos - pPos, ord=2)
        distances[enemy] = distance

    nearestEnemy = min(distances)
    direction = imgrecg.direction_vec(appWindow.center, nearestEnemy)
    clickPoint = nearestEnemy + direction * 30
    click(clickPoint[0], clickPoint[1])
    return nearestEnemy


def traceEnemy(enemyList):
    clickedPoint = goToNearestEnemy(enemyList)
    wait(0.5)

    while not isInBattle():
        enemyList = locateEnemy(limitRange=True, locateRange=140, locateCenter=clickedPoint)
        while len(enemyList) == 0:
            wait(0.5)
            enemyList = locateEnemy(limitRange=True, locateRange=140, locateCenter=clickedPoint)
            if isInBattle():
                return

        clickedPoint = goToNearestEnemy(enemyList)
        wait(0.5)


def isInBattle():
    region = convToRegion(367, 45, 446, 110)
    image = "resizedImages/clock.bmp"
    clock = locateOnScreen(image, region=region, grayscale=True, confidence=0.7)
    return clock is not None


def startBattle():
    x, y = 336, 216
    click(x, y)
    wait(1.5)
    x2, y2 = 440, 790
    pix = getPixel(x2, y2)
    while pix[0] < 10:
        wait(0.5)
        click(x, y)
        pix = getPixel(x2, y2)

    for i in range(5):
        wait(0.1)
        clickPosX, clickPosY = 50 + 80 * i, 760
        click(clickPosX, clickPosY)
        if i == 0:
            wait(0.2)
            pix = getPixel(clickPosX, clickPosY)
            print(pix)
            while imgrecg.totalRGB(pix) < 700:
                click(clickPosX, clickPosY)
                wait(0.2)
                pix = getPixel(clickPosX, clickPosY)
                print(pix)


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


def questCleared():
    q = locateOnScreen("resizedImages/ku.bmp", region=appWindow.regionWithoutStatus, confidence=0.6,
                       grayscale=True)

    return q is not None


def goToNextQuest():
    # もう一回ボタン
    click(157, 541)
    wait(5)

    # 出発ボタン
    syuppatuRegion = convToRegion(289, 716, 474, 815)
    syuppatu = locateCenterOnScreen("resizedImages/syuppatu.bmp", region=syuppatuRegion, confidence=0.7,
                                    grayscale=True)
    # x, y = (371, 763)
    # pix = getPixel(x, y)
    while syuppatu is None:
        # もう一度挑戦ボタン
        mouichidoRegion = convToRegion(262, 762, 477, 881)
        print("checkmouichido")
        mouichido = locateCenterOnScreen("resizedImages/mouichido.bmp", region=mouichidoRegion, confidence=0.7,
                                         grayscale=True)
        if mouichido is not None:
            click(mouichido[0], mouichido[1])
            wait(2)

        # 開封ボタン
        kaihu = locateCenterOnScreen("resizedImages/kaihu.bmp", region=appWindow.regionWithoutStatus, confidence=0.7,
                                     grayscale=True)
        if kaihu is not None:
            click(kaihu[0], kaihu[1])
            wait(1)

        wait(1)
        syuppatu = locateCenterOnScreen("resizedImages/syuppatu.bmp", region=syuppatuRegion, confidence=0.7,
                                        grayscale=True)
    click(syuppatu[0], syuppatu[1])


def wait(sec):
    if sec <= 1:
        checkEvent()
        time.sleep(sec)
    elif sec <= 10:
        for i in range(int(sec/0.5)):
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

