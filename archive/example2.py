import cv2
import numpy as np
import tkinter as tk
from PIL import ImageTk, Image

def color_inv(img):
    h, w = img.shape
    imgInv = np.empty((h, w), np.uint8)  # 创建空白数组
    for i in range(h):
        for j in range(w):
            imgInv[i][j] = 255 - img[i][j]
    return imgInv
def dilate_image(event):
    global dilated_image, initial_image

    # 计算膨胀迭代次数，根据鼠标按压的坐标位置
    iterations = int(event.x / 10)

    # 创建膨胀核
    kernel = np.ones((5, 5), np.uint8)

    # 逐渐膨胀图像
    for i in range(iterations):
        dilated_image = cv2.dilate(dilated_image, kernel, iterations=1)

    # 将膨胀后的图像转换为PIL Image格式
    dilated_image_pil = Image.fromarray(dilated_image)

    # 将PIL Image转换为Tkinter Image格式
    dilated_image_tk = ImageTk.PhotoImage(image=dilated_image_pil)

    # 更新标签上的图像
    label.configure(image=dilated_image_tk)
    label.image = dilated_image_tk

def open_image():
    global dilated_image, initial_image

    # 打开文件选择对话框以选择图像
    # file_path = filedialog.askopenfilename()
    file_path = "/xiaoyaoyou.jpeg"

    # 读取图像文件
    image = cv2.imread(file_path)

    # 将图像转换为灰度图像
    initial_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    initial_image = color_inv(initial_image)

    # 保存初始图像副本
    dilated_image = initial_image.copy()

    # 将图像转换为PIL Image格式
    initial_image_pil = Image.fromarray(initial_image)

    # 将PIL Image转换为Tkinter Image格式
    initial_image_tk = ImageTk.PhotoImage(image=initial_image_pil)

    # 更新标签上的图像
    label.configure(image=initial_image_tk)
    label.image = initial_image_tk

# 创建Tkinter窗口
window = tk.Tk()

# 创建一个标签来显示图像
label = tk.Label(window)
label.pack()

# 创建打开图像按钮
open_button = tk.Button(window, text="打开图像", command=open_image)
open_button.pack()

# 绑定鼠标按压事件
label.bind("<B1-Motion>", dilate_image)

window.mainloop()
