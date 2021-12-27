import pyautogui

import imgrecg
from setup import *
from wrapping import *
from imageProcessing import *
import cv2

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

img = cv2.imread(template, 0)
dst = cv2.resize(img, dsize=None, fx=2, fy=2)
imgBin = cv2.inRange(dst, 1, 255)
cv2.imshow(template, imgBin)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite("resizedImages/lv.bmp", imgBin)
cv2.imwrite("resizedImages/lv.bmp", dst)

img = screenshot(region=appWindow.regionWithoutStatus)
low, upper = (95, 40, 0), (255, 255, 10)
showBitImage(img, low, upper)
