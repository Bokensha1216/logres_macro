from PIL import Image, ImageDraw
import numpy as np
from setup import *
import wrapping
import win32gui


# def screenshot():
#     image = pyautogui.screenshot(region=Screen.region)
#
#     return image


# # 相対座標を入れる
# def getPixel(x, y):
#     image = screenshot()
#     return image.getpixel((x, y))


# # 割合座標を入れる
# def getPixelRatio(x, y):
#     x, y = convRatioToRelative(x, y)
#     return getPixel(x, y)


# def locateAll(image, confidence=0.65):
#     items = pyautogui.locateAllOnScreen(image, region=Screen.region, grayscale=True, confidence=confidence)
#     return items


# def locatePixel(r=None, g=None, b=None):
#     image = screenshot()
#     if r is not None:
#         for y in range(Screen.region[3]):
#             for x in range(Screen.region[2]):
#                 pixel = image.getpixel((x, y))
#                 if pixel[0] == r:
#                     return x, y
#
#     if g is not None:
#         for y in range(Screen.region[3]):
#             for x in range(Screen.region[2]):
#                 pixel = image.getpixel(x, y)
#                 if pixel[1] == g:
#                     return x, y
#
#     if b is not None:
#         for y in range(Screen.region[3]):
#             for x in range(Screen.region[2]):
#                 pixel = image.getpixel(x, y)
#                 if pixel[2] == b:
#                     return x, y


# 要素が(x, y, w, h)
def drawLocatedItems(items):
    image = wrapping.screenshot()
    draw = ImageDraw.Draw(image)
    for item in items:
        itemCoor = convert(wrapping.RegionToPixel(item))
        print(itemCoor)
        draw.rectangle(itemCoor, fill=(255, 255, 0))
    image.save('output/locatedItems.png', quality=95)


# 要素が(x, y)
def drawLocatedItems2(items):
    image = wrapping.screenshot()
    draw = ImageDraw.Draw(image)
    for item in items:
        item = (item[0], item[1], 10, 10)
        itemCoor = convert(item)
        print(itemCoor)
        draw.rectangle(itemCoor, fill=(255, 255, 0))
    image.save('output/locatedItems.png', quality=95)


# 相対座標に変換かつ(x,y,w,h) から (x1,y1,x2,y2)に変換
def convert(box):
    x, y, w, h = wrapping.RegionToPixel(box)
    x2, y2 = x+w, y+h
    x1, y1 = win32gui.ScreenToClient(Screen.parent_handle, (x, y))
    x2, y2 = win32gui.ScreenToClient(Screen.parent_handle, (x2, y2))

    boxConv = (x1, y1, x2, y2)
    return boxConv


# 相対座標を絶対座標に変換
def convToAbs(x, y):
    xAbs = x + Screen.region[0]
    yAbs = y + Screen.region[1]

    return xAbs, yAbs


# 割合座標を絶対座標に変換
def convRatioToAbs(x, y):
    x, y = convRatioToRelative(x, y)
    return convToAbs(x, y)


# 相対座標を割合座標に変換
def convToRatio(x, y):
    x = x / Screen.w
    y = y / Screen.h

    return x, y


# 割合座標を相対座標に変換
def convRatioToRelative(x, y):
    x = int(x * Screen.w)
    y = int(y * Screen.h)
    return x, y


def convAbsToRel(x, y):
    xAbs = x - Screen.region[0]
    yAbs = y - Screen.region[1]
    return xAbs, yAbs


# AからBへの向かう単位ベクトルを返す AとBは(x, y)
def direction_vec(A, B):
    A = np.array(A)
    B = np.array(B)
    vec = (B - A) / np.linalg.norm(B - A, ord=2)
    return vec

def totalRGB(rgb):
    return rgb[0] + rgb[1] + rgb[2]