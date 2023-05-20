import numpy as np
import matplotlib.pyplot as plt

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

def insert_polygon(polygon, quadtree):
    for i in range(len(polygon)):
        p1 = polygon[i]
        p2 = polygon[(i+1) % len(polygon)]
        quadtree.insert_segment(p1, p2)

def display_quadtree(quadtree, ax):
    if quadtree.children is None:
        rect = plt.Rectangle((quadtree.boundary.x, quadtree.boundary.y),
                             quadtree.boundary.w, quadtree.boundary.h,
                             fill=False)
        ax.add_patch(rect)
    else:
        for child in quadtree.children:
            display_quadtree(child, ax)

# 创建多边形
polygon = [Point(0, 0), Point(10, 0), Point(10, 10), Point(5, 15), Point(0, 10)]

# 设置QuadTree的范围
boundary = Rectangle(-1, -1, 12, 17)

# 创建QuadTree
class QuadTree:
    def __init__(self, boundary):
        self.boundary = boundary
        self.children = None

    def insert_segment(self, p1, p2):
        if not self.boundary_contains_segment(p1, p2):
            return

        if self.children is None:
            self.subdivide()

        for child in self.children:
            child.insert_segment(p1, p2)

    def boundary_contains_segment(self, p1, p2):
        return (
            self.boundary_contains_point(p1) or
            self.boundary_contains_point(p2) or
            self.intersects_boundary(p1, p2)
        )

    def boundary_contains_point(self, point):
        return (
            self.boundary.x <= point.x <= self.boundary.x + self.boundary.w and
            self.boundary.y <= point.y <= self.boundary.y + self.boundary.h
        )

    def intersects_boundary(self, p1, p2):
        x1, y1, x2, y2 = self.boundary.x, self.boundary.y, self.boundary.x + self.boundary.w, self.boundary.y + self.boundary.h
        return (
            self._do_segments_intersect(p1.x, p1.y, p2.x, p2.y, x1, y1, x2, y1) or
            self._do_segments_intersect(p1.x, p1.y, p2.x, p2.y, x2, y1, x2, y2) or
            self._do_segments_intersect(p1.x, p1.y, p2.x, p2.y, x2, y2, x1, y2) or
            self._do_segments_intersect(p1.x, p1.y, p2.x, p2.y, x1, y2, x1, y1)
        )

    def _do_segments_intersect(self, x1, y1, x2, y2, x3, y3, x4, y4):
        den = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
        if den == 0:
            return False

        ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / den
        ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / den

        return 0 <= ua <= 1 and 0 <= ub <= 1

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w / 2
        h = self.boundary.h / 2

        self.children = [
            QuadTree(Rectangle(x, y, w, h)),
            QuadTree(Rectangle(x + w, y, w, h)),
            QuadTree(Rectangle(x, y + h, w, h)),
            QuadTree(Rectangle(x + w, y + h, w, h))
        ]

# 创建并插入多边形到QuadTree中
quadtree = QuadTree(boundary)
insert_polygon(polygon, quadtree)

# 绘制QuadTree和多边形
fig, ax = plt.subplots()
display_quadtree(quadtree, ax)

x = [point.x for point in polygon]
y = [point.y for point in polygon]
plt.plot(x + [x[0]], y + [y[0]], 'r-')

plt.xlim(-1, 11)
plt.ylim(-1, 18)
plt.gca().set_aspect('equal')
plt.show()
