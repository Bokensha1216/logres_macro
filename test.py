import numpy as np
import pyautogui

import imgrecg
from setup import *
from wrapping import *
from imageProcessing import *
import cv2
import copy

findWindow()
# imageName = "images/wolflv.bmp"
# img = cv2.imread(imageName, 0)
# img = screenshot().convert("L")

# img = screenshot(region=appWindow.regionWithoutStatus)
template = "images/lv.bmp"
# low, upper = (95, 40, 0), (255, 255, 10)
# threshold = 0.5
# ls = detectTemplate(img, template, low, upper, threshold, show=True)
# print(ls)

# img = cv2.imread(template, 0)
# dst = cv2.resize(img, dsize=None, fx=2, fy=2)
# imgBin = cv2.inRange(dst, 1, 255)
# cv2.imshow(template, imgBin)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cv2.imwrite("resizedImages/lv.bmp", imgBin)
# cv2.imwrite("resizedImages/lv.bmp", dst)

img = screenshot(region=appWindow.regionWithoutStatus)
img2 = screenshot()
low, upper = (95, 70, 0), (255, 255, 5)
offset = (0, appWindow.Status_y)
ret = ContourRectangle(img, low, upper, show=False, offset=offset)
drawOnImage(img2, ret)
# imgBin = showBitImage(img, low, upper)
#
# kernel = np.ones((8, 8), np.uint8)
# # kernel = np.array([
# #     [1,1,1],
# #     [1,1,1],
# #     [1,1,1]], np.uint8
# # )
# dilation = cv2.dilate(imgBin, kernel, iterations=2)
# cv2.imshow("bit", dilation)

# kernel = np.array([
#     [0,1,0],
#     [0,1,0],
#     [0,1,0]], np.uint8
# )
# dilation = cv2.dilate(imgBin, kernel, iterations=1)
# cv2.imshow("bit2", dilation)

# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# img = pil2cv(img)
# img2 = copy.copy(img)
# contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# for label in contours:
#     label = [i[0] for i in label]
#     all_x = [i[0] for i in label]
#     all_y = [i[1] for i in label]
#     p1 = (min(all_x), min(all_y))
#     p2 = (max(all_x), max(all_y))
#     cv2.rectangle(img, p1, p2, (0, 0, 255), 2)

# for label in contours:
#     retval = cv2.boundingRect(label)
#     print(retval)
#     p1 = (retval[0], retval[1])
#     p2 = (p1[0] + retval[2], p1[1] + retval[3])
#     cv2.rectangle(img, p1, p2, (0, 0, 255), 2)

# cv2.imshow("rec", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# retval_filtered = []
# for label in contours:
#     retval = cv2.boundingRect(label)
#     center = (int(retval[0] + retval[2]/2), int(retval[1] + retval[3]/2))
#     cv2.circle(img, center, 5, (0, 0, 255), -1)
#
#     if center[1] < 127 - appWindow.Status_y:
#         continue
#     if center[0] < 64 and center[1] < 237 - appWindow.Status_y:
#         continue
#     if center[1] > 734:
#         continue
#
#     retval_filtered.append(retval)
# cv2.imshow("rec", img)
#
# for retval in retval_filtered:
#     p1 = (retval[0], retval[1])
#     p2 = (p1[0] + retval[2], p1[1] + retval[3])
#     cv2.rectangle(img2, p1, p2, (0, 0, 255), 2)
#
# cv2.imshow("rec2", img2)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


