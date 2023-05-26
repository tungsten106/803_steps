import tkinter as tk
from PIL import Image, ImageTk

import tkinter as tk
import random
import math
import noise
import cv2
from utils import *


class QuadTreeVisualizer:
    def __init__(self, width, height, stack_depth, image_path):
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
        self.image = Image.open(image_path)
        self.image = self.image.resize((self.width, self.height))  # 转换成画布大小
        self.image = np.array(self.image)
        # self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像
        self.image = color_inv(self.image)

    def run(self):
        self.variation = 0.0

        root = tk.Tk()
        root.title("QuadTree Visualizer")
        canvas = tk.Canvas(root, width=self.width, height=self.height, bg="black")
        canvas.pack()
        # print(self.image)

        while True:
            self.update()
            canvas.delete("all")
            self.draw(canvas)
            root.update()

    def update(self):
        # control variation speed
        self.variation += 0.004

    def draw(self, canvas):
        photo = ImageTk.PhotoImage(image=Image.fromarray(self.image))
        # canvas.create_image(0,0, anchor=tk.NW, image=photo, tags="step_803")
        self.quad_tree(canvas, self.width / 2, self.height / 2, self.max_rect_size)
        # self.quad_tree(canvas, 200, 200, self.max_rect_size)

    def quad_tree(self, canvas, x, y, size):
        if size < self.min_rect_size:
            return

        def clamp_number(num, a=0, b=self.height):
            return max(min(num, b), a)

        n = noise.snoise3((x + self.pos_x) * 0.001, (y + self.pos_y) * 0.001, self.variation)
        # x_, y_ = clamp_number(x,b=self.width), clamp_number(y,b=self.height)
        x_, y_ = int(min(x, self.width-1)), int(min(y, self.height-1))
        if abs(n - 0.2) >= (size / self.max_rect_size) and self.image[x_][y_] > 0:
            canvas.create_rectangle(x - size / 2, y - size / 2,
                                    x + size / 2, y + size / 2,
                                    outline="white")

        # c = size / 2
        # print(x, y)
        # n = noise.snoise3((x + self.pos_x) * 0.001, (y + self.pos_y) * 0.001, self.variation)
        # def is_in_circle(x, y):
        #     return (150 <=(((x + c * n - 300) ** 2 + (y + c * n - 400) ** 2)) ** 0.5 <= 200)
        #
        # if sum([is_in_circle(x - c, y - c), is_in_circle(x - c, y + c), is_in_circle(x + c, y - c),
        #         is_in_circle(x + c, y + c)]) == 3:
        #     # if ((((x+c-300) ** 2 + (y+c-400) ** 2)) ** 0.5 > 200) and ((((x-c-300) ** 2 + (y-c-400) ** 2)) ** 0.5 > 200):
        #     canvas.create_rectangle(x - size / 2, y - size / 2,
        #                             x + size / 2, y + size / 2,
        #                             outline="white")
        # if ((((x) ** 2 + (y) ** 2)) ** 0.5 > 600):
        #     canvas.create_rectangle(x - size / 2, y - size / 2,
        #                                 x + size / 2, y + size / 2,
        #                                 outline="white")

        else:
            size /= 2
            d = size / 2
            self.quad_tree(canvas, x + d, y + d, size)
            self.quad_tree(canvas, x + d, y - d, size)
            self.quad_tree(canvas, x - d, y + d, size)
            self.quad_tree(canvas, x - d, y - d, size)



# 加载图片
image_path = "../pics/xiaoyaoyou.bmp"  # 替换为你的图片路径
visualizer = QuadTreeVisualizer(800, 800, 7, image_path)
visualizer.run()
