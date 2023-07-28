# from quad_tree_csdn import *
from PIL import Image, ImageTk
import numpy as np
import cv2

# input_points = np.float32([[1500, 1500], [-985, 1300],
#                            [-1231, 2300], [1700, 2300]])
# input_points = np.float32([[1550,1340],
#                            [-850,1250],
#                            [-1030,2260],
#                            [1600,2300]])
input_points = np.float32([[1136,1147],
                           [-1227,1250],
                           [-1345,2400],
                           [1300,2430]])

output_points = np.float32([[0, 0], [1917-1, 0], [1917-1, 1080-1], [0, 1080-1]])


def mapping_position(x, y):
    transform_matrix = cv2.getPerspectiveTransform(input_points, output_points)
    input_coordinates = np.float32([[x, y]])
    output_coord = cv2.perspectiveTransform(input_coordinates.reshape(-1, 1, 2), transform_matrix)
    return output_coord[0][0]


def check_loc_domain(last_coord):
    x, y= last_coord
    is_in_domain = cv2.pointPolygonTest(input_points,
                                        (x, y), False)
    return is_in_domain > 0

def check_loc_range(cur_coord):
    x, y = cur_coord
    is_in_range =cv2.pointPolygonTest(output_points,
                                      (x, y), False)
    return is_in_range > 0




def crop_polygon(image, polygon):
    # 创建黑色背景图像
    mask = np.zeros(image.shape, dtype=np.uint8)

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


def dilate3(img, size, threshold=128, step=3):
    """
    dilate algo from chatgpt
    :param img: ndarray image to dilate
    :param size: size of block around each pixels to compute average
    :param threshold: default=128, avg>threshold then white
    :return: dilated image
    """
    for x in range(0, img.shape[0], step):
        for y in range(0, img.shape[1], step):
            xlim1 = max(x + step // 2 - size, 0)
            xlim2 = min(x + step // 2 + size + 1, img.shape[0])
            ylim1 = max(y + step // 2 - size, 0)
            ylim2 = min(y + step // 2 + size + 1, img.shape[1])
            avg = np.mean(img[xlim1:xlim2, ylim1:ylim2])

            if avg > threshold:
                img[x:x + step, y:y + step] = 255
            else:
                img[x:x + step, y:y + step] = 0
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
