# 初期化

import pyautogui

import re
import os
import subprocess
import sys
import time
import array

import win32api
import win32gui
import win32con

import glob
from PIL import Image
import cv2


# windowを見つけて選択状態にする
def findWindow(window_name="logres_andapp"):
    parent_handle = win32gui.FindWindow(None, window_name)
    win_x1, win_y1, win_x2, win_y2 = win32gui.GetClientRect(parent_handle)
    print(u"アプリの座標:" + str(win_x1) + "/" + str(win_y1))
    apw_x = win_x2 - win_x1
    apw_y = win_y2 - win_y1
    print(u"アプリの画面サイズ:" + str(apw_x) + "/" + str(apw_y))
    win32gui.SetForegroundWindow(parent_handle)

    Screen.parent_handle = parent_handle
    Screen.region = (win_x1, win_y1, apw_x, apw_y)
    # # ステータス部分を省いた範囲
    # status = 0.0810
    # Screen.regionWithoutStatus = (win_x1, win_y1+int(status*apw_y), apw_x, apw_y-int(status*apw_y))
    Screen.center = pyautogui.center(Screen.region)
    Screen.w = apw_x
    Screen.h = apw_y

    resizeImages()


def resizeImages():
    imageDic = "images/"
    images = glob.glob('images/*.bmp')
    resizedDic = "resizedImages/"
    myWidth = 486
    myHeight = 864
    for imName in images:
        img = Image.open(imName)
        img_w, img_h = img.width * (Screen.w / myWidth), img.height * (Screen.h / myHeight)
        img_resize = img.resize((int(img_w), int(img_h)), Image.LANCZOS)
        # if imName[len(imageDic):] == "lv.bmp":
        #     img.save(resizedDic + imName[len(imageDic):])
        #     continue
        img_resize.save(resizedDic + imName[len(imageDic):])

    # 2値画像用
    imageDic = "glayImages/"
    images = glob.glob(imageDic + "*.bmp")
    resizedDic = "resizedImages/"
    myWidth = 486
    myHeight = 864
    for imName in images:
        img = cv2.imread(imName, 0)
        img_resize = cv2.resize(img, dsize=None, fx=(Screen.w / myWidth), fy=(Screen.h / myHeight))
        imgBin = cv2.inRange(img_resize, 1, 255)
        cv2.imwrite(resizedDic + imName[len(imageDic):], imgBin)


class Screen:
    parent_handle = None
    region = None
    # regionWithoutStatus = None
    center = None
    w = None
    h = None
