# import tkinter as tk
# import io
# from PIL import Image, ImageTk
# import numpy as np
#
# # 创建窗口和Canvas
# window = tk.Tk()
# canvas = tk.Canvas(window, width=500, height=500)
# canvas.pack()
#
# # 在Canvas上绘制一些内容
# canvas.create_rectangle(50, 50, 200, 200, fill='red')
# canvas.create_oval(250, 250, 400, 400, fill='blue')
# canvas.create_text(100, 300, text='Hello, World!', fill='black')
#
# # 获取Canvas的信息
# ps_data = canvas.postscript(colormode='color')
#
# # 将PostScript数据转换为PIL图像
# image = Image.open(io.BytesIO(ps_data.encode('utf-8')))
#
# # 将PIL图像转换为NumPy数组
# np_array = np.array(image)
#
# # 打印NumPy数组的形状
# print(np_array.shape)
#
# # 显示PIL图像
# image.show()
#
# # 运行Tkinter主循环
# window.mainloop()
# from PIL import ImageGrab, Image
#
# image = Image.open('tmp.eps')
# image.show()


import tkinter as tk
import cv2
from PIL import Image, ImageTk

from utils import *
# 创建主窗口
window = tk.Tk()
window.title("Image Revealer")
window.configure(bg="black")
window.geometry("974x1768")
# window.attributes('-fullscreen', True)

# 加载图片
image_path = "pics/calligraphy.JPG"  # 替换为你的图片路径
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像
image = color_inv(image)

# 设置画布大小
canvas_width = image.shape[0]
canvas_height = image.shape[1]
print(canvas_width, canvas_height)
# 将图像转换为PIL Image格式
image_pil = Image.fromarray(image)
# 将PIL Image转换为Tkinter Image格式
photo = ImageTk.PhotoImage(image=image_pil)
image_pil.show()

# 创建画布
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="black")
canvas.pack()

canvas.create_image(0, 0, anchor=tk.NW, image=photo, tags="photo")

# 运行主循环
window.mainloop()
