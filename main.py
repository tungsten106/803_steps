import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image

def erode_image(event):
    global eroded_image, dilated_image
    # 根据鼠标按压时间计算膨胀迭代次数
    # iterations = int(event.time / 10)
    # 创建一个腐蚀核
    k_size = 3
    kernel = np.ones((k_size, k_size), np.uint8)
    kernel_2 = np.ones((5, 5), np.uint8)
    # 逐渐腐蚀图像
    j = 4
    i = 1
    while True:
        if j >= 0:
            eroded_image = cv2.dilate(image, kernel_2, iterations=j)
            j -= 1
        else:
        # for i in range(1, iterations+1):
            i += 1
            eroded_image = cv2.erode(image, kernel, iterations=i)
        # 将腐蚀后的图像转换为PIL Image格式
        eroded_image_pil = Image.fromarray(eroded_image)
        # 将PIL Image转换为Tkinter Image格式
        eroded_image_tk = ImageTk.PhotoImage(image=eroded_image_pil)
        # 更新标签上的图像
        label.configure(image=eroded_image_tk)
        label.image = eroded_image_tk
        # 更新窗口
        window.update()

def dilate_image(event):
    global dilated_image, image, dilate_index
    # 根据鼠标按压时间计算膨胀迭代次数
    # i = max(0, 50-int(event.time / 10))
    i = 20
    dilate_index = -1
    # 创建一个腐蚀核
    k_size = 6
    kernel = np.ones((k_size, k_size), np.uint8)
    # 逐渐腐蚀图像
    # for i in range(iterations, 0, -1):
    while True:
        if i > 0:
            dilated_image = cv2.erode(image, kernel, iterations=i)
        else:
            dilate_index += 1
            dilate_index = min(dilate_index, 4)
            dilated_image = cv2.dilate(image, kernel, iterations=dilate_index)
        # 将腐蚀后的图像转换为PIL Image格式
        dilated_image_pil = Image.fromarray(dilated_image)
        # 将PIL Image转换为Tkinter Image格式
        dilated_image_tk = ImageTk.PhotoImage(image=dilated_image_pil)
        # 更新标签上的图像
        label.configure(image=dilated_image_tk)
        label.image = dilated_image_tk
        # 更新窗口
        window.update()
        # i = max(0, 50-int(event.time / 1000))
        i -= 1

def color_inv(img):
    h, w = img.shape
    imgInv = np.empty((h, w), np.uint8)  # 创建空白数组
    for i in range(h):
        for j in range(w):
            imgInv[i][j] = 255 - img[i][j]
    return imgInv
# ————————————————
# 版权声明：本文为CSDN博主「youcans_」的原创文章，遵循CC
# 4.0
# BY - SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https: // blog.csdn.net / youcans / article / details / 121453961

def open_image():
    global eroded_image, dilated_image, image
    # 打开文件选择对话框以选择图像
    # file_path = filedialog.askopenfilename()
    # 逍遥游3个字
    file_path = "/Users/yexl_uk/PycharmProjects/pythonProject/xiaoyaoyou.jpeg"
    # 全图
    # file_path = "/Users/yexl_uk/PycharmProjects/pythonProject/calligraphy.JPG"
    # 读取图像文件
    image = cv2.imread(file_path)

    # original_shape = image.shaoe
    # 将图像转换为灰度图像
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # print(image.shape)
    image = color_inv(image)
    # 保存原始图像副本
    eroded_image = image.copy()
    dilated_image = image.copy()
    # 将图像转换为PIL Image格式
    image_pil = Image.fromarray(image)
    # 将PIL Image转换为Tkinter Image格式
    image_tk = ImageTk.PhotoImage(image=image_pil)
    # 更新标签上的图像
    label.configure(image=image_tk)
    label.image = image_tk

    # 创建背景
    initial_image = np.zeros(image.shape, dtype=np.uint8)
    # 将图像转换为PIL Image格式
    initial_image_pil = Image.fromarray(initial_image)
    # 将PIL Image转换为Tkinter Image格式
    initial_image_tk = ImageTk.PhotoImage(image=initial_image_pil)
    # 更新标签上的图像
    label.configure(image=initial_image_tk)
    label.image = initial_image_tk
    window.update()


# 创建Tkinter窗口
window = tk.Tk()

# 创建一个标签来显示图像
label = tk.Label(window)
label.pack()

# 创建打开图像按钮
open_button = tk.Button(window, text="开始！", command=open_image)
open_button.pack()

# 设置腐蚀迭代次数
# iterations = 10

# 绑定鼠标点击事件
label.bind("<Button-1>", dilate_image)
label.bind('<ButtonRelease-1>', erode_image)
# label.bind("<Button-1>", erode_image)

window.mainloop()
