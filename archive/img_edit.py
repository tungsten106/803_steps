import tkinter as tk
import os
from PIL import Image, ImageTk
import cv2 as cv
from tkinter import filedialog
import numpy as np
from functools import partial
from tools import *


# 下面的是为了直方图均衡化
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk, FigureCanvasTkAgg


# 打开，保存，退出，转灰度
# 几何变换：镜像，平移，剪切，旋转，缩放
# 空间滤波：平滑处理，锐化处理

# 直方图，计算，显示，均衡化
# 频域变换：Fourier变换，离散余弦变换，反变换（显示频谱图）
# 频域滤波：低通滤波，高通滤波

# 以颜色直方图为特征，搜索本地图片，反馈相似图片并排序

def buttonSaveImg(img, entry):
    path = entry.get()
    # try:
    img.save(path)
    win22 = tk.Toplevel()
    win22.rowconfigure(0, weight=1)
    win22.columnconfigure(0, weight=1)
    win22.geometry('200x200')
    tk.Message(win22, text='保存成功').grid()
    # except:
    #     win22 = tk.Toplevel()
    #     win22.geometry('200x200')
    #     tk.Message(win22, text='图片路径无效').grid()
    #     win22.mainloop()


def gsnoise():
    global path
    if len(path) > 0:
        img = getimg(path)[1]
        size = img.shape
        noise = np.array(np.random.randint(20, size=size[0:-1]) - 10, dtype=np.uint8)
        noise = noise.reshape(size[0], size[1], 1)
        img = img + noise
        img = Image.fromarray(img)
        wings = tk.Toplevel()
        photo = ImageTk.PhotoImage(img)
        tk.Label(wings, image=photo).grid()
        wings.mainloop()


def button1():
    global lab1, path
    path = filedialog.askopenfilename()
    if len(path) > 0:
        img = getimg(path)[0]
        photo = ImageTk.PhotoImage(img)
        if lab1 == None:
            lab1 = tk.Label(win, image=photo)
            lab1.image = photo
            # lab1.rowconfigure()
            lab1.grid(row=3, columnspan=5,sticky=tk.NSEW)
        else:
            lab1.configure(image=photo)
            lab1.image = photo

# def getimg(a):
#     return ImageTk.getimage(a)

def button2():
    global lab1, path
    path = entry1.get()
    print(path)
    if len(path) > 0:
        img = getimg(path)[0]
        photo = ImageTk.PhotoImage(img)
        if lab1 == None:
            lab1 = tk.Label(win, image=photo)
            lab1.image = photo
            lab1.grid(row=3, columnspan=5,sticky=tk.NSEW)
        else:
            lab1.configure(image=photo)
            lab1.image = photo


def button21():  # 参考faster rcnn RandomHorizontalFlip
    global path
    if len(path) == 0:
        return 0
    img = getimg(path)[1]  # Image.fromarray
    img = np.flip(img, axis=1)
    img = Image.fromarray(img)

    win21 = tk.Toplevel()  # 此处不能写Tk（）因为根部窗口只能有一个

    win21.rowconfigure((1), weight=1)
    win21.columnconfigure((0, 1,2), weight=1)
    tk.Label(win21, text='输入图片保存路径', width=20).grid(row=0, column=0,sticky=tk.EW)
    entry21 = tk.Entry(win21)
    entry21.grid(row=0, column=1,sticky=tk.EW)
    tk.Button(win21, width=20, text='保存', command=partial(buttonSaveImg, img, entry21)).grid(row=0, column=2,sticky=tk.EW)
    photo21 = ImageTk.PhotoImage(img)
    tk.Label(win21, image=photo21).grid(row=1, columnspan=3,sticky=tk.NSEW)

    win21.mainloop()


def button22():
    if len(path) > 0:
        win22 = tk.Toplevel()
        win22.rowconfigure(0, weight=1)
        win22.columnconfigure(0, weight=1)
        win22.geometry('200x200')
        tk.Message(win22, text='想象一下，已经平移了，只不过我们以它的中心为参照点').grid()
        win22.mainloop()


def button23():
    # 剪切这个功能因为需要获取图片的坐标，实现鼠标拖动剪切，实际上很不好做”
    pass

    # l1.update()

    # w.update()


