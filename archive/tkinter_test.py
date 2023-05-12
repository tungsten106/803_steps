import tkinter as tk
from tkinter import ttk

# button ---------------------------
# def callback():
# 	print("你点击了按钮")
#
# window=tk.Tk()#创建一个窗口
# button1=tk.Button(window, text='press', command=callback)#如果command还没有实现好功能，可以先填入'disabled'
# button1.pack()#打包组件
#
# window.mainloop()#维持窗口直至手动关闭

# canvas ------------------------------------
# win = tk.Tk()
# win.geometry('800x600')
# w = tk.Canvas(win, width=100, height=300)
# w.pack()
# w.create_line(0, 50, 200, 50, fill="yellow")
# # 画一条红色的竖线（虚线）
# w.create_line(100, 0, 100, 100, fill="red", dash=(4, 4))
# # 中间画一个蓝色的矩形
# w.create_rectangle(50, 25, 150, 75, fill="blue")
# win.mainloop()

# insert texts --------------------
# win = tk.Tk()
# # w = tk.Label(win, text='这只是这个label的文本').pack()
# longtext = """
# Label 可以显示多行文本，你可以直接使用换行符
# 或使用 wraplength 选项来实现。当文本换行的时
# 候，你可以使用 anchor 和 justify 选项来使得
# 文本如你所希望的显示出来。
# """
# w = tk.Label(win, text=longtext, anchor="w", justify="left").pack()
# win.mainloop()

# insert pics -----------------------------------------
win = tk.Tk()
from PIL import ImageTk, Image

img = Image.open('../xiaoyaoyou.jpeg')
size = img.size
print(size)
# win.geometry('200x800')
win.geometry('{}x{}'.format(size[0] + 100, size[1] + 100))  # fit size
photo = ImageTk.PhotoImage(img)
a = tk.Label(win, image=photo).pack()
# photo = tk.PhotoImage(file="python.gif")
# w = tk.Label(win, image=photo)
# w.pack()
win.mainloop()
