import cv2
import numpy as np

def dilate2(img, size, threshold=128):
    """
    dilate algo from chatgpt
    :param img: ndarray image to dilate
    :param size: size of block around each pixels to compute average
    :param threshold: default=128, avg>threshold then white
    :return: dilated image
    """
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            xlim1 = max(x-size, 0)
            xlim2 = min(x+size+1, img.shape[0])
            ylim1 = max(y-size,0)
            ylim2 = min(y+size+1, img.shape[1])
            avg = np.mean(img[xlim1:xlim2, ylim1:ylim2])

            if avg > threshold:
                img[x][y] = 225
            else:
                img[x][y] = 0
    return img


def color_inv(img):
    """
    实现图像的反色（255-x）
    :param img: 要反色的图片
    :return: 反色后的图片
    """
    h, w = img.shape
    imgInv = np.empty((h, w), np.uint8)  # 创建空白数组
    for i in range(h):
        for j in range(w):
            imgInv[i][j] = 255 - img[i][j]
    return imgInv
    # ————————————————
    # 版权声明：本文为CSDN博主「youcans_」的原创文章，遵循CC
    # 4.0
    # BY - SA版权协议，转载请附上原文出处链接及本声明。
    # 原文链接：https: // blog.csdn.net / youcans / article / details / 121453961