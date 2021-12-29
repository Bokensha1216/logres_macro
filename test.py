# import numpy as np
import pyautogui

import macros
from setup import *
from wrapping import *
from imageProcessing import *
import cv2
import copy
from macros import *


# findWindow()

# for i in range(5):
#     wait(0.1)
#     clickPosX, clickPosY = 50 + 80 * i, 760
#     click(clickPosX, clickPosY)
#     if i == 0:
#         wait(0.3)
#         region = convToRegion(0, 669, 157, 836)
#         while locateOnScreen("resizedImages/one.bmp", region=region, grayscale=True, confidence=0.7) is None:
#             wait(0.2)
#             click(clickPosX, clickPosY)

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
        cv2.rectangle(showImage, p1, p2, (0, 0, 255), 2)
    cv2.imshow("cont", showImage)

    return detectedRectangles


findWindow()
# img = cv2.imread('images/wolflv.bmp', 0)
img = Image.open("images/test.bmp")
region = (13, 721, 68, 71)
# imgori = screenshot()
# img = pil2cv(imgori)
# cv2.imwrite("images/test.bmp", img)
# lower, upper = (100, 70, 0), (110, 90, 0)
# offset = (0, appWindow.Status_y)
# recs = ContourRectangle(img, lower, upper, offset=offset, show=True)
# for rec in recs:
#     print(rec[2] * rec[3])


# cnts = detectContour(imgori, lower, upper)
# for cnt in cnts:
#     area = cv2.contourArea(cnt)
#     print(convAreaToVirtual(area))
# cnts = list(filter(lambda x: 60 >= cv2.contourArea(x) >= 20, cnts))
# sikaku = showContours(img, cnts)
# # print(len(cnts))
# # print(isSelected(cnts))
# for detectedRectangle in sikaku:
#     p1 = (detectedRectangle[0], detectedRectangle[1])
#     p2 = (p1[0] + detectedRectangle[2], p1[1] + detectedRectangle[3])
#     cv2.rectangle(bit, p1, p2, (255, 255, 255), -1)
# cv2.imshow("bit2", bit)

# img = pil2cv(imgori)
# bit = cv2.inRange(img, lower, upper)
# kernel = np.ones((1, 1), np.uint8)
# ero = cv2.erode(bit, kernel, iterations=1)
# cv2.imshow("bit", bit)
# kernel = np.ones((4, 4), np.uint8)
# dilation = cv2.dilate(ero, kernel, iterations=1)
# cv2.imshow("dil", dilation)
#
# contours, hierarchy = cv2.findContours(bit, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# showContours(img, contours)


# detectedRectangles = []
# for label in contours:
#     detectedRectangle = cv2.boundingRect(label)
#     detectedRectangles.append(detectedRectangle)
# # 表示
# img = pil2cv(img)
# showImage = copy.copy(img)
# for detectedRectangle in detectedRectangles:
#     p1 = (detectedRectangle[0], detectedRectangle[1])
#     p2 = (p1[0] + detectedRectangle[2], p1[1] + detectedRectangle[3])
#     cv2.rectangle(showImage, p1, p2, (0, 0, 255), 2)
#
# # for i, cnt in enumerate(contours):
# #     # 輪郭の面積を計算する。
# #     area = cv2.contourArea(cnt)
# #     print(f"contour: {i}, area: {area}")
#
# fil_contours = list(filter(lambda x: 150 >= cv2.contourArea(x) >= 90, contours))
# for i, cnt in enumerate(fil_contours):
#     # 輪郭の面積を計算する。
#     area = cv2.contourArea(cnt)
#     print(f"contour: {i}, area: {area}")
# showContours(img, fil_contours)
#
# cv2.imshow("検出物体", showImage)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# # approx_contours = []
# # for i, cnt in enumerate(fil_contours):
# #     # 輪郭の周囲の長さを計算する。
# #     arclen = cv2.arcLength(cnt, True)
# #     # 輪郭を近似する。
# #     approx_cnt = cv2.approxPolyDP(cnt, epsilon=0.005 * arclen, closed=True)
# #     approx_contours.append(approx_cnt)
# #
# # for i, cnt in enumerate(approx_contours):
# #     print(f"contour: {i}, number of points: {len(cnt)}")
#
# fil_contours = list(filter(lambda x: 10 >= len(x) >= 4, fil_contours))
# print("tenfil")
# for i, cnt in enumerate(fil_contours):
#     print(f"contour: {i}, number of points: {len(cnt)}")
#
# showContours(img, fil_contours)

# cv2.waitKey(0)
# cv2.destroyAllWindows()


# dst = cv2.GaussianBlur(img, (5, 5), 3)
# cv2.imshow("bruh", dst)

# edges = cv2.Canny(img,600,1000)
# # edges = cv2.Canny(img,800,900)
# #
# cv2.imshow("aa", img)
# cv2.imshow("edge", edges)
#
# kernel = np.ones((2, 2), np.uint8)
# bit = cv2.dilate(bit, kernel, iterations=1)
# cv2.imshow("dil1", bit)

# img_mask = cv2.medianBlur(bit,3)
# cv2.imshow("medblur", img_mask)

# kernel = np.ones((1, 1), np.uint8)
# ero = cv2.erode(bit, kernel, iterations=1)
# cv2.imshow("ero", ero)
# kernel = np.ones((4, 4), np.uint8)
# dilation = cv2.dilate(ero, kernel, iterations=3)
# cv2.imshow("dil2", dilation)

#
# contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
#
# detectedRectangles = []
# for label in contours:
#     detectedRectangle = cv2.boundingRect(label)
#     detectedRectangles.append(detectedRectangle)
# # 表示
# showImage = copy.copy(img)
# for detectedRectangle in detectedRectangles:
#     p1 = (detectedRectangle[0], detectedRectangle[1])
#     p2 = (p1[0] + detectedRectangle[2], p1[1] + detectedRectangle[3])
#     cv2.rectangle(showImage, p1, p2, (0, 0, 255), 2)
# cv2.imshow("検出物体", showImage)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# fil_contours = list(filter(lambda x: 280 >= cv2.contourArea(x) >= 100, contours))
# for i, cnt in enumerate(fil_contours):
#     # 輪郭の面積を計算する。
#     area = cv2.contourArea(cnt)
#     print(f"contour: {i}, area: {area}")
# detectedRectangles = []
# for label in fil_contours:
#     detectedRectangle = cv2.boundingRect(label)
#     detectedRectangles.append(detectedRectangle)
# # 表示
# showImage = copy.copy(img)
# for detectedRectangle in detectedRectangles:
#     p1 = (detectedRectangle[0], detectedRectangle[1])
#     p2 = (p1[0] + detectedRectangle[2], p1[1] + detectedRectangle[3])
#     cv2.rectangle(showImage, p1, p2, (0, 0, 255), 2)
# cv2.imshow("検出物体", showImage)
#
# fil_contours = list(filter(lambda x: 10 >= len(x) >= 4, fil_contours))
# print("tenfil")
# for i, cnt in enumerate(fil_contours):
#     print(f"contour: {i}, number of points: {len(cnt)}")
# showContours(img, fil_contours)
# # #
# # #
# # #
# # #
cv2.waitKey(0)
cv2.destroyAllWindows()
