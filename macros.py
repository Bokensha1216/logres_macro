import _queue
import time

from wrapping import *
import numpy as np
import imgrecg
from imageProcessing import *
from questData import *
from perception import *


def locateQuestNavi():
    try:
        x, y, w, h = locateOnScreen("resizedImages/navi.bmp", region=appWindow.regionWithoutStatus, confidence=0.65)
    except TypeError:
        return None
    else:
        return x - 30, y + 56


def locateEnemy(limitRange=True, locateRange=100, locateCenter=None, show=False):
    img = screenshot(appWindow.regionWithoutStatus)
    img = pil2cv(img)
    if QuestData.dayOrNight == Stage.NIGHT:
        img = brightness(img, a=2, b=0)
    low, upper = (105, 70, 0), (240, 150, 5)
    offset = (0, appWindow.Status_y)
    ret = ContourRectangle(img, low, upper, show=False, offset=offset, conv=False)
    region = (0, 140, 500, 633)
    excRegion = (0, 171, 65, 64)
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


def goToNearestEnemy(enemyList, show=False):
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

    if show:
        img = screenshot()
        imgrecg.drawVecOnImage(img, appWindow.center, nearestEnemy)
        imgrecg.drawVecOnImage(img, nearestEnemy, clickPoint)

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
    region = convToRegion(367, 45, 446, 120)
    image = "resizedImages/clock.bmp"
    clock = locateOnScreen(image, region=region, grayscale=True, confidence=0.7)
    return clock is not None


def startBattle():
    # wait(4.5)
    wait(1)
    while isInBattle():
        try:
            enemyPos = EnemyPosOnBattle()
        except IndexError:
            wait(1)
        else:
            x, y = enemyPos[0][0], enemyPos[0][1]
            click(x, y)
            wait(0.5)
            x2, y2 = 440, 790
            pix = getPixel(x2, y2)
            if pix[0] >= 10:
                break

    wait(1.0)
    for i in range(5):
        wait(0.1)
        clickPosX, clickPosY = 50 + 80 * i, 760
        # imgRange = (50, 50)
        # x1 = int(clickPosX - imgRange[0] / 2)
        # y1 = int(clickPosY - imgRange[1] / 2)
        # region = (x1, y1, imgRange[0], imgRange[1])
        # img1 = screenshot(region).convert("L")
        click(clickPosX, clickPosY)
        # wait(0.3)
        # img2 = screenshot(region).convert("L")
        # if i == 0:
        #     wait(0.5)
        #     region = (13, 721, 68, 71)
        #     img = screenshot(region)
        #     lower, upper = (150, 255, 255), (255, 255, 255)
        #     cnts = detectContour(img, lower, upper)
        #     while isSelected(cnts) is False:
        #         print(isSelected(cnts))
        #         click(clickPosX, clickPosY)
        #         wait(0.5)
        #         img = screenshot(region)
        #         cnts = detectContour(img, lower, upper)
        # else:
        #     img1 = pil2cv(img1)
        #     img2 = pil2cv(img2)
        #     img1_hist = cv2.calcHist([img1], [0], None, [256], [0, 256])
        #     img2_hist = cv2.calcHist([img2], [0], None, [256], [0, 256])
        #     if cv2.compareHist(img1_hist, img2_hist, 0) <= 0.8:
        #         continue
        #     else:
        #         wait(0.1)
        #         img3 = screenshot(region).convert("L")
        #         img3 = pil2cv(img3)
        #         img3_hist = cv2.calcHist([img3], [0], None, [256], [0, 256])
        #         if cv2.compareHist(img1_hist, img3_hist, 0) <= 0.8:
        #             continue
        #         else:
        #             print("click fail")
        #             click(clickPosX, clickPosY)


def differ(img1, img2):
    img1 = img1.convert("L")
    img2 = img2.convert("L")
    cnts1 = detectContourFromEdge(img1, 300, 600, show=False, kernel=1)
    cnts2 = detectContourFromEdge(img2, 300, 600, show=False, kernel=1)
    cnts1 = list(filter(lambda x: convAreaToVirtual(cv2.contourArea(x)) >= 10, cnts1))
    cnts2 = list(filter(lambda x: convAreaToVirtual(cv2.contourArea(x)) >= 10, cnts2))

    if len(cnts1) != len(cnts2):
        return True
    else:
        ruiji = []
        for cnt1 in cnts1:
            for cnt2 in cnts2:
                ret = cv2.matchShapes(cnt1, cnt2, cv2.CONTOURS_MATCH_I1, 0)
                ruiji.append(ret)
        try:
            print(min(ruiji))
            if min(ruiji) > 1:
                return True
            else:
                return False
        except ValueError:
            return True


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


