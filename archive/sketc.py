from tkinter import Tk, Canvas
from PIL import Image, ImageTk
from datetime import datetime
import numpy as np


root = Tk()
canvas_width = 400
canvas_height = 400
brush_size = 10
start_time = None

# 加载背景图片
background_image = Image.open("../xiaoyaoyou.jpeg")
background_image = background_image.resize((canvas_width, canvas_height))
background_image_tk = ImageTk.PhotoImage(background_image)

# 创建画布
canvas = Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

def on_mouse_press(event):
    global start_time
    # start_time = datetime.now()

def on_mouse_release(event):
    global start_time
    if start_time is not None:
        elapsed_time = datetime.now() - start_time
        brush_size = int(elapsed_time.total_seconds() * 10)  # 根据按压时长计算brush size
        start_time = None
        draw_image(event.x, event.y, brush_size)

# def draw_image(x, y, size):
#     new_image = background_image.copy()
#     pixels = new_image.load()
#
#     frame_size = 50
#     for i in range(-frame_size, frame_size+1):
#         for j in range(-frame_size, frame_size+1):
#             xlim1 = max(x-size, 0)
#             xlim2 = min(x+size+1, pixels.shape[0])
#             ylim1 = max(y-size,0)
#             ylim2 = min(y+size+1, pixels.shape[1])
#             avg = np.mean(pixels[xlim1:xlim2][ylim1:ylim2])
#
#             if avg > 128:
#                 pixels[x][y] = 225
#             else:
#                 pixels[x][y] = 0
#
#
#     # 显示处理后的图像
#     new_image_tk = ImageTk.PhotoImage(new_image)
#     canvas.create_image(0, 0, anchor="nw", image=new_image_tk)
#     canvas.image = new_image_tk
def draw_image(x, y, brush_size):
    new_image = background_image.copy()
    pixels = new_image.load()

    # 膨胀处理
    for dy in range(-brush_size, brush_size + 1):
        for dx in range(-brush_size, brush_size + 1):
            nx = x + dx
            ny = y + dy
            if nx >= 0 and nx < canvas_width and ny >= 0 and ny < canvas_height:
                pixels[nx, ny] = (255, 255, 255)  # 设置指定区域的像素为白色

    # 显示处理后的图像
    new_image_tk = ImageTk.PhotoImage(new_image)
    canvas.create_image(0, 0, anchor="nw", image=new_image_tk)
    canvas.image = new_image_tk


# 绑定鼠标按下和释放事件
canvas.bind("<Button-1>", on_mouse_press)
canvas.bind("<ButtonRelease-1>", on_mouse_release)

# 显示初始背景图片
canvas.create_image(0, 0, anchor="nw", image=background_image_tk)
canvas.image = background_image_tk

root.mainloop()
