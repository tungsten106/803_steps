# from quad_tree_csdn import *
from PIL import Image, ImageTk
import numpy as np
import cv2


# def get_screenshot(canvas):
#     # 获取Canvas的信息
#     file_name = "tmp"
#     canvas.postscript(file=file_name + '.eps')
#     image = Image.open(file_name + '.eps')
#
#     # 显示PIL图像
#     # image.show()
#     return image
#
# def get_screenshot_1(window, canvas):
#     # 获取Canvas的屏幕坐标
#     x = window.winfo_rootx() + canvas.winfo_x()
#     y = window.winfo_rooty() + canvas.winfo_y()
#     width = canvas.winfo_width()
#     height = canvas.winfo_height()
#
#     # 从屏幕中截取Canvas的部分
#     screenshot = ImageGrab.grab((x, y, x + width, y + height))
#
#     # 将截图转换为NumPy数组
#     # return np.array(screenshot)
#     return screenshot
def crop_polygon(image, polygon):
    # 创建黑色背景图像
    mask = np.zeros(image.shape[:2], dtype=np.uint8)

    # polygon = Polygon_112(n=poly_n, int(image.shape[0]), (int(image.shape[1]//2),
    #                                       int(image.shape[0]//2)))
    # 使用多边形坐标绘制填充区域
    cv2.fillPoly(mask, [np.array(polygon.vertices, dtype=np.int32)], 255)

    # 将掩码应用于图像
    masked_image = cv2.bitwise_and(image, image, mask=mask)

    # 将Numpy数组转换为PIL图像
    # cropped_image = Image.fromarray(masked_image)
    cropped_image = masked_image

    return cropped_image


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
            xlim1 = max(x - size, 0)
            xlim2 = min(x + size + 1, img.shape[0])
            ylim1 = max(y - size, 0)
            ylim2 = min(y + size + 1, img.shape[1])
            avg = np.mean(img[xlim1:xlim2, ylim1:ylim2])

            if avg > threshold:
                img[x][y] = 255
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
