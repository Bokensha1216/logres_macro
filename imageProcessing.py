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
    # offsetをクライアント座標に変換
    offset = coordinateToPixelRelative(*offset)
    # 画像座標をクライアント座標に変換
    x, y, w, h = region[0] + offset[0], region[1] + offset[1], region[2], region[3]
    # クライアント座標を仮想座標に変換
    region = RegionClientToCoordinate((x, y, w, h))
    return region


def VirtualRegionToImage(region, offset):
    # offsetをクライアント座標に変換
    offset = coordinateToPixelRelative(*offset)
    # 仮想座標をクライアント座標に変換
    region = RegionCoordinateToClient(region)
    # クライアント座標を画像座標に変換
    region = (region[0] - offset[0], region[1] - offset[1], region[2], region[3])
    return region


def filterDetectedRec(detRecs, region, excRegion=None):
    filDecRec = []
    for detRec in detRecs:
        center = (int(detRec[0] + detRec[2] / 2), int(detRec[1] + detRec[3] / 2))
        if isInRegion(region, center):
            filDecRec.append(detRec)

            if excRegion is not None:
                if isInRegion(excRegion, center):
                    filDecRec.pop(-1)
    return filDecRec


def isInRegion(region, point):
    x, y = point
    x1, y1, x2, y2 = region[0], region[1], region[0] + region[2], region[1] + region[3]
    if x1 < x < x2 and y1 < y < y2:
        return True
    else:
        return False


def drawOnImage(image, rectangles, offset=(0, 0)):
    rectangles = [VirtualRegionToImage(rectangle, offset) for rectangle in rectangles]

    image = pil2cv(image)
    for rec in rectangles:
        p1 = (rec[0], rec[1])
        p2 = (p1[0] + rec[2], p1[1] + rec[3])
        cv2.rectangle(image, p1, p2, (0, 0, 255), 2)
    cv2.imshow("draw", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def drawSingleOnImage(image, rectangle, offset=(0, 0)):
    image = pil2cv(image)
    rec = VirtualRegionToImage(rectangle, offset)
    p1 = (rec[0], rec[1])
    p2 = (p1[0] + rec[2], p1[1] + rec[3])
    cv2.rectangle(image, p1, p2, (0, 0, 255), 2)
    cv2.imshow("draw", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def detectLine(image, lower, upper, show=False, offset=(0, 0), tilt=(0, 0.3)):
    # openCV型に変換
    img = pil2cv(image)
    # 2値化
    imgBin = cv2.inRange(img, lower, upper)
    # 縮小
    kernel = np.ones((2, 2), np.uint8)
    ero = cv2.erode(imgBin, kernel, iterations=1)
    # 膨張
    kernel = np.ones((5, 5), np.uint8)
    dilation = cv2.dilate(ero, kernel, iterations=1)
    # 直線検出
    threshold = 50
    minLineLength = 40
    maxLineGap = 10
    lines = cv2.HoughLinesP(dilation, rho=1, theta=np.pi / 360, threshold=threshold, minLineLength=minLineLength,
                            maxLineGap=maxLineGap)
    # 傾きでフィルター
    lines = [line[0] for line in lines]
    fil_lines = []
    for line in lines:
        x1, y1, x2, y2 = line
        if x2 - x1 == 0:
            print("ゼロ除算")
            continue
        m = (y2 - y1) / (x2 - x1)
        if tilt[0] - tilt[1] <= m <= tilt[0] + tilt[1]:
            fil_lines.append(line)
    lines = fil_lines

    # 表示
    if show is True:
        lineImage = pil2cv(image)
        for line in lines:
            x1, y1, x2, y2 = line
            # 赤線を引く
            red_line_img = cv2.line(lineImage, (x1, y1), (x2, y2), (255, 0, 0), 3)
        cv2.imshow("draw", lineImage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    # 変換して返還
    lines = [convToRegion(x1, y1, x2, y2) for x1, y1, x2, y2 in lines]
    lines = [ImageRegionToVirtual(line, offset) for line in lines]
    return lines


def mergeLines(lines, distance=50):
    mergedLines = [lines.pop(0)]
    while len(lines) > 0:
        line = lines.pop(0)
        flag = False
        for i, ml in enumerate(mergedLines):
            if abs(ml[1] - line[1]) <= distance:
                mergedLines[i] = (min(ml[0], line[0]), min(ml[1], line[1]), max(ml[2], line[2]), max(ml[3], line[3]))
                flag = True
                break
        if flag is False:
            mergedLines.append(line)
    return mergedLines


def detectContour(image, lower, upper):
    img = pil2cv(image)
    bit = cv2.inRange(img, lower, upper)
    contours, hierarchy = cv2.findContours(bit, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def detectEdge(image, prmMin, prmMax, show=False):
    img = pil2cv(image)
    edges = cv2.Canny(img, prmMin, prmMax)
    if show:
        cv2.imshow("edge", edges)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return edges


def detectContourFromEdge(image, prmMin, prmMax, kernel=3, show=False, external=True):
    # エッジ検出
    edge = detectEdge(image, prmMin, prmMax, show=show)
    # 膨張
    kernel = np.ones((kernel, kernel), np.uint8)
    dil = cv2.dilate(edge, kernel, iterations=1)
    # 輪郭検出
    mode = cv2.RETR_EXTERNAL if external else cv2.RETR_LIST
    contours, hierarchy = cv2.findContours(dil, mode, cv2.CHAIN_APPROX_SIMPLE)
    if show:
        cv2.imshow("dil", dil)
        showContours(image, contours)
    return contours


def showContours(img, contours):
    detectedRectangles = []
    for label in contours:
        detectedRectangle = cv2.boundingRect(label)
        detectedRectangles.append(detectedRectangle)
    # 表示
    showImage = pil2cv(img)
    for detectedRectangle in detectedRectangles:
        p1 = (detectedRectangle[0], detectedRectangle[1])
        p2 = (p1[0] + detectedRectangle[2], p1[1] + detectedRectangle[3])
        cv2.rectangle(showImage, p1, p2, (255, 0, 0), 2)
    cv2.imshow("cont", showImage)

    return detectedRectangles


def ContoursToVirtualRectangles(contours, offset=(0, 0)):
    recs = [cv2.boundingRect(cnt) for cnt in contours]
    recs = [ImageRegionToVirtual(rec, offset) for rec in recs]
    return recs
