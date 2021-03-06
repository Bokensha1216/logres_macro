from coordinate import *


def click(x, y, interval=None):
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    if x > appWindow.w:
        x = appWindow.w
    if y > appWindow.h:
        y = appWindow.h

    x, y = coordinateToPixelAbs(x, y)
    if interval is None:
        pyautogui.click(x, y)
    else:
        pyautogui.mouseDown(x=x, y=y)
        time.sleep(interval)
        pyautogui.mouseUp()


def locateOnScreen(imageName, region, **kwargs):
    region = RegionToPixel(region)
    locatedItem = pyautogui.locateOnScreen(imageName, region=region, **kwargs)
    try:
        return RegionPixelToCoordinate(locatedItem)
    except TypeError:
        return None


def RegionToPixel(region):
    x, y = coordinateToPixelAbs(region[0], region[1])
    w, h = coordinateToPixelRelative(region[2], region[3])
    region = (x, y, w, h)
    return region


def RegionPixelToCoordinate(region):
    x, y = AbsPixelToCoordinate(region[0], region[1])
    w, h = RelPixelToCoordinate(region[2], region[3])
    region = (x, y, w, h)
    return region


def RegionClientToCoordinate(region):
    x, y = RelPixelToCoordinate(region[0], region[1])
    w, h = RelPixelToCoordinate(region[2], region[3])
    region = (x, y, w, h)
    return region


def RegionCoordinateToClient(region):
    x, y = coordinateToPixelRelative(region[0], region[1])
    w, h = coordinateToPixelRelative(region[2], region[3])
    region = (x, y, w, h)
    return region


def locateCenterOnScreen(imageName, region, **kwargs):
    region = RegionToPixel(region)
    locatedItem = pyautogui.locateCenterOnScreen(imageName, region=region, **kwargs)
    try:
        return AbsPixelToCoordinate(locatedItem[0], locatedItem[1])
    except TypeError:
        return None


def locateAllOnScreen(imageName, region, **kwargs):
    region = RegionToPixel(region)
    locatedItems = pyautogui.locateAllOnScreen(imageName, region=region, **kwargs)
    itemList = []
    for item in locatedItems:
        itemList.append(RegionPixelToCoordinate(item))
    return itemList


def screenshot(region=appWindow.region):
    region = RegionToPixel(region)
    image = pyautogui.screenshot(region=region)

    return image


def getPixel(x, y):
    x, y = coordinateToPixelRelative(x, y)
    image = screenshot()
    return image.getpixel((x, y))
