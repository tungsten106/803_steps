import tkinter as tk
from PIL import Image, ImageTk

# 创建主窗口
window = tk.Tk()
window.title("Image Viewer")

# 加载图片
image_path = "pics/calligraphy.JPG"  # 替换为你的图片路径
image = Image.open(image_path)

# 获取窗口大小
window_width = 1086
window_height = 600

# 调整图片大小以适应窗口
image = image.resize((window_width, window_height))

# 将图片转换为Tkinter格式
photo = ImageTk.PhotoImage(image)

# 创建标签并显示图片
label = tk.Label(window, image=photo)
label.pack()

# 运行主循环
window.mainloop()
