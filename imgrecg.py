from PIL import Image, ImageDraw
import numpy as np
from setup import *
import wrapping
import win32gui
from imageProcessing import *


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


# AからBへの向かう単位ベクトルを返す AとBは(x, y)
def direction_vec(A, B):
    A = np.array(A)
    B = np.array(B)
    vec = (B - A) / np.linalg.norm(B - A, ord=2)
    return vec


def totalRGB(rgb):
    return rgb[0] + rgb[1] + rgb[2]


def drawVecOnImage(img, A, B, offset=(0, 0)):
    img = pil2cv(img)
    A = coordinateToPixelRelative(*A)
    B = coordinateToPixelRelative(*B)
    cv2.arrowedLine(img, (A[0] + offset[0], A[1] + offset[1]), (B[0] + offset[0], B[1] + offset[1]), (0, 255, 0), thickness=4)
    cv2.imshow("vec", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
