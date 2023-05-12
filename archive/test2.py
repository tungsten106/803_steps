import tkinter as tk
from PIL import Image, ImageTk

# 创建主窗口
window = tk.Tk()

# 加载图像
image_path = "../calligraphy.JPG"  # 替换为你的图像路径
original_image = Image.open(image_path)

# 裁剪图像
x = 100  # 裁剪区域左上角 x 坐标
y = 100  # 裁剪区域左上角 y 坐标
width = 200  # 裁剪区域宽度
height = 200  # 裁剪区域高度
cropped_image = original_image.crop((x, y, x + width, y + height))

# 将裁剪后的图像转换为PhotoImage对象
cropped_photo = ImageTk.PhotoImage(cropped_image)

# 创建标签，并显示裁剪后的图像
label = tk.Label(window, image=cropped_photo)
label.pack()

# 运行主循环
window.mainloop()
