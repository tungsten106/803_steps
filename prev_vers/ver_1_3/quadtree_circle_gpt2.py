import tkinter as tk
import random
import math

class QuadTreeVisualizer:
    def __init__(self, width, height, stack_depth):
        self.width = width
        self.height = height
        self.stack_depth = stack_depth
        self.max_rect_size = max(width, height)
        self.min_rect_size = self.max_rect_size / (2 ** stack_depth)
        self.pos_x = random.uniform(0, self.width)
        self.pos_y = random.uniform(0, self.height)
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
        # 控制 variation 的速度
        self.variation += 0.004

    def draw(self, canvas):
        self.quad_tree(canvas, self.width / 2, self.height / 2, self.max_rect_size)

    def quad_tree(self, canvas, x, y, size):
        canvas.create_oval(x, y, x + 1, y + 1, outline="white")
        if size < self.min_rect_size:
            return

        if self.dist_to_circle_boundary(x, y) < size / 2:
            canvas.create_rectangle(x - size / 2, y - size / 2,
                                    x + size / 2, y + size / 2,
                                    outline="white")
        else:
            size /= 2
            d = size / 2
            self.quad_tree(canvas, x + d, y + d, size)
            self.quad_tree(canvas, x + d, y - d, size)
            self.quad_tree(canvas, x - d, y + d, size)
            self.quad_tree(canvas, x - d, y - d, size)

    def dist_to_circle_boundary(self, x, y):
        center = (self.width / 2, self.height / 2)
        radius = min(self.width, self.height) / 4
        return abs(((x - center[0]) ** 2 + (y - center[1]) ** 2) ** 0.5 - radius)

# 使用示例
if __name__ == "__main__":
    visualizer = QuadTreeVisualizer(800, 600, 7)
    visualizer.run()
