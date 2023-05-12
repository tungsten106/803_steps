import cv2
import numpy as np




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