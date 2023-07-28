from polygons_1_1_2 import *
from quad_tree_csdn_59 import *
import cv2
import serial
import time
import struct
import serial.tools.list_ports
from Xen202TT01 import Radar

"""
version final!! WORKED with interactive device!
combine programme & position signal input script
version5.3.1+Xen202TT01
"""

# 雷达设定（by林彦
serial_port = "COM31"

pack_len = 30
pack_head = b'\xAA\xFF\03\00'
cmd_multi = b'\xFD\xFC\xFB\xFA\x02\x00\x90\x00\x04\x03\x02\x01'
cmd_single = b'\xFD\xFC\xFB\xFA\x02\x00\x80\x00\x04\x03\x02\x01'

reply_multi = b'\xFD\xFC\xFB\xFA\x04\x00\x90\x01\x01\x00\x04\x03\x02\x01'
reply_single = b'\xFD\xFC\xFB\xFA\x04\x00\x80\x01\x01\x00\x04\x03\x02\x01'


def gen_bg_img(image):
    bg_img = Image.new("RGB", (int(canvas_height // 5 * 16), int(canvas_height // 5 * 8)), "black")
    bg_img.paste(Image.fromarray(image),
                 (int(pressed_x - image.shape[0] // 2),
                  int(pressed_y - image.shape[1] // 2)))  # 将b贴到a的坐标为（0,0）的位置，以图片左上角为坐标原点，这里说的是原点的移动
    bg_img = np.array(bg_img)
    # print(bg.img)
    bg_img = cv2.cvtColor(bg_img, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像
    return bg_img


def gen_grid(canvas):
    for i in range(1, n_row):  # horizontal lines
        canvas.create_line(0, grid_height * i, canvas_width, grid_height * i, fill='white')
    for j in range(1, n_col):
        canvas.create_line(grid_width * j, 0, grid_width * j, canvas_height, fill='white')
    return


# 特效函数s
def draw_dilate(sq_size):
    '''
    add dilate effect to original work
    :param sq_size: side of square cropped from original image
    :return: None
    '''
    global dilate_index, mouse_pressed, old_polygon, mask
    global cropped_subimage, bounded_img, new_subimage
    global max_dilate, new_polygon, cur_sq_size

    cur_sq_size = sq_size

    # 计算要显示的图像位置和大小
    x = pressed_x - sq_size // 2
    y = pressed_y - sq_size // 2
    width = sq_size
    height = sq_size
    new_subimage = image_pil.crop((x, y, x + width, y + height))
    new_subimage = np.array(new_subimage)

    # crop original image
    new_polygon = Polygon_112(n=poly_n,
                              size=sq_size,
                              center=(width // 2, height // 2),
                              angles=old_polygon.angles,
                              distances=old_polygon.distances / max_sq_size * sq_size)
    cropped_subimage = crop_polygon(new_subimage, new_polygon)

    # add a black boundary to make stronger effect
    boundary_size = int(sq_size * 1.5)
    bounded_img = Image.new("RGB", (boundary_size, boundary_size), "black")
    new_x, new_y = int(boundary_size // 2 - (sq_size // 2)), int(boundary_size // 2 - (sq_size // 2))
    bounded_img.paste(Image.fromarray(cropped_subimage),
                      (new_x, new_y))

    bounded_img = np.array(bounded_img)
    bounded_img = cv2.cvtColor(bounded_img, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像  # 裁剪后的原图

    # start dilate by different mode (1-4)
    if max_dilate < 0:  # mode
        dilate_index = max(abs(max_dilate), dilate_index)
        dilated_img = cv2.erode(bounded_img, kernel, iterations=dilate_index)
        dilate_index -= 1
    else:
        if dilate_index >= 0:
            dilated_img = dilate3(bounded_img, dilate_index, 128 - 2 * dilate_index,
                                  step=init_sq_size // 10)
            dilate_index -= 1
        else:
            # print(dilate_index, max_dilate)
            dilate_index = max(0 - max_dilate, dilate_index)
            dilated_img = cv2.dilate(bounded_img, kernel, iterations=abs(dilate_index))
            dilate_index -= cv2_dilate_step

    bg_img = gen_bg_img(dilated_img)

    # find boundary locs
    x_b = pressed_x - boundary_size // 2
    y_b = pressed_y - boundary_size // 2
    w_b = boundary_size
    h_b = boundary_size
    if get_mode(pressed_x, pressed_y) == 3:
        screenshot = get_quad_grid(bg_img, min_sq=init_sq_size / (2 ** (quad_power)),
                                   subimage_coord=(x_b, y_b, x_b + w_b, y_b + h_b),
                                   canvas_width=canvas_width,
                                   canvas_height=canvas_height)
    else:
        screenshot = get_quad_grid(bg_img, min_sq=init_sq_size / (2 ** (quad_power)),
                                   subimage_coord=(x, y, x + width, y + height),
                                   canvas_width=canvas_width,
                                   canvas_height=canvas_height)

    sub_photo = ImageTk.PhotoImage(Image.fromarray(screenshot))

    canvas.create_image(0, 0, anchor=tk.NW, image=sub_photo, tags="revealed_image")
    gen_grid(canvas)

    # 保留对sub_photo的引用
    canvas.sub_photo = sub_photo
    return


def draw_erode(sq_size):
    global dilate_index, mouse_pressed, new_subimage
    global cur_sq_size, new_polygon
    global pressed_x, pressed_y, bounded_img
    if mouse_pressed:
        return
    # 计算要显示的图像位置和大小
    # sq_size = cur_sq_size
    # x = max(0, pressed_x - sq_size // 2)
    # y = max(0, pressed_y - sq_size // 2)
    # width = min(sq_size, canvas_width - x)
    # height = min(sq_size, canvas_height - y)
    x = pressed_x - sq_size // 2
    y = pressed_y - sq_size // 2
    width = sq_size
    height = sq_size
    # print("erode bounded", bounded_img.shape)

    # 开始腐蚀
    # sub_image = dilate2(sub_image, abs(dilate_index), 128 + 2 * dilate_index)
    if dilate_index < 0:
        # 更新参数
        dilate_index += cv2_dilate_step
        eroded_subimage = cv2.dilate(bounded_img, kernel, iterations=abs(dilate_index))
    else:
        dilate_index += 1
        eroded_subimage = cv2.erode(bounded_img, kernel, iterations=dilate_index)

    bg_img = gen_bg_img(eroded_subimage)

    # print(f"erode:{(x, y, x + width, y + height)}")
    boundary_size = int(sq_size * 1.5)
    if get_mode(pressed_x, pressed_y) == 3:
        x_b = pressed_x - boundary_size // 2
        y_b = pressed_y - boundary_size // 2
        w_b = boundary_size
        h_b = boundary_size
        screenshot = get_quad_grid(bg_img, min_sq=init_sq_size / (2 ** (quad_power)),
                                   subimage_coord=(x_b, y_b, x_b + w_b, y_b + h_b),
                                   canvas_width=canvas_width,
                                   canvas_height=canvas_height)
    else:
        screenshot = get_quad_grid(bg_img, min_sq=init_sq_size / (2 ** (quad_power)),
                                   subimage_coord=(x, y, x + width, y + height),
                                   canvas_width=canvas_width,
                                   canvas_height=canvas_height)
    sub_photo = ImageTk.PhotoImage(Image.fromarray(screenshot))

    canvas.create_image(0, 0, anchor=tk.NW, image=sub_photo, tags="revealed_image")
    gen_grid(canvas)

    # 保留对sub_photo的引用
    canvas.sub_photo = sub_photo
    return


# 鼠标函数s
def on_mouse_press(pressed_x, pressed_y,
                   sq_size=10):
    global dilate_index, cropped_subimage
    global old_polygon, bounded_img
    # global pressed_x, pressed_y
    global max_dilate, coord_list, last_coord
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
    if not 0 <= mode < 4:
        return
    # if not mode:
    #     return
    max_dilate = max_dilate_ind[mode]
    # 为了让多边形的形状固定 先生成一个固定的“大多边形”
    sub_image = np.array(sub_image)
    sub_image_center = (sub_image.shape[0] // 2, sub_image.shape[1] // 2)
    old_polygon = Polygon_112(n=poly_n,
                              center=sub_image_center,
                              size=max_sq_size)
    cropped_subimage = crop_polygon(np.array(sub_image), old_polygon)
    bounded_img = cropped_subimage
    # mouse_pressed = True
    # for i in range(n_iters):
    # while dilate_index > -max_dilate:
    #     print(dilate_index, max_dilate)
    # print()
    # print(mouse_pressed, (pressed_x, pressed_y))

    last_coord = (pressed_x, pressed_y)
    radar.update()
    cur_coord = mapping_position(radar.x, radar.y)
    # pressed_x, pressed_y = cur_coord
    # sq_size = init_sq_size
    # moved = np.linalg.norm(np.array(cur_coord) - np.array(last_coord))
    # is_in_domain = cv2.pointPolygonTest(input_points,
    #                                     tuple([radar.x, radar.y]), False)
    # pressed_x, pressed_y = mapping_position(radar.x, radar.y)
    # is_in_range =cv2.pointPolygonTest(output_points,
    #                                   (pressed_x, pressed_y), False)
    # for i in range(10):
    #     sq_size = min(int(sq_size * 1.1), max_sq_size)
    #     draw_dilate(sq_size)
    #     window.update()
    while check_loc_range(last_coord) and \
            check_loc_range(cur_coord) and \
            (np.linalg.norm(np.array(cur_coord) - np.array(last_coord)) <= 1.5 * grid_height):
        sq_size = min(int(sq_size * 1.1), max_sq_size)
        draw_dilate(sq_size)
        window.update()
        radar.update()
        cur_coord = mapping_position(radar.x, radar.y)
    while dilate_index <= max_erode:
        draw_erode(sq_size)
        window.update()
    canvas.delete(tk.ALL)
    for i in range(1, n_row):  # horizontal lines
        canvas.create_line(0, grid_height * i, canvas_width, grid_height * i, fill='white')
    for j in range(1, n_col):
        canvas.create_line(grid_width * j, 0, grid_width * j, canvas_height, fill='white')


def get_mode(x, y):
    try:
        # output = mode_table[int(y // grid_width)][int(x // grid_height)] - 1
        output = mode_table[int(y // grid_height)][int(x // grid_width)] - 1
        print(output)
        return output
    # return mode_table[int(y // grid_width)][int(x // grid_height)] - 1
    except IndexError:
        print("error:", [int(y // grid_height), int(x // grid_width)])


# 选择端口
port_list = list(serial.tools.list_ports.comports())
print("\nDetected COM ports:")
for i in range(0, len(port_list)):
    print("	[ID:{}] {}".format(i, port_list[i]))
inputerror = True  # will be turned to False when the input is correct
selected = input("Please select the port which you want to open, ID:")
if selected.isdigit():
    if int(selected) < len(port_list):
        selected_com = port_list[int(selected)]
        print("\nOpening: {}\n".format(selected_com))
        inputerror = False
if inputerror:
    print("\nInput error! Please only input the ID number in the list above.")
    exit()

radar = Radar(selected_com[0])
# 创建主窗口
window = tk.Tk()
window.title("Image Revealer")
window.configure(bg="black")

# 设置画布大小
canvas_width = 1086
canvas_height = 600
# canvas_width = 1920
# canvas_height = 1080

n_row = 5
n_col = 9
canvas_width = int(canvas_width // n_col * n_col)
canvas_height = int(canvas_height // n_row * n_row)
# print(canvas_width, canvas_height)

# 加载图片 改变图片大小
image_path = "pics/calligraphy.JPG"  # 图片路径
# image_path = "../../Downloads/xiaoyaoyou_ver_5_new/pics/xiaoyaoyou_new.jpg"
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
# boundary_size = int(canvas_width)  # 膨胀界限
# max_sq_size = int(canvas_width // n_col)  # 图片扩大最大尺寸
# max_sq_size = int(canvas_height // 5 * 4)
max_sq_size = canvas_height
init_sq_size = int(max_sq_size // 10)
poly_n = 20
poly_range = (init_sq_size, max_sq_size)
mouse_pressed = False
init_dilate = 5
max_erode = 10
cv2_dilate_step = 5

k_size = 3
kernel = np.ones((k_size, k_size), np.uint8)
quad_power = 7

# set different mode param
max_dilate_ind = [-1, 3, 5, 450]
mode_table = np.array(
    [
        [2, 2, 2, 3, 4, 2, 1, 4, 4],
        [2, 2, 2, 1, 1, 3, 1, 4, 4],
        [2, 2, 2, 1, 1, 4, 2, 1, 2],
        [4, 4, 3, 1, 2, 2, 1, 3, 3],
        [4, 4, 2, 4, 2, 2, 2, 3, 3]
    ]
)

for i in range(1, n_row):  # horizontal lines
    canvas.create_line(0, grid_height * i, canvas_width, grid_height * i, fill='white')
for j in range(1, n_col):
    canvas.create_line(grid_width * j, 0, grid_width * j, canvas_height, fill='white')
window.update()
# new: ver5.3
mouse_pressed = False
dilate_index = init_dilate
# print("Radar preparing...")
# for i in range(10):
#     radar.update()
#     print(radar.x, radar.y)
# print("Done!")
while True:
    radar.update()

    # pressed_x, pressed_y = radar.x, radar.y
    print(radar.x, radar.y)
    is_in_domain = cv2.pointPolygonTest(input_points,
                                        tuple([radar.x, radar.y]), False)
    pressed_x, pressed_y = mapping_position(radar.x, radar.y)
    is_in_range = cv2.pointPolygonTest(output_points,
                                       (pressed_x, pressed_y), False)
    if is_in_domain <= 0 or is_in_range <= 0:
        # while not lx <= radar.x < rx and ly<= radar.y < ry:
        #     radar.update()
        # pressed_x, pressed_y = radar.x, radar.y
        # print(pressed_x, pressed_y)
        radar.update()
    else:
        # print(mapping_position(radar.x, radar.y))
        # pressed_x, pressed_y = mapping_position(radar.x, radar.y)
        sq_size = init_sq_size
        on_mouse_press(pressed_x, pressed_y, sq_size=init_sq_size)

    canvas.delete(tk.ALL)

    for i in range(1, n_row):  # horizontal lines
        canvas.create_line(0, grid_height * i, canvas_width, grid_height * i, fill='white')
    for j in range(1, n_col):
        canvas.create_line(grid_width * j, 0, grid_width * j, canvas_height, fill='white')
    window.update()
# 运行主循环
window.mainloop()

# with open("input2.txt") as f:
#     coord_list = []
#     for line in f:
#         coord_list.append((tuple([int(a) for a in line.rstrip('\n').split(" ")])))


# def tmp_get():
#     global coord_list
#     return coord_list.pop(0)

#
# while coord_list:
#     pressed_x, pressed_y = coord_list[0]
#     print(pressed_x, pressed_y)
#     sq_size = init_sq_size
#     on_mouse_press(pressed_x, pressed_y, sq_size=init_sq_size)
#     canvas.delete(tk.ALL)