def button24():  # 旋转——做出拖动条
    global path
    if len(path)==0:
        return 0
    # 测试旋转框函数的可行性

    #     l1.configure(image=img1)
    a = tk.Toplevel(win)
    a.rowconfigure(3, weight=1)
    a.columnconfigure((0, 1), weight=1)
    img = Image.open(path)
    img = ImageTk.PhotoImage(img)
    # 这次我们换一个思路，先加最关键的控件

    # 最终画布
    l1 = tk.Label(a, image=img)
    l1.grid(row=3, columnspan=2,sticky=tk.NSEW)

    # 角度
    agl = tk.IntVar()
    agl.set(0)

    # 定义setangle函数，为滑块提供反馈
    def setangle(value):
        agl.set(value)

    # 滑块
    scale24 = tk.Scale(a, from_=0, to=360, orient=tk.HORIZONTAL, showvalue=0, tickinterval=45,
                       resolution=1, command=setangle)
    scale24.grid(row=2, columnspan=2, sticky=tk.EW)

    # 按钮函数组件1：旋转图像函数
    def rotimg():
        # angle.path
        img = cv.imread(path)
        angle = agl.get()
        (h, w) = img.shape[:2]
        center = (w // 2, h // 2)
        M = cv.getRotationMatrix2D(center, angle, 1.0)
        rotedimg = cv.warpAffine(img, M, (w, h))
        rgb_img = cv.cvtColor(rotedimg, cv.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_img)
        return img

    # 利用组件函数，构建按钮函数
    def button24():
        img = rotimg()
        # img.show()
        img = ImageTk.PhotoImage(img)
        l1.configure(image=img)
        a.mainloop()

    # 按钮控件
    b1 = tk.Button(a, width=20, command=button24, text='显示旋转图')
    b1.grid(row=1, column=1, sticky=tk.EW)

    # 角度显示盘
    la = tk.Label(a, textvariable=str(agl), bg='pink')
    la.grid(row=1, column=0, sticky=tk.EW)

    # 好的，既然我们实现了困难的部分，下面开始实现简单的部分，保存路径输入框entry
    entry01 = tk.Entry(a)
    entry01.grid(row=0, column=0, sticky=tk.EW)

    # 下面的部分是保存图片的按钮，会利用到之前的rotimg函数,和之前一样，先写按钮函数
    def button02():
        path = entry01.get()
        if len(path) == 0:
            print('保存失败')
            return 0
        img = rotimg()
        img.save(path)
        # 保存成功我们希望有个弹窗
        winmessage = tk.Toplevel(a)
        winmessage.rowconfigure(0, weight=1)
        winmessage.columnconfigure(0, weight=1)
        winmessage.geometry('300x200')
        tk.Message(winmessage, text='恭喜你，或者说恭喜这个熬了很久的猿，你们保存成功了').grid(sticky=tk.NSEW)

    # 这里就是保存图片按钮了
    b02 = tk.Button(a, text='左侧输入，点此保存', command=button02, bg='pink')
    b02.grid(row=0, column=1, sticky=tk.EW)

    a.mainloop()


def button25():    # 缩放，我们希望设置两个方法——输入缩放比或者做成可视化的那种拖动条
    global path
    if len(path)==0:
        return 0
    # 缩放功能
    a = tk.Toplevel()
    a.rowconfigure(3, weight=1)
    a.columnconfigure((0, 1), weight=1)
    img = Image.open(path)
    img = ImageTk.PhotoImage(img)

    # 显而易见，当我们已经可以实现旋转功能时，缩放就不在话下了
    # 第一步：定义图片展示窗口（毕竟咱是按照逻辑顺序）

    # 最终画布
    l31 = tk.Label(a, image=img)
    l31.grid(row=3, columnspan=2,sticky=tk.NSEW)

    # 比例
    rate = tk.DoubleVar()
    rate.set(1.0)

    # 定义setangle函数，为滑块提供反馈
    def setangle(value):
        rate.set(value)

    # 滑块
    scale24 = tk.Scale(a, from_=1, to=5, orient=tk.HORIZONTAL, showvalue=1, tickinterval=1,
                       resolution=0.1, command=setangle)
    scale24.grid(row=2, columnspan=2, sticky=tk.EW)

    # 定义组件函数，实现缩放功能
    def shrink():
        # 收缩比例，路径
        r = rate.get()
        img = Image.open(path)
        size = img.size
        #     print(size)
        img2 = img.resize((int(size[0] / r), int(size[1] / r)))
        return img2

    def button22():
        img = shrink()
        #     img.show()
        img = ImageTk.PhotoImage(img)
        l31.configure(image=img)
        a.mainloop()

    # 按钮控件
    b22 = tk.Button(a, width=20, command=button22, text='显示缩放图')
    b22.grid(row=1, column=1, sticky=tk.EW)

    # 角度显示盘
    l21 = tk.Label(a, textvariable=str(rate), bg='pink')
    l21.grid(row=1, column=0, sticky=tk.EW)

    # 好的，既然我们实现了困难的部分，下面开始实现简单的部分，保存路径输入框entry
    entry01 = tk.Entry(a)
    entry01.grid(row=0, column=0, sticky=tk.EW)

    # 下面的部分是保存图片的按钮，会利用到之前的rotimg函数,和之前一样，先写按钮函数
    def button02():
        path = entry01.get()
        if len(path) == 0:
            print('保存失败')
            return 0
        img = shrink()
        img.save(path)
        # 保存成功我们希望有个弹窗
        winmessage = tk.Toplevel(a)
        winmessage.rowconfigure(0, weight=1)
        winmessage.columnconfigure(0, weight=1)
        winmessage.geometry('300x200')
        tk.Message(winmessage, text='恭喜你，或者说恭喜这个熬了很久的猿，你们保存成功了').grid(sticky=tk.NSEW)

    # 这里就是保存图片按钮了
    b02 = tk.Button(a, text='左侧输入，点此保存', command=button02, bg='pink')
    b02.grid(row=0, column=1, sticky=tk.EW)

    a.mainloop()

    # 至此，缩放功能实现完毕button25


def button31():  # 平滑（模糊）
    # 平滑功能
    global path
    if len(path) == 0:
        return 0
    a = tk.Toplevel()
    a.rowconfigure(3, weight=1)
    a.columnconfigure((0, 1), weight=1)

    img = Image.open(path)
    img = ImageTk.PhotoImage(img)

    # 显而易见，当我们已经可以实现旋转功能时，缩放就不在话下了
    # 第一步：定义图片展示窗口（毕竟咱是按照逻辑顺序）
    kernels = [np.ones((i, i), np.float32) / (i * i) for i in range(1, 11)]
    # 最终画布
    l31 = tk.Label(a, image=img)
    l31.grid(row=3, columnspan=2,sticky=tk.NSEW)

    # 卷积核的大小比例
    rate = tk.IntVar()
    rate.set(1)

    # 定义setangle函数，为滑块提供反馈
    def setkernel(value):
        rate.set(value)

    # 滑块
    scale31 = tk.Scale(a, from_=1, to=11, orient=tk.HORIZONTAL, showvalue=1, tickinterval=2,
                       command=setkernel)
    scale31.grid(row=2, columnspan=2, sticky=tk.EW)

    # 定义组件函数，实现缩放功能
    def averaging():
        # 核大小，图片
        r = (rate.get() - 1) // 2
        img = cv.imread(path)
        kernel = kernels[r]
        avgimg = cv.filter2D(img, -1, kernel)
        rgb_img = cv.cvtColor(avgimg, cv.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_img)
        return img

    def button22():
        img = averaging()
        img = ImageTk.PhotoImage(img)
        l31.configure(image=img)
        a.mainloop()

    # 按钮控件
    b22 = tk.Button(a, width=20, command=button22, text='显示缩放图')
    b22.grid(row=1, column=1, sticky=tk.EW)

    # 显示盘
    l21 = tk.Label(a, textvariable=str(rate), bg='pink')
    l21.grid(row=1, column=0, sticky=tk.EW)

    # 好的，既然我们实现了困难的部分，下面开始实现简单的部分，保存路径输入框entry
    entry01 = tk.Entry(a)
    entry01.grid(row=0, column=0, sticky=tk.EW)

    # 下面的部分是保存图片的按钮，会利用到之前的rotimg函数,和之前一样，先写按钮函数
    def button02():
        path = entry01.get()
        if len(path) == 0:
            print('保存失败')
            return 0
        img = averaging()
        img.save(path)
        # 保存成功我们希望有个弹窗
        winmessage = tk.Toplevel(a)
        winmessage.rowconfigure(0, weight=1)
        winmessage.columnconfigure(0, weight=1)
        winmessage.geometry('300x200')
        tk.Message(winmessage, text='恭喜你，或者说恭喜这个熬了很久的猿，你们保存成功了').grid(sticky=tk.NSEW)

    # 这里就是保存图片按钮了
    b02 = tk.Button(a, text='左侧输入，点此保存', command=button02)
    b02.grid(row=0, column=1, sticky=tk.EW)

    a.mainloop()

    # 至此，平滑功能实现完毕


def button32():  # 锐化
    # 锐化功能
    global path
    if len(path) == 0:
        return 0
    a = tk.Toplevel()
    a.rowconfigure(3,weight=1)
    a.columnconfigure((0, 1), weight=1)
    # global path
    img = Image.open(path)
    img = ImageTk.PhotoImage(img)

    # 显而易见，当我们已经可以实现旋转功能时，缩放就不在话下了
    # 第一步：定义高通滤波核
    kernel0 = -np.ones((3, 3), np.float32)
    kernel0[1, 1] += 9
    kernel1 = -np.ones((5, 5), np.float32)
    kernel1[1:4, 1:4] = -kernel0
    kernel1[2, 2] = 8
    kernel2 = -np.ones((5, 5), np.float32)
    kernel2[2, 2] += 25
    kernels = [kernel0, kernel1, kernel2]

    # 最终画布
    l31 = tk.Label(a, image=img)
    l31.grid(row=3, columnspan=2,sticky=tk.NSEW)

    # 卷积核的大小比例
    rate = tk.IntVar()
    rate.set(1)

    # 定义setangle函数，为滑块提供反馈
    def setkernel(value):
        rate.set(value)

    # 滑块
    scale31 = tk.Scale(a, from_=1, to=3, orient=tk.HORIZONTAL, showvalue=1, tickinterval=1,
                       resolution=1, command=setkernel)
    scale31.grid(row=2, columnspan=2, sticky=tk.EW)

    # 定义组件函数，实现缩放功能
    def averaging():
        # 核大小，图片
        r = rate.get() - 1
        img = cv.imread(path)
        kernel = kernels[r]
        avgimg = cv.filter2D(img, -1, kernel)
        rgb_img = cv.cvtColor(avgimg, cv.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_img)
        return img

    def button22():
        img = averaging()
        img = ImageTk.PhotoImage(img)
        l31.configure(image=img)
        a.mainloop()

    # 按钮控件
    b22 = tk.Button(a, width=20, command=button22, text='显示缩放图')
    b22.grid(row=1, column=1, sticky=tk.EW)

    # 显示盘
    l21 = tk.Label(a, textvariable=str(rate), bg='pink')
    l21.grid(row=1, column=0, sticky=tk.EW)

    # 好的，既然我们实现了困难的部分，下面开始实现简单的部分，保存路径输入框entry
    entry01 = tk.Entry(a)
    entry01.grid(row=0, column=0, sticky=tk.EW)

    # 下面的部分是保存图片的按钮
    def button02():
        path = entry01.get()
        if len(path) == 0:
            print('保存失败')
            return 0
        img = averaging()
        img.save(path)
        # 保存成功我们希望有个弹窗
        winmessage = tk.Toplevel(a)
        winmessage.rowconfigure(0, weight=1)
        winmessage.columnconfigure(0, weight=1)
        winmessage.geometry('300x200')
        tk.Message(winmessage, text='恭喜你，或者说恭喜这个熬了很久的猿，你们保存成功了').grid(sticky=tk.NSEW)

    # 这里就是保存图片按钮了
    b02 = tk.Button(a, text='左侧输入，点此保存', command=button02)
    b02.grid(row=0, column=1, sticky=tk.EW)

    a.mainloop()

    # 至此，锐化功能实现完毕


def button23():  # 直方图均衡化
    global path
    if len(path) == 0:
        return 0
    # 利用cv内置工具获得直方图，已经均衡化后的图像
    img_ori=cv.imread(path)
    for i in range(3):
        im=img_ori[:,:,i]
        equ=cv.equalizeHist(im)
        try:
            im_box.append(equ)
        except:
            im_box=[equ]
    im_box=np.stack((im_box[2],im_box[1],im_box[0]),axis=2)
    #获得直方图三尺度均衡化后的图片
    rgb_im=Image.fromarray(im_box)
    #rgb_im.show()
    img = cv.imread(path, 0)
    hist = cv.calcHist([img], [0], None, [256], [0, 256])
    equ = cv.equalizeHist(img)
    histequ = cv.calcHist([equ], [0], None, [256], [0, 256])

    # 第二步，把这些图像放到一个figure上
    f = Figure(figsize=(10, 8), dpi=100)
    a11 = f.add_subplot(221)  # 添加子图:1行1列第1个
    # a11.title='原图像素值直方图'
    x = np.arange(256)
    y = hist
    a11.plot(x, y)

    a12 = f.add_subplot(222)
    # a12.title='原图灰度图'
    rgb_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    a12.imshow(rgb_img)

    a21 = f.add_subplot(223)
    # a21.title('均衡化后的直方图')
    y = histequ
    a21.plot(x, y)

    a22 = f.add_subplot(224)
    # a22.title('均衡化后的图像')
    rgb_equ = cv.cvtColor(equ, cv.COLOR_BGR2RGB)
    a22.imshow(rgb_equ)

    # 第三步，建立和tkinter的联系,提供保存方法
    #显示均衡化的彩图
    def button10():
        img=rgb_im
        aa=tk.Toplevel()
        img=ImageTk.PhotoImage(img)
        aal=tk.Label(aa,image=img)
        aal.grid()
        aa.mainloop()

    #保存均衡化彩图
    def button11():
        path = entry00.get()
        rgb_im.save(path)
        winmessage = tk.Toplevel(a)
        winmessage.geometry('300x200')
        tk.Message(winmessage, text='恭喜你，或者说恭喜这个熬了很久的猿，你们保存成功了').grid(sticky=tk.NSEW)

    a = tk.Toplevel()
    a.rowconfigure((2),weight=1)
    a.columnconfigure((0,1),weight=1)
    img_real=ImageTk.PhotoImage(rgb_im)
    b = tk.Frame(a)
    canvas1 = FigureCanvasTkAgg(f, b)
    canvas1.draw()
    canvas1.get_tk_widget().grid()
    b.grid(row=2, columnspan=2, sticky=tk.NSEW)
    b10=tk.Button(a,text='展示均衡化彩图',command=button10).grid(row=1,column=0,sticky=tk.EW)
    b11=tk.Button(a,text='保存均衡化彩图',command=button11).grid(row=1,column=1,sticky=tk.EW)
    # 提供保存方法
    def button01():
        path = entry00.get()
        cv.imwrite(path, equ)
        winmessage = tk.Toplevel(a)
        winmessage.rowconfigure(0, weight=1)
        winmessage.columnconfigure(0, weight=1)
        winmessage.geometry('300x200')
        tk.Message(winmessage, text='恭喜你，或者说恭喜这个熬了很久的猿，你们保存成功了').grid(sticky=tk.NSEW)

    entry00 = tk.Entry(a)
    entry00.grid(row=0, column=0, sticky=tk.EW)
    b01 = tk.Button(a, text='点此保存均衡化的图片', command=button01)
    b01.grid(row=0, column=1,sticky=tk.EW)
    a.mainloop()

def button33():#低通滤波
    '''低通滤波，基本组件：

        文字框，保存图片按钮

        滑块数值展示，展示图片

        滑块

        图片'''
    # 判断函数
    if len(path) == 0:
        return 0
    if path.endswith('.jpg') is not True:
        return 0
    # 读取图片
    a = tk.Toplevel()
    img = Image.open(path)
    img = ImageTk.PhotoImage(img)

    # 可以调节界面
    a.rowconfigure(3, weight=1)
    for j in range(2):
        a.columnconfigure(j, weight=1)
    # 画布
    l30 = tk.Label(a, image=img)
    l30.grid(row=3, columnspan=2, sticky=tk.NSEW)

    # 定义一个变量
    kernelwidth = tk.IntVar()
    kernelwidth.set(1)

    # 定义滑块函数
    def setwidth(value):
        kernelwidth.set(value)

    # 定义滑块
    scale20 = tk.Scale(a, from_=1, to=5, orient=tk.HORIZONTAL, showvalue=1,
                       resolution=1, tickinterval=1, command=setwidth)
    scale20.grid(row=2, columnspan=2, sticky=tk.EW)

    # 滑块数值显示器
    l10 = tk.Label(a, textvariable='滤波核宽度为' + str(kernelwidth.get() * 20), bg='pink')
    l10.grid(row=1, column=0, sticky=tk.EW)

    # 按钮函数组件1：低通滤波器
    def low_filter():
        width = kernelwidth.get() * 10
        img = cv.imread(path)
        rows, cols = img.shape[:2]
        mask = np.zeros((rows,cols), np.uint8)
        mask[(rows // 2 - width):(rows // 2 + width)][:, (cols // 2 - width):(cols // 2 + width)] = 1
        img_l = [1, 2, 3]
        for i in range(3):
            f1 = np.fft.fft2(img[:, :, i])
            f1shift = np.fft.fftshift(f1) * mask
            f2shift = np.fft.ifftshift(f1shift)
            img_new = np.fft.ifft2(f2shift)
            img_new = np.abs(img_new)
            img_new = (img_new - np.amin(img_new)) / (np.amax(img_new) - np.amin(img_new))
            img_new *= 255
            img_l[i] = np.array(img_new, np.uint8)
        img = np.stack((img_l[0], img_l[1], img_l[2]), axis=2)
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        return img

    def button11():
        img = low_filter()
        img = ImageTk.PhotoImage(img)
        l30.configure(image=img)
        a.mainloop()

    b11 = tk.Button(a, text='点此展示滤波效果', command=button11)
    b11.grid(row=1, column=1, sticky=tk.EW)

    # 保存
    entry01 = tk.Entry(a)
    entry01.grid(row=0, column=0, sticky=tk.EW)

    # 下面的部分是保存图片的按钮，会利用到之前的rotimg函数,和之前一样，先写按钮函数
    def button02():
        path = entry01.get()
        if len(path) == 0:
            print('保存失败')
            return 0
        img = low_filter()
        img.save(path)
        # 保存成功我们希望有个弹窗
        winmessage = tk.Toplevel(a)
        winmessage.rowconfigure(0, weight=1)
        winmessage.columnconfigure(0, weight=1)
        winmessage.geometry('300x200')
        tk.Message(winmessage, text='恭喜你，或者说恭喜这个熬了很久的猿，你们保存成功了').grid(sticky=tk.NSEW)

    # 这里就是保存图片按钮了
    b02 = tk.Button(a, text='左侧输入，点此保存', command=button02)
    b02.grid(row=0, column=1, sticky=tk.EW)

    a.mainloop()
def button35():#低通滤波
    # 判断函数
    if len(path) == 0:
        return 0
    if path.endswith('.jpg') is not True:
        return 0
    # 读取图片
    a = tk.Toplevel()
    img = Image.open(path)
    img = ImageTk.PhotoImage(img)

    # 可以调节界面

    a.rowconfigure(3, weight=1)
    for j in range(2):
        a.columnconfigure(j, weight=1)
    # 画布
    l30 = tk.Label(a, image=img)
    l30.grid(row=3, columnspan=2, sticky=tk.NSEW)

    # 定义一个变量
    kernelwidth = tk.IntVar()
    kernelwidth.set(1)

    # 定义滑块函数
    def setwidth(value):
        kernelwidth.set(value)

    # 定义滑块
    scale20 = tk.Scale(a, from_=1, to=5, orient=tk.HORIZONTAL, showvalue=1,
                       resolution=1, tickinterval=1, command=setwidth)
    scale20.grid(row=2, columnspan=2, sticky=tk.EW)

    # 滑块数值显示器
    l10 = tk.Label(a, textvariable='滤波核宽度为' + str(kernelwidth.get() * 20), bg='pink')
    l10.grid(row=1, column=0, sticky=tk.EW)

    # 按钮函数组件1：低通滤波器
    def low_filter():
        width = kernelwidth.get() * 10
        img = cv.imread(path)
        rows, cols = img.shape[:2]
        mask = np.ones((rows,cols), np.uint8)
        mask[(rows // 2 - width):(rows // 2 + width)][:, (cols // 2 - width):(cols // 2 + width)] = 0
        img_l = [1, 2, 3]
        for i in range(3):
            f1 = np.fft.fft2(img[:, :, i])
            f1shift = np.fft.fftshift(f1) * mask
            f2shift = np.fft.ifftshift(f1shift)
            img_new = np.fft.ifft2(f2shift)
            img_new = np.abs(img_new)
            img_new = (img_new - np.amin(img_new)) / (np.amax(img_new) - np.amin(img_new))
            img_new *= 255
            img_l[i] = np.array(img_new, np.uint8)
        img = np.stack((img_l[0], img_l[1], img_l[2]), axis=2)
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        return img

    def button11():
        img = low_filter()
        img = ImageTk.PhotoImage(img)
        l30.configure(image=img)
        a.mainloop()

    b11 = tk.Button(a, text='点此展示滤波效果', command=button11)
    b11.grid(row=1, column=1, sticky=tk.EW)

    # 保存
    entry01 = tk.Entry(a)
    entry01.grid(row=0, column=0, sticky=tk.EW)

    # 下面的部分是保存图片的按钮，会利用到之前的rotimg函数,和之前一样，先写按钮函数
    def button02():
        path = entry01.get()
        if len(path) == 0:
            print('保存失败')
            return 0
        img = low_filter()
        img.save(path)
        # 保存成功我们希望有个弹窗
        winmessage = tk.Toplevel(a)
        winmessage.rowconfigure(0, weight=1)
        winmessage.columnconfigure(0, weight=1)
        winmessage.geometry('300x200')
        tk.Message(winmessage, text='恭喜你，或者说恭喜这个熬了很久的猿，你们保存成功了').grid(sticky=tk.NSEW)

    # 这里就是保存图片按钮了
    b02 = tk.Button(a, text='左侧输入，点此保存', command=button02)
    b02.grid(row=0, column=1, sticky=tk.EW)

    a.mainloop()

win = tk.Tk()
win.rowconfigure((3),weight=1)
win.columnconfigure((0,1,2,3,4),weight=1)
path = ''
lab1 = tk.Label(win,width=30,height=30).grid(row=3,column=0,sticky=tk.NSEW,columnspan=5)

entry1 = tk.Entry(win, width=20)
entry1.grid(row=0, column=1, sticky=tk.EW)
lab2 = tk.Label(win, text='输入图片路径', width=20).grid(row=0, column=0,sticky=tk.EW)
lab2 = tk.Label(win, text='手动选择路劲', width=20).grid(row=0, column=3,sticky=tk.EW)

b1 = tk.Button(win, text='选择路径', command=button1, width=20).grid(row=0, column=4,sticky=tk.EW)
b2 = tk.Button(win, text='确认路径', command=button2, width=20).grid(row=0, column=2,sticky=tk.EW)

b21 = tk.Button(win, text='镜像', command=button21, width=20).grid(row=1, column=0,sticky=tk.EW)
b22 = tk.Button(win, text='平移', command=button22, width=20).grid(row=1, column=1,sticky=tk.EW)
b23 = tk.Button(win, text='直方图均衡化', command=button23, width=20).grid(row=1, column=2,sticky=tk.EW)
b24 = tk.Button(win, text='顺时针旋转', command=button24, width=20).grid(row=1, column=3,sticky=tk.EW)
b25 = tk.Button(win, text='缩放', command=button25, width=20).grid(row=1, column=4,sticky=tk.EW)

b31 = tk.Button(win, text='图像平滑', command=button31, width=20).grid(row=2, column=0,sticky=tk.EW)
b32 = tk.Button(win, text='图像锐化', command=button32, width=20).grid(row=2, column=1,sticky=tk.EW)
b33 = tk.Button(win, text='低通滤波', command=button33, width=20).grid(row=2, column=2,sticky=tk.EW)
b34 = tk.Button(win, text='高斯噪声', command=gsnoise, width=20).grid(row=2, column=3,sticky=tk.EW)
b35 = tk.Button(win, text='高通滤波', command=button35, width=20).grid(row=2, column=4,sticky=tk.EW)
win.mainloop()

