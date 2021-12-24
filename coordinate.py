from setup import *
import imgrecg


def coordinateToPixelRelative(x, y):
    return int(x * (Screen.w / appWindow.w)), int(y * (Screen.h / appWindow.h))


def coordinateToPixelAbs(x, y):
    x, y = coordinateToPixelRelative(x, y)
    x, y = imgrecg.convToAbs(x, y)
    return x, y


def AbsPixelToCoordinate(x, y):
    x, y = imgrecg.convAbsToRel(x, y)
    return int(x * (appWindow.w / Screen.w)), int(y * (appWindow.h / Screen.h))


def RelPixelToCoordinate(x, y):
    return int(x * (appWindow.w / Screen.w)), int(y * (appWindow.h / Screen.h))


# (x1, y1, x2, y2)を(x, y, w, h)に変換
def convToRegion(x1, y1, x2, y2):
    x = x1
    y = y1
    w = x2 - x1
    h = y2 - y1
    region = (x, y, w, h)
    return region


class appWindow:
    def __init__(self):
        self.w = 500
        self.h = 900
        self.region = (0, 0, self.w, self.h)
        self.center = (int(self.w / 2), int(self.h / 2))
        self.regionWithoutStatus = (0, 73, self.w, self.h - 73)


appWindow = appWindow()