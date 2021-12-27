import cv2
import numpy as np


def pil2cv(image):
    ''' PIL型 -> OpenCV型 '''
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image


# image 対象画像, template 検知したい画像名, lower upper 下限上限 2値化に使う, threshold 検知精度 show 検知結果を表示するか
def detectTemplate(image, template, lower, upper, threshold, show=False):
    # openCV型に変換
    img = pil2cv(image)
    # 2値化
    imgBin = cv2.inRange(img, lower, upper)
    # 検知画像読込
    templateImg = cv2.imread(template, 0)
    # 検知
    res = cv2.matchTemplate(imgBin, templateImg, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    # 検知結果を表示
    if show is True:
        h, w = templateImg.shape
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        cv2.imshow(template, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    # (x, y)のリストに加工して返す
    itemList = []
    for pt in zip(*loc[::-1]):
        itemList.append((pt[0], pt[1]))
    return itemList



