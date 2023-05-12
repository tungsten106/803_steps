import numpy as np
import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image

def color_inv(img):
    h, w = img.shape
    imgInv = np.empty((h, w), np.uint8)  # 创建空白数组
    for i in range(h):
        for j in range(w):
            imgInv[i][j] = 255 - img[i][j]
    return imgInv
def dilate2(img, size):
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            xlim1 = max(x-size, 0)
            xlim2 = min(x+size+1, img.shape[0])
            ylim1 = max(y-size,0)
            ylim2 = min(y+size+1, img.shape[1])
            avg = np.mean(img[xlim1:xlim2, ylim1:ylim2])

            if avg > 128:
                img[x][y] = 225
            else:
                img[x][y] = 0
    return img

def dilate_img(event):
    global dilated_image, image, dilation_size
    # dilation_size = 1
    while "<Button-1>":
        print("botton pressed")
        dilation_size -= 1
        dilated_image = dilate2(dilated_image, dilation_size)
        dilated_image_pil = Image.fromarray(dilated_image)
        dilated_image_tk = ImageTk.PhotoImage(image=dilated_image_pil)
        label.configure(image=dilated_image_tk)
        label.image = dilated_image_tk
        window.update()

def open_image():
    global dilated_image, image, dilation_size
    dilation_size = 3
    # 打开文件选择对话框以选择图像
    # file_path = filedialog.askopenfilename()
    # 逍遥游3个字
    file_path = "/xiaoyaoyou.jpeg"
    # 全图
    # file_path = "/Users/yexl_uk/PycharmProjects/pythonProject/calligraphy.JPG"
    # 读取图像文件
    image = cv2.imread(file_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = color_inv(image)
    dilated_image = image.copy()
    # dilate_image = dilate2(image, 2)
    # 将图像转换为PIL Image格式
    image_pil = Image.fromarray(dilated_image)
    # 将PIL Image转换为Tkinter Image格式
    image_tk = ImageTk.PhotoImage(image=image_pil)
    # 更新标签上的图像
    label.configure(image=image_tk)
    label.image = image_tk
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
label.bind("<Button-1>", dilate_img)
# label.bind('<ButtonRelease-1>', erode_image)
# label.bind("<Button-1>", erode_image)

window.mainloop()
