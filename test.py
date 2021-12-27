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

img = screenshot(region=appWindow.regionWithoutStatus)
template = "images/lv.bmp"
low, upper = (95, 40, 0), (255, 255, 10)
threshold = 0.5
ls = detectTemplate(img, template, low, upper, threshold, show=True)
print(ls)
