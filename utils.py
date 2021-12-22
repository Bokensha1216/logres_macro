from ursina import *
import ui

from setup import *


# 相対座標表示
def getCoordinate():
    x, y = pyautogui.position()
    x = x - Screen.region[0]
    y = y - Screen.region[1]

    return x, y


# 絶対座標表示
def getAbsCoordinate():
    x, y = pyautogui.position()

    return x, y


def getColor():
    x, y = pyautogui.position()
    region = (x, y, 1, 1)
    image = pyautogui.screenshot(region=region)
    return image.getpixel((0, 0))


if __name__ == "__main__":
    findWindow()

    app = Ursina()
    window.size = (140, 80)
    window.borderless = False

    coordinate = ui.MyText(text="", position=(0, 0.25), scale=(10, 10))
    absCoordinate = ui.MyText(text="", position=(0, 0), scale=(10, 10))
    color = ui.MyText(text="", position=(0, -0.25), scale=(10, 10))


    def update():
        x, y = getCoordinate()
        coordinate.text = f"({str(x)}, {str(y)})"

        x, y = getAbsCoordinate()
        absCoordinate.text = f"({str(x)}, {str(y)})"

        pixelRgb = getColor()
        color.text = str(pixelRgb)
        # color.color = rgb(pixelRgb[0], pixelRgb[1], pixelRgb[2])


    app.run()
