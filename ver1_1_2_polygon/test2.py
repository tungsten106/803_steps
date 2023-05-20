from ver1_1_2_polygon.utils import *
from PIL import ImageTk, Image

# 创建主窗口
window = tk.Tk()
window.title("Image Revealer")
window.configure(bg="black")

# 加载图片
image_path = "../pics/calligraphy.JPG"  # 替换为你的图片路径
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像
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

max_sq_size = 50
poly_n = 6
def on_mouse_press(event):
    global mouse_pressed, dilate_index, sub_image
    global old_polygon
    dilate_index = 50
    pressed_x, pressed_y = event.x, event.y
    # init_sq_size = 5
    # 现在开始1）裁剪图像 2）使用sub_image内的相对坐标
    x = int(max(0, pressed_x - max_sq_size // 2))
    y = int(max(0, pressed_y - max_sq_size // 2))
    width = min(max_sq_size, canvas_width - x)
    height = min(max_sq_size, canvas_height - y)
    sub_image = image_pil.crop((x, y, x + width, y + height))
    # sub_image.show()
    # 为了让多边形的形状固定 先生成一个固定的“大多边形”
    sub_image = np.array(sub_image)
    sub_image_center = (sub_image.shape[0] // 2, sub_image.shape[1] // 2)
    old_polygon = Polygon_112(n=poly_n,
                              center=sub_image_center,
                              size=max_sq_size)
    new_vertices = old_polygon.moved_vertices(x, y)
    # print(new_vertices)
    canvas.create_polygon(new_vertices,
                          outline='red', fill='white', width=1)



# 绑定鼠标点击事件
canvas.bind("<Button-1>", on_mouse_press)

# 运行主循环
window.mainloop()