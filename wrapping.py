from coordinate import *


def click(x, y):
    x, y = coordinateToPixelAbs(x, y)
    pyautogui.click(x, y)


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


def locateCenterOnScreen(imageName, region, **kwargs):
    region = RegionToPixel(region)
    locatedItem = pyautogui.locateCenterOnScreen(imageName, region=region,**kwargs)
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
