import cv2
import numpy as np
import tkinter as tk
from PIL import ImageTk, Image

def erode_image(event):
    # 在鼠标点击位置创建一个腐蚀核
    kernel = np.ones((5, 5), np.uint8)
    # 对图像进行腐蚀处理
    global eroded_image
    eroded_image = cv2.erode(frame, kernel, iterations=1)
    # 将腐蚀后的图像转换为PIL Image格式
    eroded_image_pil = Image.fromarray(eroded_image)
    # 将PIL Image转换为Tkinter Image格式
    eroded_image_tk = ImageTk.PhotoImage(image=eroded_image_pil)
    # 更新标签上的图像
    label.configure(image=eroded_image_tk)
    label.image = eroded_image_tk

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("无法打开摄像头")
    exit()

ret, frame = cap.read()
eroded_image = frame.copy()

# 创建Tkinter窗口
window = tk.Tk()

# 创建一个标签来显示图像
label = tk.Label(window)
label.pack()

# 将OpenCV图像转换为PIL Image格式
image_pil = Image.fromarray(frame)

# 将PIL Image转换为Tkinter Image格式
image_tk = ImageTk.PhotoImage(image=image_pil)

# 在标签上显示图像
label.configure(image=image_tk)
label.image = image_tk

# 绑定鼠标点击事件
label.bind("<Button-1>", erode_image)

window.mainloop()

# 释放摄像头
cap.release()