# def EnemyPosOnBattle():
#     img = screenshot(region=appWindow.regionWithoutStatus)
#     low, upper = (0, 0, 0), (255, 0, 255)
#     offset = (0, appWindow.Status_y)
#     lines = detectLine(img, low, upper, offset=offset, show=False)
#     region = (244, 163, 275, 513)
#     lines = filterDetectedRec(lines, region)
#     lines = mergeLines(lines)
#     return [RegionCenter(line) for line in lines]

def EnemyPosOnBattle():
    region = (0, 90, 500, 620)
    offset = (0, 90)
    # fps = 10.0
    #
    # recoder = Recoder(fps)
    # images = recoder.record(10, region)
    #
    # moveImages = movement(images, step=1)
    # moveSum = MoveSum(moveImages, 0)
    # recs = detectMovingObject(moveSum, 1000, 70000, showArea=False, dilL=2, offset=offset)
    # drawOnImage(images[-1], recs, show=True, offset=offset)

    img = screenshot(region=region)
    cnts = detectFromStillImage(img, 1000, 70000)
    # showContours(img, cnts)
    recs = ContoursToVirtualRectangles(cnts, offset=offset)
    # drawOnImage(img, recs, offset=offset)

    hyouka = getEnemy(recs)

    enemies = []
    for kouho in hyouka:
        if hyouka[kouho][0] > 0.5:
            enemies.append(kouho)

    if len(enemies) == 0:
        raise IndexError

    enemies.sort(reverse=True, key=lambda x:hyouka[x][0])

    # for enemy in enemies:
    #     print(hyouka[enemy])
    return [RegionCenter(enemy) for enemy in enemies]


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
        if convAreaToVirtual(rec[2] * rec[3]) > 9000:
            return True

    return False


def goToNextQuest():
    def detectButton(img):
        areaMin, areaMax = 2000, 12000
        # region = (24, 445, 452, 423)
        # img = screenshot(region=region)
        # offset = (24, 445)
        offset = (0, 0)

        prmMin, prmMax = 200, 400
        contours = detectContourFromEdge(img, prmMin, prmMax, show=False, external=False)
        fil_contours = list(filter(lambda x: areaMax >= convAreaToVirtual(cv2.contourArea(x)) >= areaMin, contours))
        recs = ContoursToVirtualRectangles(fil_contours, offset=offset)
        recs = list(filter(lambda x: 5 >= x[2] / (x[3] + 0.1) >= 1.5, recs))
        recs = list(filter(lambda x: 10000 >= x[2] * x[3] >= 2000, recs))
        recs = non_max_suppression(recs)
        return recs

    def posHyouka(poses):
        def sigmoid(x):
            sigmoid_range = 34.538776394910684
            return 1.0 / (1.0 + np.exp(-np.clip(x, -sigmoid_range, sigmoid_range)))

        hyouka = {}
        for pos in poses:
            hyouka[pos] = []

            # x
            pos_x = pos[0]
            pos_x = (pos_x - 250) / 50
            h = sigmoid(pos_x)
            hyouka[pos].append(h)

            # y
            pos_y = pos[1]
            pos_y = (pos_y - 450) / 90
            h = sigmoid(pos_y)
            hyouka[pos].append(h)

        # print(hyouka)

        return hyouka

    def selectButton(buttons):
        buttonCenters = [RegionCenter(button) for button in buttons]
        # button = random.choice(buttonCenters)
        hyouka = posHyouka(buttonCenters)
        for button in hyouka:
            buttonSim = sum(hyouka[button])
            hyouka[button] = buttonSim
        # print(hyouka)
        button = max(hyouka, key=hyouka.get)
        return button

    # もう一回ボタン
    clickPosX, clickPosY = 157, 541
    imgRange = (50, 50)
    x1 = int(clickPosX - imgRange[0] / 2)
    y1 = int(clickPosY - imgRange[1] / 2)
    region = (x1, y1, imgRange[0], imgRange[1])
    img1 = screenshot(region).convert("L")
    click(clickPosX, clickPosY)
    wait(0.3)
    img2 = screenshot(region).convert("L")
    img1 = pil2cv(img1)
    img2 = pil2cv(img2)
    img1_hist = cv2.calcHist([img1], [0], None, [256], [0, 256])
    img2_hist = cv2.calcHist([img2], [0], None, [256], [0, 256])
    if cv2.compareHist(img1_hist, img2_hist, 0) <= 0.8:
        pass
    else:
        img3 = screenshot(region).convert("L")
        img3 = pil2cv(img3)
        img3_hist = cv2.calcHist([img3], [0], None, [256], [0, 256])
        if cv2.compareHist(img1_hist, img3_hist, 0) <= 0.8:
            pass
        else:
            click(clickPosX, clickPosY)

    wait(7)

    # 一番評価の高いボタンをフィールドに戻るまで押す
    while not isInField():
        buttons = detectButton(screenshot())
        print(len(buttons))

        if 1 <= len(buttons):
            button = selectButton(buttons)
            click(*button)
        wait(3)


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
