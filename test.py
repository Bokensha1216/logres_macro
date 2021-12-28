import numpy as np
import pyautogui

from setup import *
from wrapping import *
from imageProcessing import *
import cv2
import copy
from macros import *

findWindow()

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
