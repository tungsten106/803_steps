import tkinter as tk
import random
import math
import noise
import numpy as np

class QuadTreeVisualizer:
    def __init__(self, width, height, stack_depth):
        self.width = width
        self.height = height
        self.stack_depth = stack_depth
        self.max_rect_size = max(width, height)
        self.min_rect_size = self.max_rect_size / (2 ** stack_depth)
        self.pos_x = random.uniform(0, self.width)
        self.pos_y = random.uniform(0, self.height)
        # self.pos_x = 100
        # self.pos_y = 100
        self.variation = 0

    def run(self):
        self.variation = 0.0

        root = tk.Tk()
        root.title("QuadTree Visualizer")
        canvas = tk.Canvas(root, width=self.width, height=self.height, bg="black")
        canvas.pack()

        while True:
            self.update()
            canvas.delete("all")
            self.draw(canvas)
            root.update()

    def update(self):
        # control variation speed
        self.variation += 0.01

    def draw(self, canvas):
        self.quad_tree(canvas, self.width / 2, self.height / 2, self.max_rect_size)

    def quad_tree(self, canvas, x, y, size):
        a = np.array([x, y])
        b = np.array([100, 200])
        if (self.eucliDist(a, b)) <= 50:
            return
        # if np.linalg.norm(np.array(x, y) , np.array(100,100)) < 50:
        # if abs(self.dist_to_center(x, y)) < 50:
        #     # canvas.create_rectangle(x - size / 2, y - size / 2,
        #     #                         x + size / 2, y + size / 2,
        #     #                         outline="white")
        #     return
        if size < self.min_rect_size:
            return

        n = noise.snoise3((math.sin(x) + self.pos_x) * 0.001,
                          (math.cos(y) + self.pos_y) * 0.001, 0.001)
        if abs(n - 0.2) > (size / self.max_rect_size):
            canvas.create_rectangle(x - size / 2, y - size / 2,
                                    x + size / 2, y + size / 2,
                                    outline="white")
        # if self.dist_to_circle_boundary(x, y) < size:
        #     canvas.create_rectangle(x - size / 2, y - size / 2,
        #                             x + size / 2, y + size / 2,
        #                             outline="white")
        else:
            size /= 2
            d = size / 2
            self.quad_tree(canvas, x + d, y + d, size)
            self.quad_tree(canvas, x + d, y - d, size)
            self.quad_tree(canvas, x - d, y + d, size)
            self.quad_tree(canvas, x - d, y - d, size)

    # def noise(self, x, y, variation):
    #     return math.sin(x * 0.1) * math.cos(y * 0.1) + math.sin((x + y) * 0.05) * variation

    def eucliDist(self, A, B):
        return np.sqrt(sum(np.power((A - B), 2)))
    def dist_to_center(self, x, y):
        center = (100, 200)
        radius = 50
        return ((x - center[0]) ** 2 + (y - center[1]) ** 2)**0.5

    # def is_in_circle(self, x, y):
    #     center = (100, 100)
    #     radius = 50
    #     return abs(((x - center[0]) ** 2 + (y - center[1]) ** 2) ** 0.5 - radius) < 0.01


# 使用示例
if __name__ == "__main__":
    visualizer = QuadTreeVisualizer(800, 600, 7)
    visualizer.run()
