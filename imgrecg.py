from PIL import Image, ImageDraw
import numpy as np
from setup import *


def screenshot():
    image = pyautogui.screenshot(region=Screen.region)

    return image


# 相対座標を入れる
def getPixel(x, y):
    image = screenshot()
    return image.getpixel((x, y))


def locateAll(image, confidence=0.65):
    items = pyautogui.locateAllOnScreen(image, region=Screen.region, grayscale=True, confidence=confidence)
    return items


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
    image = screenshot()
    draw = ImageDraw.Draw(image)
    for item in items:
        itemCoor = convert(item)
        print(itemCoor)
        draw.rectangle(itemCoor, fill=(255, 255, 0))
    image.save('output/locatedItems.png', quality=95)


# 要素が(x, y)
def drawLocatedItems2(items):
    image = screenshot()
    draw = ImageDraw.Draw(image)
    for item in items:
        item = (item[0], item[1], 10, 10)
        itemCoor = convert(item)
        print(itemCoor)
        draw.rectangle(itemCoor, fill=(255, 255, 0))
    image.save('output/locatedItems.png', quality=95)


# 相対座標に変換かつ(x,y,w,h) から (x1,y1,x2,y2)に変換
def convert(box):
    x1 = box[0] - Screen.region[0]
    y1 = box[1] - Screen.region[1]
    x2 = x1 + box[2]
    y2 = y1 + box[3]

    boxConv = (x1, y1, x2, y2)
    return boxConv


# 相対座標(x1, y1, x2, y2)を絶対座標(x, y, w, h)に変換
def convToRegion(x1, y1, x2, y2):
    x = x1 + Screen.region[0]
    y = y1 + Screen.region[1]
    w = x2 - x1
    h = y2 - y1
    region = (x, y, w, h)
    return region


# 絶対座標に変換
def convToAbs(x, y):
    xAbs = x + Screen.region[0]
    yAbs = y + Screen.region[1]

    return xAbs, yAbs


# AからBへの向かう単位ベクトルを返す AとBは(x, y)
def direction_vec(A, B):
    A = np.array(A)
    B = np.array(B)
    vec = (B - A) / np.linalg.norm(B - A, ord=2)
    return vec
