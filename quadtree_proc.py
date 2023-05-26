import tkinter as tk
import random
import math
import noise


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
        self.variation += 0.003

    def draw(self, canvas):
        self.quad_tree(canvas, self.width / 2, self.height / 2, self.max_rect_size)

    def quad_tree(self, canvas, x, y, size):
        if size < self.min_rect_size:
            return
        # n = self.noise((x + self.pos_x) * 0.001, (y + self.pos_y) * 0.001, self.variation)
        # print(x, y, self.dist_to_center(x, y))
        # n = noise.pnoise3((x + self.pos_x) * 0.004, (y + self.pos_y) * 0.004, self.variation)
        n = noise.snoise3((x + self.pos_x) * 0.001, (y + self.pos_y) * 0.001, self.variation)
        # if abs(n - 0.2) > (size / self.max_rect_size):
        c = size // 2
        if ((abs(x-c*n)-300)**2+(abs(y-c*n)-400)**2)**0.5 <= 100:
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

# 使用示例
if __name__ == "__main__":
    visualizer = QuadTreeVisualizer(800, 600, 7)
    visualizer.run()