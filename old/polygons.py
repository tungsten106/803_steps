import math
import numpy as np

import math
import random
import tkinter as tk


class Polygon:
    """
    Polygon class represents a polygon with its vertices.

    Attributes:
        vertices (list): A list of (x, y) tuples representing the vertices of the polygon.

    Methods:
        is_in_polygon(pos2): Check if a point is inside the polygon.
    """

    def __init__(self, n=5, size=50, center=(0,0)):
        self.n = n
        self.size = size
        self.center = center
        self.vertices = self.create()
        # self.fix_vertex_order()

    def create(self):
        vertices = []
        c1, c2 = self.center

        # angle = 2 * math.pi / self.n  # 计算每个顶点之间的角度差
        angles = np.random.uniform(0, 2 * math.pi, self.n)
        # angles = [i * 2 * math.pi//self.n for i in range(self.n)]
        angles = sorted(angles)
        # print("angles are: ", angles)

        for i in range(self.n):
            # 生成随机的到圆心的距离
            # distance = random.uniform(0, self.size)
            # distance = min(self.size//2, distance)
            # 生成到圆心的距离
            distance = self.size//2

            x = int(c1 + distance * math.sin(angles[i]))
            y = int(c2 + distance * math.cos(angles[i]))
            # print((x, y), distance, angles[i])
            vertices.append((x, y))

        # vertices = self.fix_vertex_order(vertices)
        # print("vertices are: ", vertices)
        return vertices

    # def fix_vertex_order(self, vertices):
    #     # 计算多边形的有向面积
    #     def signed_area(x1, y1, x2, y2):
    #         return (x1 * y2 - x2 * y1) / 2
    #
    #     # 检查多边形的有向面积，如果是顺时针方向则反转顶点顺序
    #     area = sum(signed_area(x1, y1, x2, y2) for (x1, y1), (x2, y2)
    #                in zip(vertices, vertices[1:] + [vertices[0]]))
    #     if area < 0:
    #         vertices = list(reversed(vertices))
    #     return vertices

    def is_in_polygon(self, point):
        x, y = point
        num_vertices = len(self.vertices)

        # 使用射线法判断点是否在多边形内部
        inside = False
        j = num_vertices - 1

        for i in range(num_vertices):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[j]

            if ((y1 > y) != (y2 > y)) and (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1):
                inside = not inside

            j = i

        return inside

    def is_in_poly(self, p):
        """
        :param p: [x, y]
        :param poly: [[], [], [], [], ...]
        :return:
        """
        poly = self.vertices
        px, py = p
        is_in = False
        for i, corner in enumerate(poly):
            next_i = i + 1 if i + 1 < len(poly) else 0
            x1, y1 = corner
            x2, y2 = poly[next_i]
            if (x1 == px and y1 == py) or (x2 == px and y2 == py):  # if point is on vertex
                is_in = True
                break
            if min(y1, y2) < py <= max(y1, y2):  # find horizontal edges of polygon
                x = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
                if x == px:  # if point is on edge
                    is_in = True
                    break
                elif x > px:  # if point is on left-side of line
                    is_in = not is_in
        return is_in



# examples

