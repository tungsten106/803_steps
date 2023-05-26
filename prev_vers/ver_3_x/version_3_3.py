from polygons_1_1_2 import *
from quad_tree_csdn_new import *
import cv2

"""
version3.3: quad_tree_csdn_new.py, 算法改进
"""


# TODO: 1）改变效果
#       2) 连接雷达
# TODO: 上传github


def draw_dilate(mouse_x, mouse_y, sq_size):
    global dilate_index, mouse_pressed, old_polygon, mask
    global cropped_subimage, cropped_sub_small
    global max_dilate, new_polygon
    if not mouse_pressed:
        return

    # 计算要显示的图像位置和大小
    x = max(0, pressed_x - sq_size // 2)
    y = max(0, pressed_y - sq_size // 2)
    width = min(sq_size, canvas_width - x)
    height = min(sq_size, canvas_height - y)
    new_subimage = image_pil.crop((x, y, x + width, y + height))

    bounded_img = Image.new("RGB", (canvas_width, canvas_width), "black")
    bounded_img.paste(new_subimage,
                      (x, y))  # 将b贴到a的坐标为（0,0）的位置，以图片左上角为坐标原点，这里说的是原点的移动
    # bounded_img.show()
    bounded_img = np.array(bounded_img)
    bounded_img = cv2.cvtColor(bounded_img, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像

    cropped_sub_small = np.array(bounded_img)
    # # dilate
    # dilate_index -= 1
    # # dilate_index = max(0, dilate_index)
    # if dilate_index >= 0:
    #     dilated_img = dilate2(cropped_sub_small, dilate_index, 128 - 2 * dilate_index)
    # else:
    #     dilate_index = max(-max_dilate, dilate_index)
    #     dilated_img = cv2.dilate(cropped_sub_small, kernel, iterations=abs(dilate_index))

    screenshot = get_quad_grid(cropped_sub_small, min_sq=sq_size / (2 ** quad_power),
                               subimage_coord=(x, y, x + width, y + height))

    sub_photo = ImageTk.PhotoImage(Image.fromarray(screenshot))

    canvas.create_image(0,0, anchor=tk.NW, image=sub_photo, tags="revealed_image")

    # 保留对sub_photo的引用
    canvas.sub_photo = sub_photo
    if mouse_pressed:
        window.update()
        cur_sq_size = sq_size + 10
        window.after(80, lambda: draw_dilate(mouse_x, mouse_y, min(cur_sq_size, max_sq_size)))


def draw_erode(mouse_x, mouse_y, sq_size):
    global dilate_index, mouse_pressed, cropped_sub_small, new_subimage
    global cur_sq_size, new_polygon
    if mouse_pressed:
        return
    # 计算要显示的图像位置和大小
    sq_size = cropped_sub_small.shape[0] // 2
    x = max(0, mouse_x - sq_size)
    y = max(0, mouse_y - sq_size)
    width = min(sq_size, canvas_width - x)
    height = min(sq_size, canvas_height - y)

    # 开始腐蚀
    # sub_image = dilate2(sub_image, abs(dilate_index), 128 + 2 * dilate_index)
    if dilate_index < 0:
        eroded_subimage = cv2.dilate(cropped_sub_small, kernel, iterations=abs(dilate_index))
    else:
        eroded_subimage = cv2.erode(cropped_sub_small, kernel, iterations=dilate_index)

    # 更新参数
    dilate_index += 1
    # dilate_index = min(20, dilate_index)

    screenshot = get_quad_grid(eroded_subimage, min_sq=sq_size / (2 ** quad_power),
                               subimage_coord=(x, y, x + width, y + height))
    sub_photo = ImageTk.PhotoImage(Image.fromarray(screenshot))
    # sub_photo = ImageTk.PhotoImage(Image.fromarray(eroded_subimage))
    canvas.create_image(0,0, anchor=tk.NW, image=sub_photo, tags="revealed_image")

    # 保留对sub_photo的引用
    canvas.sub_photo = sub_photo
    if not mouse_pressed and dilate_index <= 10:
        window.update()
        window.after(10, lambda: draw_erode(mouse_x, mouse_y, sq_size))
    else:
        canvas.delete(tk.ALL)


def on_mouse_press(event):
    global mouse_pressed, dilate_index, cropped_subimage
    global old_polygon
    global pressed_x, pressed_y
    global max_dilate
    dilate_index = init_dilate
    pressed_x, pressed_y = event.x, event.y

    # 现在开始1）裁剪图像 2）使用sub_image内的相对坐标
    x = max(0, pressed_x - max_sq_size // 2)
    y = max(0, pressed_y - max_sq_size // 2)
    width = min(max_sq_size, canvas_width - x)
    height = min(max_sq_size, canvas_height - y)
    sub_image = image_pil.crop((x, y, x + width, y + height))

    # 为了让多边形的形状固定 先生成一个固定的“大多边形”
    sub_image = np.array(sub_image)
    sub_image_center = (sub_image.shape[0] // 2, sub_image.shape[1] // 2)
    old_polygon = Polygon_112(n=poly_n,
                              center=sub_image_center,
                              size=max_sq_size)
    cropped_subimage = crop_polygon(np.array(sub_image), old_polygon)

    mode = get_mode(x, y)
    max_dilate = max_dilate_ind[mode]

    if not mouse_pressed:
        mouse_pressed = True
        draw_dilate(pressed_x, pressed_y,
                    init_sq_size)


def on_mouse_release(event):
    global mouse_pressed, dilate_index
    global pressed_x, pressed_y
    x, y = pressed_x, pressed_y
    if mouse_pressed:
        mouse_pressed = False
        draw_erode(x, y, max_sq_size)


# 创建主窗口
window = tk.Tk()
window.title("Image Revealer")
window.configure(bg="black")

# 设置画布大小
canvas_width = 1086
canvas_height = 600
# 加载图片 改变图片大小
# image_path = "pics/calligraphy.JPG"  # 图片路径
image_path = "pics/xiaoyaoyou_new.jpg"
image = Image.open(image_path)
image = image.resize((canvas_width, canvas_height))
image = np.array(image)

# 将图像转换为PIL Image格式
image_pil = Image.fromarray(image)
# 将PIL Image转换为Tkinter Image格式
photo = ImageTk.PhotoImage(image=image_pil)

# 创建画布
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="black")
canvas.pack()
# 画5*9网格
n_row = 5
n_col = 9
grid_width = int(canvas_width / n_col)
grid_height = int(canvas_height / n_row)
for i in range(1, n_row):  # horizontal lines
    canvas.create_line(0, grid_height * i, canvas_width, grid_height * i, fill='white')
for j in range(1, n_col):
    canvas.create_line(grid_width * j, 0, grid_width * j, canvas_height, fill='white')

# parameters
boundary_size = int(canvas_width//3)  # 膨胀界限
max_sq_size = int(canvas_width // n_col)  # 图片扩大最大尺寸
init_sq_size = 10
poly_n = 15
poly_range = (init_sq_size, max_sq_size)
mouse_pressed = False
init_dilate = 5

k_size = 3
kernel = np.ones((k_size, k_size), np.uint8)
quad_power = 6

# set different mode param
max_dilate_ind = [0, 3, 5, 15]
mode_table = np.array(
    [
        [2, 2, 2, 3, 4, 2, 1, 4, 4],
        [2, 2, 2, 1, 1, 3, 1, 4, 4],
        [2, 2, 2, 1, 1, 4, 2, 1, 2],
        [4, 4, 3, 1, 2, 2, 1, 3, 3],
        [4, 4, 2, 4, 2, 2, 2, 3, 3]
    ]
)


def get_mode(x, y):
    return mode_table[int(y // grid_width)][int(x // grid_height)] - 1
    # return min(int((x // (canvas_width // 2)) + 2 * (y // (canvas_height // 2))), 4)


# 绑定鼠标点击事件
canvas.bind("<Button-1>", on_mouse_press)
canvas.bind("<ButtonRelease-1>", on_mouse_release)
canvas.delete("revealed_image")

# 运行主循环
window.mainloop()
