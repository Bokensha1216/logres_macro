import queue

from setup import *
import win32gui


def coordinateToPixelRelative(x, y):
    return int(x * (Screen.w / appWindow.w)), int(y * (Screen.h / appWindow.h))


def coordinateToPixelAbs(x, y):
    x, y = coordinateToPixelRelative(x, y)
    x, y = win32gui.ClientToScreen(Screen.parent_handle, (x, y))
    return x, y


def AbsPixelToCoordinate(x, y):
    x, y = win32gui.ScreenToClient(Screen.parent_handle, (x, y))
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


def RegionCenter(region):
    x = int(region[0] + region[2] / 2)
    y = int(region[1] + region[3] / 2)
    center = (x, y)
    return center


def convAreaToScreen(area):
    s_area = Screen.w * Screen.h
    v_area = appWindow.w * appWindow.h
    return area * (s_area / v_area)


def convAreaToVirtual(area):
    s_area = Screen.w * Screen.h
    v_area = appWindow.w * appWindow.h
    return area * (v_area / s_area)


class appWindow:
    def __init__(self):
        self.w = 500
        self.h = 900
        self.region = (0, 0, self.w, self.h)
        self.center = (int(self.w / 2), int(self.h / 2))
        self.Status_y = 53
        self.regionWithoutStatus = (0, self.Status_y, self.w, self.h - self.Status_y)
        self.eventQueue = queue.Queue()
        self.observer = None


appWindow = appWindow()
