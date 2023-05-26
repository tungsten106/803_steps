from PIL import ImageTk, Image

from prev_vers.ver1_1_2_polygon.utils import *
from old.polygons import *

"""version1.0: 满足了效果的基本要求，下面需要微调
"""


def draw_dilate(mouse_x, mouse_y):
    global dilate_index, mouse_pressed, dilate_speed, sub_image
    if not mouse_pressed:
        return
    # print("dilate!")
    # 获取鼠标点击位置
    # 计算要显示的图像位置和大小
    # x = max(0, mouse_x - sq_size // 2)
    # y = max(0, mouse_y - sq_size // 2)
    # width = min(sq_size, canvas_width - x)
    # height = min(sq_size, canvas_width - y)
    # sub_image = image_pil.crop((x, y, x + width, y + height))
    # sub_image = np.array(sub_image)
    x = int(canvas_width//2) * int(mouse_x//(canvas_width//2))
    y = int(canvas_height//2) * int(mouse_y//(canvas_height//2))
    # print(x, y)
    width = min(sq_size, canvas_width - x)
    height = min(sq_size, canvas_width - y)
    sub_image = image_pil.crop((x, y, x + width, y + height))

    # sub_image = image_pil.crop((x, y, int(canvas_width//2), int(canvas_height//2)))
    cropped_subimage = np.array(sub_image)

    # 裁剪多边形
    # cropped_subimage = crop_polygon(np.array(sub_image), 20)

    k_size = 3
    kernel = np.ones((k_size, k_size), np.uint8)
    # dilate
    # print(dilate_index)
    dilate_index -= step
    dilate_index = max(0, dilate_index)
    # print(dilate_index)
    # sub_image = cv2.dilate(sub_image, kernel, iterations=dilate_index)
    # sub_image = dilate2(sub_image, dilate_index, 128 - 2 * dilate_index)
    # sub_image = dilate_polygon(sub_image, dilate_index, 128 - 2 * dilate_index,
    #                            polygon)
    sub_image = dilate2(cropped_subimage, dilate_index, 128 - 2 * dilate_index)

    sub_photo = ImageTk.PhotoImage(Image.fromarray(sub_image))
    canvas.create_image(x, y, anchor=tk.NW, image=sub_photo, tags="revealed_image")

    # 保留对sub_photo的引用
    canvas.sub_photo = sub_photo
    if mouse_pressed:
        window.update()
        window.after(dilate_speed, lambda: draw_dilate(mouse_x, mouse_y))


def draw_erode(mouse_x, mouse_y):
    global dilate_index, mouse_pressed, erode_speed, sub_image
    if mouse_pressed:
        return
    # print("erode!")
    # 获取鼠标点击位置
    # 计算要显示的图像位置和大小
    # create subimage
    # x = max(0, mouse_x - sq_size // 2)
    # y = max(0, mouse_y - sq_size // 2)
    # width = min(sq_size, canvas_width - x)
    # height = min(sq_size, canvas_width - y)
    # sub_image = image_pil.crop((x, y, x + width, y + height))
    # sub_image = np.array(sub_image)
    x = int(canvas_width//2) * int(mouse_x//(canvas_width//2))
    y = int(canvas_height//2) * int(mouse_y//(canvas_height//2))
    # sub_image = image_pil.crop((x, y, int(canvas_width//2), int(canvas_height//2)))
    # sub_image = np.array(sub_image)
    k_size = 5
    kernel = np.ones((k_size, k_size), np.uint8)
    # 开始腐蚀
    # sub_image = dilate2(sub_image, abs(dilate_index), 128 + 2 * dilate_index)
    # print(sub_image)
    sub_image = cv2.erode(sub_image, kernel, iterations=dilate_index)

    sub_photo = ImageTk.PhotoImage(Image.fromarray(sub_image))
    canvas.create_image(x, y, anchor=tk.NW, image=sub_photo, tags="revealed_image")

    # 更新参数
    dilate_index += step
    dilate_index = min(max_erode, dilate_index)
    # 保留对sub_photo的引用
    canvas.sub_photo = sub_photo
    if not mouse_pressed:
        window.update()
        window.after(erode_speed, lambda: draw_erode(mouse_x, mouse_y))

def on_mouse_press(event):
    # print("Mouse position: (%s %s)" % (event.x, event.y))
    global mouse_pressed, dilate_index, dilate_speed
    x, y = event.x, event.y
    # dilate_index = init_dilate
    dilate_index = mode_finder(x, y)
    dilate_speed, erode_speed = speed_finder(x, y)
    if not mouse_pressed:
        mouse_pressed = True
        draw_dilate(x, y)


def on_mouse_release(event):
    global mouse_pressed, dilate_index, erode_speed, sub_image
    x, y = event.x, event.y

    dilate_speed, erode_speed = speed_finder(x, y)
    if mouse_pressed:
        mouse_pressed = False
        draw_erode(x, y)
    # canvas.delete("revealed_image")

def speed_finder(x, y):
    # zone1
    if x <= canvas_width//2 and y <= canvas_height//2:
        dilate_speed = speed_fast[0]
        erode_speed = speed_fast[1]
    # zone2
    elif x <= canvas_width//2 and y > canvas_height//2:
        dilate_speed = speed_fast[0]
        erode_speed = speed_slow[1]
    elif x > canvas_width//2 and y <= canvas_height//2:
        dilate_speed = speed_slow[0]
        erode_speed = speed_fast[1]
    else:
        dilate_speed = speed_slow[0]
        erode_speed = speed_slow[1]
    return dilate_speed, erode_speed

def mode_finder(x, y):
    # mode1, out of bound
    if x <= canvas_width//2 and y <= canvas_height//2:
        init_dilate = 45
    # mode 2,
    elif x <= canvas_width//2 and y > canvas_height//2:
        init_dilate = 25
    elif x > canvas_width//2 and y <= canvas_height//2:
        init_dilate = 15
    else:
        init_dilate = 10
    return init_dilate
# 创建主窗口
window = tk.Tk()
window.title("Image Revealer")
window.configure(bg="black")

# 加载图片
image_path = "../../pics/803step.bmp"  # 替换为你的图片路径
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

# parameters
sq_size = canvas_width//2
mouse_pressed = False
init_dilate = 25
max_erode = 50
step = 5
speed_fast = (50, 20) # dilate, erode
speed_slow = (200, 200)

# 绑定鼠标点击事件
canvas.bind("<Button-1>", on_mouse_press)
canvas.bind("<ButtonRelease-1>", on_mouse_release)

# 运行主循环
window.mainloop()
