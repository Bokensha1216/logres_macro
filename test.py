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


def detectButton(areaMin, areaMax):
    region = (24, 445, 452, 423)
    img = screenshot(region=region)
    offset = (24, 445)
    prmMin, prmMax = 200, 400
    contours = detectContourFromEdge(img, prmMin, prmMax)
    fil_contours = list(filter(lambda x: areaMax >= convAreaToVirtual(cv2.contourArea(x)) >= areaMin, contours))
    recs = ContoursToVirtualRectangles(fil_contours, offset=offset)
    recs = list(filter(lambda x: 5 >= x[2] / (x[3] + 0.1) >= 1.5, recs))
    recs = list(filter(lambda x: 10000 >= x[2] * x[3] >= 2000, recs))
    recs = non_max_suppression(recs)
    return recs


buttons = detectButton(2000, 12000)
print(len(buttons))
if 1 <= len(buttons):
    buttonCenters = [RegionCenter(button) for button in buttons]
    x, y = max(buttonCenters, key=lambda center: center[0])
    click(x, y)

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
# # ??????
# img = pil2cv(img)
# showImage = copy.copy(img)
# for detectedRectangle in detectedRectangles:
#     p1 = (detectedRectangle[0], detectedRectangle[1])
#     p2 = (p1[0] + detectedRectangle[2], p1[1] + detectedRectangle[3])
#     cv2.rectangle(showImage, p1, p2, (0, 0, 255), 2)
#
# # for i, cnt in enumerate(contours):
# #     # ?????????????????????????????????
# #     area = cv2.contourArea(cnt)
# #     print(f"contour: {i}, area: {area}")
#
# fil_contours = list(filter(lambda x: 150 >= cv2.contourArea(x) >= 90, contours))
# for i, cnt in enumerate(fil_contours):
#     # ?????????????????????????????????
#     area = cv2.contourArea(cnt)
#     print(f"contour: {i}, area: {area}")
# showContours(img, fil_contours)
#
# cv2.imshow("????????????", showImage)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# # approx_contours = []
# # for i, cnt in enumerate(fil_contours):
# #     # ??????????????????????????????????????????
# #     arclen = cv2.arcLength(cnt, True)
# #     # ????????????????????????
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
# # ??????
# showImage = copy.copy(img)
# for detectedRectangle in detectedRectangles:
#     p1 = (detectedRectangle[0], detectedRectangle[1])
#     p2 = (p1[0] + detectedRectangle[2], p1[1] + detectedRectangle[3])
#     cv2.rectangle(showImage, p1, p2, (0, 0, 255), 2)
# cv2.imshow("????????????", showImage)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# fil_contours = list(filter(lambda x: 9000 >= cv2.contourArea(x) >= 3000, contours))
# for i, cnt in enumerate(fil_contours):
#     # ?????????????????????????????????
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
# # ??????
# showImage = copy.copy(img)
# for detectedRectangle in detectedRectangles:
#     p1 = (detectedRectangle[0], detectedRectangle[1])
#     p2 = (p1[0] + detectedRectangle[2], p1[1] + detectedRectangle[3])
#     cv2.rectangle(showImage, p1, p2, (0, 0, 255), 2)
# cv2.imshow("????????????", showImage)
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
