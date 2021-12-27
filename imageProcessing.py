import cv2
import numpy as np
import copy

from wrapping import *


def pil2cv(image):
    ''' PIL型 -> OpenCV型 '''
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image


# image 対象画像, template 検知したい画像名, lower upper 下限上限 2値化に使う, threshold 検知精度 show 検知結果を表示するか
def detectTemplate(image, template, lower, upper, threshold, show=False):
    # openCV型に変換
    img = pil2cv(image)
    # 2値化
    imgBin = cv2.inRange(img, lower, upper)
    # 検知画像読込
    templateImg = cv2.imread(template, 0)
    # 検知
    res = cv2.matchTemplate(imgBin, templateImg, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    # 検知結果を表示
    if show is True:
        h, w = templateImg.shape
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        cv2.imshow(template, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    # (x, y)のリストに加工して返す
    itemList = []
    for pt in zip(*loc[::-1]):
        itemList.append((pt[0], pt[1]))
    return itemList


def showBitImage(image, lower, upper):
    img = pil2cv(image)
    imgBin = cv2.inRange(img, lower, upper)
    cv2.imshow("bit", imgBin)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return imgBin


def ContourRectangle(image, lower, upper, show=False, offset=(0, 0)):
    # openCV型に変換
    img = pil2cv(image)
    # 2値化
    imgBin = cv2.inRange(img, lower, upper)
    # 膨張
    kernel = np.ones((8, 8), np.uint8)
    # kernel = np.array([
    #     [1,1,1],
    #     [1,1,1],
    #     [1,1,1]], np.uint8
    # )
    dilation = cv2.dilate(imgBin, kernel, iterations=2)
    # 輪郭検出
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 長方形にする
    detectedRectangles = []
    for label in contours:
        detectedRectangle = cv2.boundingRect(label)
        detectedRectangles.append(detectedRectangle)
    # 表示
    if show is True:
        showImage = copy.copy(img)
        for detectedRectangle in detectedRectangles:
            p1 = (detectedRectangle[0], detectedRectangle[1])
            p2 = (p1[0] + detectedRectangle[2], p1[1] + detectedRectangle[3])
            cv2.rectangle(showImage, p1, p2, (0, 0, 255), 2)
        cv2.imshow("検出物体", showImage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    # 変換して返還
    detectedRectangles = [ImageRegionToVirtual(i, offset) for i in detectedRectangles]

    return detectedRectangles


def ImageRegionToVirtual(region, offset):
    # 画像座標をクライアント座標に変換
    x, y, w, h = region[0] + offset[0], region[1] + offset[1], region[2], region[3]
    # # クライアント座標を仮想座標に変換
    # region = RegionClientToCoordinate((x, y, w, h))
    region = (x, y, w, h)
    return region


def filterDetectedRec(detRecs, region, ExcRegion=None):
    for detRec in detRecs:
        center = (int(detRec[0] + detRec[2] / 2), int(detRec[1] + detRec[3] / 2))


def isInRegion(region, point, offset=(0, 0)):
    pass


def drawOnImage(image, rectangles):
    image = pil2cv(image)
    for rec in rectangles:
        p1 = (rec[0], rec[1])
        p2 = (p1[0] + rec[2], p1[1] + rec[3])
        cv2.rectangle(image, p1, p2, (0, 0, 255), 2)
    cv2.imshow("draw", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
