import time

import cv2
import numpy
import numpy as np

from imageProcessing import *
import matplotlib.pyplot as plt
import threading
from exception import *
from questData import *


# class Recoder(threading.Thread):
#     def __init__(self):
#         super().__init__()
#
#         self.imageQueue = queue.Queue()
#         self.eventQueue = queue.Queue()
#         self.START = 1
#         self.STOP = 0
#
#     def run(self):
#         try:
#             self.record()
#         except FinishButtonException:
#             print("finish recorder")
#
#     def record(self):
#         while True:
#             event = self.eventQueue.get()
#             if isinstance(event, FinishButtonException):
#                 raise event
#             else:
#                 if event == self.START:
#                     if self.hasEvent():
#                         break
#
#                     region = (0, 0, 500, 900)
#                     offset = (0, 0)
#                     fps = 10.0
#                     for i in range(50):
#                         img = screenshot(region)
#                         while self.imageQueue.qsize() >= 50:
#                             time.sleep(1 / fps)
#                         self.imageQueue.put(img)
#                         time.sleep(1 / fps)
#
#                 if event == self.STOP:
#                     pass
#
#     def hasEvent(self):
#         if self.eventQueue.qsize() != 0:
#             return True
#         else:
#             return False

class Recoder:
    def __init__(self, fps=10.0):
        self.fps = fps

    def record(self, frames, region=(0, 0, 500, 900)):
        images = []
        # offset = (0, 0)
        for i in range(frames):
            img = screenshot(region)
            images.append(img)
            time.sleep(1 / self.fps)

        return images


def showHist(img, isColor=False):
    def average(hist):
        wSum = 0
        for i, h in enumerate(hist):
            wSum += h * i

        return wSum / sum(hist)

    img = pil2cv(img)
    n_bins = 256  # ビンの数
    hist_range = [0, 256]  # 集計範囲

    if isColor is False:
        hist = cv2.calcHist(
            [img], channels=[0], mask=None, histSize=[n_bins], ranges=hist_range
        )
        ave = average(hist)
        print(ave)
        plt.plot(hist)
        plt.show()
    else:
        channels = {0: "blue", 1: "green", 2: "red"}
        hists = []
        for ch in channels:
            hist = cv2.calcHist(
                [img], channels=[ch], mask=None, histSize=[n_bins], ranges=hist_range
            )
            ave = np.average(hist[:-2])
            print(channels[ch], ave)
            print(len(hist))
            hist = hist.squeeze(axis=-1)
            hists.append(hist)

        # 描画する。
        def plot_hist(bins, hist, color):
            centers = (bins[:-1] + bins[1:]) / 2
            widths = np.diff(bins)
            ax.bar(centers, hist, width=widths, color=color)

        bins = np.linspace(*hist_range, n_bins + 1)

        fig, ax = plt.subplots()
        ax.set_xticks([0, 256])
        ax.set_xlim([0, 256])
        ax.set_xlabel("Pixel Value")
        for hist, color in zip(hists, channels.values()):
            plot_hist(bins, hist, color=color)
        plt.show()


def getHistAverage(img):
    def average(hist):
        wSum = 0
        for i, h in enumerate(hist):
            wSum += h * i

        return wSum / sum(hist)

    n_bins = 256  # ビンの数
    hist_range = [0, 256]  # 集計範囲

    hist = cv2.calcHist(
        [img], channels=[0], mask=None, histSize=[n_bins], ranges=hist_range
    )
    ave = average(hist)
    return ave


def kakou(img, edgePrm=(550, 300)):
    prmMin = edgePrm[0]
    prmMax = edgePrm[1]
    img = pil2cv(img)
    # img = cv2.medianBlur(img,3)
    # cv2.imshow("blur", img)
    edges = detectEdge(img, prmMin=prmMin, prmMax=prmMax, toCV2=False)
    kernel = np.ones((2, 2), np.uint8)
    dilation = cv2.dilate(edges, kernel, iterations=2)
    # cv2.imshow("dil", dilation)
    # kernel = np.ones((2, 2), np.uint8)
    # ero = cv2.erode(dilation, kernel, iterations=3)

    return dilation

    # cv2.imshow("edge", edges)
    # # cv2.imshow("ero", ero)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


