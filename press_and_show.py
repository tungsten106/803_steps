import tkinter as tk
import cv2
from PIL import ImageTk, Image

from utils import *

# 创建主窗口
window = tk.Tk()
window.title("Image Revealer")
window.configure(bg="black")

# 加载图片
image_path = "calligraphy.JPG"  # 替换为你的图片路径
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像
print(image.shape)
image = color_inv(image)

# 设置画布大小
canvas_width = image.shape[0]
canvas_height = image.shape[1]
# 将图像转换为PIL Image格式
image_pil = Image.fromarray(image)
# 将PIL Image转换为Tkinter Image格式
photo = ImageTk.PhotoImage(image=image_pil)

# 创建画布
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="black")
canvas.pack()

# parameters
sq_size = 50
mouse_pressed = False

def mousePressed(event):
    global mouse_pressed
    if not mouse_pressed:
        draw(event)
        mouse_pressed = True

def draw(event):
    # 获取鼠标点击位置
    # 计算要显示的图像位置和大小
    x = max(0, event.x - sq_size//2)
    y = max(0, event.y - sq_size//2)
    width = min(sq_size, canvas_width-x)
    height = min(sq_size, canvas_width-y)
    sub_image = image_pil.crop((x, y, x + width, y + height))
    sub_photo = ImageTk.PhotoImage(sub_image)

    # 在画布上显示方块和图像
    canvas.create_image(x, y, anchor=tk.NW, image=sub_photo, tags="revealed_image")

    # 保留对sub_photo的引用
    canvas.sub_photo = sub_photo

def hide_image(event):
    global mouse_pressed
    if mouse_pressed:
        canvas.delete("revealed_image")
        mouse_pressed = False


# 绑定鼠标点击事件
canvas.bind("<Button-1>", mousePressed)
canvas.bind("<ButtonRelease-1>", hide_image)

# 运行主循环
window.mainloop()
