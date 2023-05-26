import cv2
from PIL import Image

from old.polygons import *

def crop_polygon(image):
    # 创建黑色背景图像
    mask = np.zeros(image.shape[:2], dtype=np.uint8)

    polygon = Polygon(8, int(image.shape[0]), (int(image.shape[1]//2),
                                          int(image.shape[0]//2)))

    # 使用多边形坐标绘制填充区域
    cv2.fillPoly(mask, [np.array(polygon.vertices)], 255)

    # 将掩码应用于图像
    masked_image = cv2.bitwise_and(image, image, mask=mask)

    # 将Numpy数组转换为PIL图像
    cropped_image = Image.fromarray(masked_image)

    return cropped_image

# 加载图像
image = Image.open("../../pics/calligraphy.JPG")

# x = max(0, mouse_x - sq_size // 2)
# y = max(0, mouse_y - sq_size // 2)
# width = min(sq_size, canvas_width - x)
# height = min(sq_size, canvas_width - y)
# sub_image = image.crop((0, 0, 400, 400))
# sub_image = np.array(sub_image)

# 定义多边形坐标
# vertices = np.array([(100, 100), (200, 50), (300, 150), (250, 250), (150, 200)])
# print(vertices.dtype)
# polygon = Polygon(6, 50, (500, 500))
# print(polygon.vertices)
# vertices = np.array(polygon.vertices)
# print(vertices.shape)
# 裁剪多边形
print(np.array(image).shape)
cropped_image = crop_polygon(np.array(image))

# 显示裁剪后的图像
cropped_image.show()
