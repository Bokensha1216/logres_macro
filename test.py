# import numpy as np
import numpy as np
import pyautogui

import macros
from setup import *
from wrapping import *
from imageProcessing import *
import cv2
import copy
from macros import *
from imgrecg import *

findWindow()

startBattle()

# for i in range(5):
#     wait(0.1)
#     clickPosX, clickPosY = 50 + 80 * i, 760
#     imgRange = (50, 50)
#     x1 = int(clickPosX - imgRange[0] / 2)
#     y1 = int(clickPosY - imgRange[1] / 2)
#     region = (x1, y1, imgRange[0], imgRange[1])
#     img1 = screenshot(region).convert("L")
#     click(clickPosX, clickPosY)
#     wait(0.3)
#     img2 = screenshot(region).convert("L")
#     img1 = pil2cv(img1)
#     img2 = pil2cv(img2)
#
#     img1_hist = cv2.calcHist([img1], [0], None, [256], [0, 256])
#     img2_hist = cv2.calcHist([img2], [0], None, [256], [0, 256])
#     if cv2.compareHist(img1_hist, img2_hist, 0) <= 0.8:
#         print("click seikou")
#     else:
#         img3 = screenshot(region).convert("L")
#         img3 = pil2cv(img3)
#         img3_hist = cv2.calcHist([img3], [0], None, [256], [0, 256])
#         if cv2.compareHist(img1_hist, img3_hist, 0) <= 0.8:
#             print("click seikou")
#         else:
#             print("click sippai")

# img = cv2.imread('images/wolflv.bmp', 0)
# click(131, 532, check=True)

# img = Image.open("images/test1.bmp")
# img = img.crop((region[0], region[1], region[0]+region[2], region[1]+region[3]))
# prmMin, prmMax = 200, 400
# contours = detectContourFromEdge(img, prmMin, prmMax, show=True)
# print(len(contours))
# showContours(img, contours)
# recs = ContoursToVirtualRectangles(contours, offset=(24, 692))
# recs = list(filter(lambda x: 3 >= x[2]/(x[3]+0.1) >= 2, recs))
# recs = list(filter(lambda x: 10000 >= x[2]*x[3] >= 5000, recs))
# for rec in recs:
#     print(rec, rec[2]*rec[3])
# fil_contours = list(filter(lambda x: areaMax >= convAreaToVirtual(cv2.contourArea(x)) >= areaMin, contours))
# recs = ContoursToVirtualRectangles(fil_contours, offset=(0, 0))
# return recs
# showImage = copy.copy(img)

# img = screenshot()
# elist = locateEnemy(limitRange=False)
# goToNearestEnemy(elist)
# low, upper = (105, 70, 0), (240, 200, 5)
# cv2.imshow("ori", pil2cv(img))
# showBitImage(img, low, upper)
# elist = locateEnemy(limitRange=False, locateRange=140, show=True)
# macros.traceEnemy(elist)

# imgori = screenshot()
# img = pil2cv(imgori)
# cv2.imwrite("images/test.bmp", img)


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
# prmMin, prmMax = 200, 400
# contours = detectContourFromEdge(img, prmMin, prmMax)
# fil_contours = list(filter(lambda x: 9000 >= convAreaToVirtual(cv2.contourArea(x)) >= 3000, contours))
# recs = ContoursToVirtualRectangles(fil_contours)
# mouichidoRegion = (0, 634, 500, 260)
# recs = filterDetectedRec(recs, mouichidoRegion)
# print(recs)
# showContours(img, contours)
# detectedRectangles = []
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
# fil_contours = list(filter(lambda x: 9000 >= cv2.contourArea(x) >= 3000, contours))
# for i, cnt in enumerate(fil_contours):
#     # 輪郭の面積を計算する。
#     area = cv2.contourArea(cnt)
#     print(f"contour: {i}, area: {area}, Varea: {convAreaToVirtual(area)}")
# showContours(showImage, fil_contours)
# for label in fil_contours:
#     detectedRectangle = cv2.boundingRect(label)
#     detectedRectangles.append(detectedRectangle)
# print(detectedRectangles)

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
