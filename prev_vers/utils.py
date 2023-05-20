import cv2
from polygons_1_1_2 import *


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

# def crop_polygon(image, polygon):
#     # 创建黑色背景图像
#     mask = np.zeros(image.shape, dtype=np.uint8)
#     polygon = np.array(polygon, dtype=np.int32)
#
#     # 使用多边形坐标绘制填充区域
#     cv2.fillPoly(mask, [polygon], 255)
#
#     # 将掩码应用于图像
#     masked_image = cv2.bitwise_and(image, image, mask=mask)
#
#     # 将Numpy数组转换为PIL图像
#     # cropped_image = Image.fromarray(masked_image)
#     cropped_image = masked_image
#
#     return cropped_image

def dilate_polygon(img, size, threshold=128, polygon=None):
    """
    dilate algo from chatgpt, but provide a polygon.
    :param img: ndarray image to dilate
    :param size: size of block around each pixels to compute average
    :param threshold: default=128, avg>threshold then white
    :return: dilated image
    """
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            # justify if (x, y) in polygon
            if not polygon.is_in_poly(p=(x, y)):
                img[x][y] = 0
                continue
            xlim1 = max(x - size, 0)
            xlim2 = min(x + size + 1, img.shape[0])
            ylim1 = max(y - size, 0)
            ylim2 = min(y + size + 1, img.shape[1])
            avg = np.mean(img[xlim1:xlim2, ylim1:ylim2])

            if avg > threshold:
                img[x][y] = 225
            else:
                img[x][y] = 0
    return img


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
