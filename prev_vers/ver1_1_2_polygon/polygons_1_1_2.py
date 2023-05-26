import numpy as np
import math


class Polygon_112:
    """
    Polygon class represents a polygon with its vertices.

    Attributes:
        vertices (list): A list of (x, y) tuples representing the vertices of the polygon.

    Methods:
        is_in_poly(pos2): Check if a point is inside the polygon.
    """

    def __init__(self, n=5, size=50, center=(0, 0),
                 angles=None,
                 distances=None, dist_range=None):
        self.n = n
        self.size = size
        self.center = center

        # 如果没有初始值，随机生成
        if angles is not None:
            self.angles = angles
        else:
            self.angles = np.random.uniform(0, 2 * math.pi, self.n)
        self.angles = np.array(sorted(self.angles))
        if dist_range is not None:
            self.dist_range = dist_range
        else:
            self.dist_range = (5, size)
        if distances is not None:
            self.distances = distances
        else:
            self.distances = np.random.uniform(self.dist_range[0],
                                               self.dist_range[1],
                                               self.n)

        # 根据输入/生成的angles和diatnces 生成顶点坐标
        self.vertices = self.create()

    def create(self):
        # print(self.distances.shape, self.angles.shape)
        c1, c2 = self.center
        vertices = []
        for i in range(self.n):
            x = int(c1 + self.distances[i] * math.sin(self.angles[i]))
            y = int(c2 + self.distances[i] * math.cos(self.angles[i]))
            vertices.append((x, y))
        return vertices

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

    # functions for "update" polygons
    def update_polygon(self, new_size):
        new_dist = self.distances * new_size / self.size
        new_range = (self.dist_range[0], new_size)

        return Polygon_112(n=self.n,
                           size=new_size, center=self.center,
                           angles=self.angles,
                           distances=new_dist,
                           dist_range=new_range)

    def moved_vertices(self, dx, dy):
        new_vertices = self.vertices.copy()
        # print(np.array(new_vertices).shape)
        for i in range(self.n):
            # print(new_vertices[i])
            # new_vertices[i] += [dx, dy]
            x, y = new_vertices[i]
            new_vertices[i] = (x+dx, y+dy)

            # print("new vertices: ", new_vertices[i])
        return new_vertices

# examples
# polygon1 = Polygon_112(8, size=50)
# polygon2 = polygon1.update_polygon(new_size=25)
# print(polygon1.distances)
# print(polygon2.vertices)
# print(polygon2.dist_range)
