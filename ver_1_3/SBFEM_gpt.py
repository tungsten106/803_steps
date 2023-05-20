import numpy as np
import matplotlib.pyplot as plt

def draw_polygon(vertices):
    # 绘制多边形
    polygon = plt.Polygon(vertices, closed=True, color='white')
    plt.gca().add_patch(polygon)

def color_difference(image, rect):
    # 计算矩形内最大和最小颜色强度之间的差异
    region = image[rect[0][0]:rect[1][0], rect[0][1]:rect[1][1]]
    return np.max(region) - np.min(region)

def subdivide_rectangle(rect):
    # 将矩形细分为四个子矩形
    x_center = (rect[0][0] + rect[1][0]) // 2
    y_center = (rect[0][1] + rect[1][1]) // 2
    sub_rects = [
        [(rect[0][0], rect[0][1]), (x_center, y_center)],
        [(x_center, rect[0][1]), (rect[1][0], y_center)],
        [(rect[0][0], y_center), (x_center, rect[1][1])],
        [(x_center, y_center), (rect[1][0], rect[1][1])]
    ]
    return sub_rects

def draw_outline_with_quadtree(image, rect, color_threshold):
    # 如果矩形内的颜色差异大于颜色阈值，则细分矩形并继续绘制轮廓
    if color_difference(image, rect) > color_threshold:
        sub_rects = subdivide_rectangle(rect)
        for sub_rect in sub_rects:
            draw_outline_with_quadtree(image, sub_rect, color_threshold)
    else:
        # 绘制矩形轮廓
        draw_rectangle(rect)

def draw_rectangle(rect):
    # 绘制矩形
    x = [rect[0][0], rect[1][0], rect[1][0], rect[0][0], rect[0][0]]
    y = [rect[0][1], rect[0][1], rect[1][1], rect[1][1], rect[0][1]]
    plt.plot(x, y, color='black')

# 创建黑底画布
image_size = 100
image = np.zeros((image_size, image_size))

# 定义多边形顶点坐标
vertices = [(30, 20), (70, 10), (60, 40), (50, 60), (20, 50)]

# 绘制多边形
draw_polygon(vertices)

# 设置绘图区域
plt.axis([0, image_size, 0, image_size])

# 绘制轮廓
draw_outline_with_quadtree(image, [[0, 0], [image_size, image_size]], color_threshold=10)

# 显示图形
plt.show()
