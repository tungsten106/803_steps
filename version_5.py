from polygons_1_1_2 import *
from quad_tree_csdn_new import *
import cv2

"""
version5: 使用输入信号
"""


# TODO: 1）改变效果  # complete

#       2) 连接雷达
# TODO: 上传github


#tmp vars



def draw_dilate(mouse_x, mouse_y, sq_size):
    global dilate_index, mouse_pressed, old_polygon, mask
    global cropped_subimage, bounded_img, new_subimage
    global max_dilate, new_polygon, cur_sq_size

    cur_sq_size = sq_size
    if not mouse_pressed:
        return

    # 计算要显示的图像位置和大小
    x = max(0, pressed_x - sq_size // 2)
    y = max(0, pressed_y - sq_size // 2)
    width = min(sq_size, canvas_width - x)
    height = min(sq_size, canvas_height - y)
    new_subimage = image_pil.crop((x, y, x + width, y + height))
    new_subimage = np.array(new_subimage)

    new_polygon = Polygon_112(n=poly_n,
                              size=sq_size,
                              center=(width//2, height//2),
                              angles=old_polygon.angles,
                              distances=old_polygon.distances/max_sq_size*sq_size)
    cropped_subimage = crop_polygon(new_subimage, new_polygon)

    bounded_img = Image.new("RGB", (boundary_size, boundary_size), "black")
    new_x, new_y = int(boundary_size // 2 - sq_size // 2), int(boundary_size // 2 - sq_size // 2)
    bounded_img.paste(Image.fromarray(cropped_subimage),
                      (new_x, new_y))
    # bounded_img.show()
    bounded_img = np.array(bounded_img)
    bounded_img = cv2.cvtColor(bounded_img, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像  # 裁剪后的原图

    # dilate
    if max_dilate < 0:
        dilate_index = max(abs(max_dilate), dilate_index)
        dilated_img = cv2.erode(bounded_img, kernel, iterations=dilate_index)
        dilate_index -= 1
    else:
        if dilate_index >= 0:
            dilated_img = dilate3(bounded_img, dilate_index, 128 - 2 * dilate_index,
                                  step = sq_size//5)
            dilate_index -= 1
        else:
            # print(dilate_index, max_dilate)
            dilate_index = max(0-max_dilate, dilate_index)
            dilated_img = cv2.dilate(bounded_img, kernel, iterations=abs(dilate_index))
            dilate_index -= 3

    # print(dilated_img.shape)
    bg_img = Image.new("RGB", (canvas_width, canvas_width), "black")
    bg_img.paste(Image.fromarray(dilated_img),
                 (int(pressed_x - dilated_img.shape[0] // 2),
                  int(pressed_y - dilated_img.shape[0] // 2)))  # 将b贴到a的坐标为（0,0）的位置，以图片左上角为坐标原点，这里说的是原点的移动
    bg_img = np.array(bg_img)
    bg_img = cv2.cvtColor(bg_img, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像

    # print(f"dilate:{(x, y, x + width, y + height)}")

    screenshot = get_quad_grid(bg_img, min_sq=sq_size / (2 ** (quad_power-1)),
                               subimage_coord=(x, y, x + width, y + height))

    sub_photo = ImageTk.PhotoImage(Image.fromarray(screenshot))

    canvas.create_image(0, 0, anchor=tk.NW, image=sub_photo, tags="revealed_image")

    # 保留对sub_photo的引用
    canvas.sub_photo = sub_photo
    # if mouse_pressed:
    #     window.update()
    #     cur_sq_size = sq_size + 10
    #     window.after(20, lambda: draw_dilate(mouse_x, mouse_y, min(cur_sq_size, max_sq_size)))


def draw_erode(mouse_x, mouse_y, sq_size):
    global dilate_index, mouse_pressed, new_subimage
    global cur_sq_size, new_polygon, bounded_img
    global pressed_x, pressed_y
    if mouse_pressed:
        return
    # 计算要显示的图像位置和大小
    # sq_size =
    x = max(0, pressed_x - sq_size//2)
    y = max(0, pressed_y - sq_size//2)
    width = min(sq_size, canvas_width - x)
    height = min(sq_size, canvas_height - y)

    # 开始腐蚀
    # sub_image = dilate2(sub_image, abs(dilate_index), 128 + 2 * dilate_index)
    if dilate_index < 0:
        eroded_subimage = cv2.dilate(bounded_img, kernel, iterations=abs(dilate_index))
        # 更新参数
        dilate_index += 3
    else:
        eroded_subimage = cv2.erode(bounded_img, kernel, iterations=dilate_index)
        dilate_index += 1

    # dilate_index = min(20, dilate_index)
    bg_img = Image.new("RGB", (canvas_width, canvas_width), "black")
    bg_img.paste(Image.fromarray(eroded_subimage),
                 (int(pressed_x - bounded_img.shape[0] // 2),
                  int(pressed_y - bounded_img.shape[0] // 2)))  # 将b贴到a的坐标为（0,0）的位置，以图片左上角为坐标原点，这里说的是原点的移动
    bg_img = np.array(bg_img)
    bg_img = cv2.cvtColor(bg_img, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像

    # print(f"erode:{(x, y, x + width, y + height)}")


    screenshot = get_quad_grid(bg_img, min_sq=sq_size / (2 ** (quad_power+1)),
                               subimage_coord=(x, y, x + width, y + height))
    # Image.fromarray(screenshot).show()
    sub_photo = ImageTk.PhotoImage(Image.fromarray(screenshot))

    # sub_photo = ImageTk.PhotoImage(Image.fromarray(eroded_subimage))
    canvas.create_image(0, 0, anchor=tk.NW, image=sub_photo, tags="revealed_image")

    # 保留对sub_photo的引用
    canvas.sub_photo = sub_photo
    if not mouse_pressed and dilate_index <= max_erode:
        window.update()
        window.after(20, lambda: draw_erode(mouse_x, mouse_y))
    else:
        canvas.delete(tk.ALL)
        for i in range(1, n_row):  # horizontal lines
            canvas.create_line(0, grid_height * i, canvas_width, grid_height * i, fill='white')
        for j in range(1, n_col):
            canvas.create_line(grid_width * j, 0, grid_width * j, canvas_height, fill='white')


def on_mouse_press(pressed_x, pressed_y):
    global mouse_pressed, dilate_index, cropped_subimage
    global old_polygon
    # global pressed_x, pressed_y
    global max_dilate
    dilate_index = init_dilate
    # pressed_x, pressed_y = event.x, event.y

    # 现在开始1）裁剪图像 2）使用sub_image内的相对坐标
    x = max(0, pressed_x - max_sq_size // 2)
    y = max(0, pressed_y - max_sq_size // 2)
    width = min(max_sq_size, canvas_width - x)
    height = min(max_sq_size, canvas_height - y)
    sub_image = image_pil.crop((x, y, x + width, y + height))

    # 根据坐标获取mode
    mode = get_mode(pressed_x, pressed_y)
    max_dilate = max_dilate_ind[mode]
    # print(max_dilate)
    # if mode==3:
    #     max_sq_size = int(canvas_width // 4)
    # 为了让多边形的形状固定 先生成一个固定的“大多边形”
    sub_image = np.array(sub_image)
    sub_image_center = (sub_image.shape[0] // 2, sub_image.shape[1] // 2)
    old_polygon = Polygon_112(n=poly_n,
                              center=sub_image_center,
                              size=max_sq_size)
    cropped_subimage = crop_polygon(np.array(sub_image), old_polygon)
    #
    # mode = get_mode(x, y)
    # max_dilate = max_dilate_ind[mode]

    if not mouse_pressed:
        mouse_pressed = True
        draw_dilate(pressed_x, pressed_y,
                    init_sq_size)


def on_mouse_release(pressed_x, pressed_y):
    global mouse_pressed, dilate_index, cur_sq_size
    # global pressed_x, pressed_y
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
boundary_size = int(canvas_height)  # 膨胀界限
# max_sq_size = int(canvas_width // n_col)  # 图片扩大最大尺寸
max_sq_size = int(canvas_width//2)
init_sq_size = 10
poly_n = 15
poly_range = (init_sq_size, max_sq_size)
mouse_pressed = False
init_dilate = 5
max_erode = 10

k_size = 3
kernel = np.ones((k_size, k_size), np.uint8)
quad_power = 6

# set different mode param
max_dilate_ind = [-1, 3, 5, 100]
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


# # 绑定鼠标点击事件
# canvas.bind("<Button-1>", on_mouse_press)
# canvas.bind("<ButtonRelease-1>", on_mouse_release)
# canvas.delete("revealed_image")

# def check_continuous_press():
#     global last_time
#     current_time = time.time()
#     if current_time - last_time > 5:
#         # 在5秒内没有信号变动，认定为持续按压状态
#         # 这里可以添加你的逻辑处理
#         print("持续按压状态")
#     else:
#         # 信号变动较大，重新记录时间
#         last_time = current_time
#
#     # 清空坐标列表
#     coordinates.clear()
#
#     # 继续检查持续按压状态
#     root.after(5000, check_continuous_press)


#
# dilate_index = None
# mouse_pressed = False
#
# global dilate_index, mouse_pressed, old_polygon, mask
# global cropped_subimage, bounded_img, new_subimage
# global max_dilate, new_polygon, cur_sq_size
#     global mouse_pressed, dilate_index, cropped_subimage
#     global old_polygon
#     # global pressed_x, pressed_y
#     global max_dilate
#     dilate_index = init_dilate
mouse_pressed = False
# while(True):
dilate_index = init_dilate
pressed_x, pressed_y = (200, 200)
mouse_pressed = True
# if mouse_pressed:
# 现在开始1）裁剪图像 2）使用sub_image内的相对坐标
x = max(0, pressed_x - max_sq_size // 2)
y = max(0, pressed_y - max_sq_size // 2)
width = min(max_sq_size, canvas_width - x)
height = min(max_sq_size, canvas_height - y)
sub_image = image_pil.crop((x, y, x + width, y + height))

# 根据坐标获取mode
mode = get_mode(pressed_x, pressed_y)
max_dilate = max_dilate_ind[mode]
# print(max_dilate)
# if mode==3:
#     max_sq_size = int(canvas_width // 4)
# 为了让多边形的形状固定 先生成一个固定的“大多边形”
sub_image = np.array(sub_image)
sub_image_center = (sub_image.shape[0] // 2, sub_image.shape[1] // 2)
old_polygon = Polygon_112(n=poly_n,
                          center=sub_image_center,
                          size=max_sq_size)
cropped_subimage = crop_polygon(np.array(sub_image), old_polygon)

sq_size = init_sq_size
for i in range(10):
    sq_size = sq_size + 10
    draw_dilate(pressed_x, pressed_y, sq_size)
    window.update()
for i in range(10):
    draw_erode(pressed_x, pressed_y, sq_size)
    window.update()

# 运行主循环
window.mainloop()