def movement(images, step=1, OR=False):
    diffs = []
    moveImages = []
    for i, img in enumerate(images):
        if i < step:
            continue
        img_present = kakou(img)
        img_past = kakou(images[i - step])
        img_diff1 = cv2.absdiff(img_present, img_past)
        diffs.append(img_diff1)
        if len(diffs) <= step:
            continue
        if OR is False:
            movImage = cv2.bitwise_and(diffs[-1], diffs[-2])
        else:
            movImage = cv2.bitwise_or(diffs[-1], diffs[-2])
        moveImages.append(movImage)

        # cv2.imshow("imgpre", img_present)
        # cv2.imshow("imgpast", img_past)
        # # cv2.imshow("imgdif1", diffs[-1])
        # # cv2.imshow("imgdif2", diffs[-2])
        # cv2.imshow("movement", movImage)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    return moveImages


# frame:何フレーム前まで求めるか 0だと全部
def MoveSum(moveImages, frame=0):
    if frame > 0 or frame < len(moveImages):
        moveImages = moveImages[-frame:]

    moveSum = moveImages[0]
    for i in range(1, len(moveImages)):
        moveSum = cv2.bitwise_or(moveImages[i], moveSum)

    return moveSum


def makeVideo(images, fileName, fps):
    # images = [pil2cv(img) for img in images]
    image_h, image_w, _ = images[0].shape[:3]
    print(image_w, image_h)
    codec = cv2.VideoWriter_fourcc(*'H264')
    video = cv2.VideoWriter(fileName, codec, fps, (image_w, image_h))

    for img in images:
        # img = cv2.resize(img, dsize=(image_w, image_h))
        # cv2.imshow("tes", img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        video.write(img)

    video.release()


def detectMovingObject(moveSum, areaMin, areaMax, showArea=False, dilK=3, dilL=2, offset=()):
    kernel = np.ones((dilK, dilK), np.uint8)
    dilation = cv2.dilate(moveSum, kernel, iterations=dilL)

    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if showArea:
        cv2.imshow("dil", dilation)
        for cnt in contours:
            area = convAreaToVirtual(cv2.contourArea(cnt))
            print(area)
    contours = list(filter(lambda x: areaMax >= convAreaToVirtual(cv2.contourArea(x)) >= areaMin, contours))
    recs = ContoursToVirtualRectangles(contours, offset)
    return recs


def detectFromStillImage(img, areaMin, areaMax, external=True, edgePrm=(550, 300)):
    img = kakou(img, edgePrm)
    mode = cv2.RETR_EXTERNAL if external else cv2.RETR_LIST
    contours, hierarchy = cv2.findContours(img, mode, cv2.CHAIN_APPROX_SIMPLE)
    areaMin, areaMax = areaMin, areaMax
    contours = list(filter(lambda x: areaMax >= convAreaToVirtual(cv2.contourArea(x)) >= areaMin, contours))
    return contours


def makeVideoImages(images, moveImages, moveFrame):
    videoImages = []
    for i in range(moveFrame - 1, len(images)):
        moveSum = MoveSum(moveImages[:i], frame=moveFrame)
        # cv2.imshow("movesum", moveSum)
        areaMin, areaMax = 2000, 70000
        recs = detectMovingObject(moveSum, areaMin, areaMax)
        img = drawOnImage(images[i], recs, show=False)
        videoImages.append(img)
    return videoImages


def getEnemy(recs):
    def sigmoid(x):
        sigmoid_range = 34.538776394910684
        return 1.0 / (1.0 + np.exp(-np.clip(x, -sigmoid_range, sigmoid_range)))

    hyouka = {}
    for rec in recs:
        hyouka[rec] = []

        # 位置
        center_x = RegionCenter(rec)[0]
        center_x = (center_x - 250) / 50
        h = sigmoid(center_x)
        hyouka[rec].append(h)

    return hyouka

    # # 面積
    # area = rec[2]*rec[3]
    # area = -(area/5 - 2000)/200
    # h = sigmoid(area)
    # hyouka[rec].append(h)


def main():
    findWindow()

    region = (0, 90, 500, 620)
    offset = (0, 90)
    # images = []
    # fps = 10.0

    img = screenshot(region=region)
    cnts = detectFromStillImage(img, 1000, 70000)
    # showContours(img, cnts)
    recs = ContoursToVirtualRectangles(cnts, offset=offset)
    drawOnImage(img, recs, offset=offset)

    hyouka = getEnemy(recs)
    print(hyouka)

    # cv2.imshow("rec", moveSum)

    # cv2.imshow("rec", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # videoImages = makeVideoImages(images, moveImages, 10)
    # fileName = "ImgVideo.mp4"
    # makeVideo(videoImages, fileName, fps)


if __name__ == "__main__":
    main()
