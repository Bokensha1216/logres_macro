from ursina import *
import ui
import numpy as np
import win32gui

from setup import *
from wrapping import *
from coordinate import *


# 相対座標取得
def getCoordinate():
    x, y = pyautogui.position()
    x, y = win32gui.ScreenToClient(Screen.parent_handle, (x, y))

    return x, y


# 割合座標取得
def getRatio():
    x, y = getCoordinate()
    return x / Screen.w, y / Screen.h


# 絶対座標取得
def getAbsCoordinate():
    x, y = pyautogui.position()

    return x, y


def getColor():
    x, y = pyautogui.position()
    region = (x, y, 1, 1)
    image = pyautogui.screenshot(region=region)
    return image.getpixel((0, 0))


# 仮想座標取得
def getVirtualCoordinate():
    x, y = getCoordinate()
    return RelPixelToCoordinate(x, y)


# 距離ベクトル取得
def distance(A, B):
    A = np.array(A)
    B = np.array(B)
    vec = B - A
    return vec


if __name__ == "__main__":
    findWindow()

    app = Ursina()
    window.size = (240*1.5, 160*1.5)
    window.borderless = False

    scale = (2.5, 2.5)
    offset = 0.5
    posY = -0.15
    coordinate = ui.MyText(text="", position=(0, offset + posY), scale=scale)
    absCoordinate = ui.MyText(text="", position=(0, offset + posY * 2), scale=scale)
    color = ui.MyText(text="", position=(0, offset + posY * 3), scale=scale)
    ratio = ui.MyText(text="", position=(0, offset + posY * 4), scale=scale)
    distanceVec = ui.MyText(text="", position=(0, offset + posY * 5), scale=scale)
    virtualCoordinate = ui.MyText(text="", position=(0, offset + posY * 6), scale=scale)


    def update():
        # global d
        x, y = getCoordinate()
        coordinate.text = f"({str(x)}, {str(y)})"

        x, y = getAbsCoordinate()
        absCoordinate.text = f"({str(x)}, {str(y)})"

        pixelRgb = getColor()
        color.text = str(pixelRgb)
        # color.color = rgb(pixelRgb[0], pixelRgb[1], pixelRgb[2])

        x, y = getRatio()
        ratio.text = "({:.4f}, ".format(x) + "{:.4f})".format(y)

        distanceVec.text = distanceVecText

        x, y = getVirtualCoordinate()
        virtualCoordinate.text = f"virtual ({str(x)}, {str(y)})"


    vec1 = None
    vec2 = None
    distanceVecText = ""
    count = 0
    def input(key):
        global vec1, vec2, count, distanceVecText
        if key == 'space':
            count += 1

            if count==1:
                vec1 = (getVirtualCoordinate())
                x = vec1[0]
                y = vec1[1]
                distanceVecText = f"({str(x)}, {str(y)})"
            if count==2:
                vec2 = (getVirtualCoordinate())
                x = vec2[0]
                y = vec2[1]
                distanceVecText = f"({str(x)}, {str(y)}) - " + distanceVecText
                vec = distance(vec1, vec2)
                distanceVecText += f" = {vec}"
            if count==3:
                count=0
                distanceVecText = ""


    app.run()
