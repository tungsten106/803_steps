from PIL import ImageTk, Image
from PIL import ImageGrab
from ref_csdn import *

from utils import *
from polygons_1_1_2 import *

"""
version2.1: 添加了产生quadtree的功能，尚未完善
"""


# TODO: 1）优先完成多边形 # complete!
#       2）完成quadtree
#       3）不同区域的效果
#       4）连接雷达
# TODO: 上传github


def draw_dilate(mouse_x, mouse_y, sq_size):
    global dilate_index, mouse_pressed, old_polygon, mask
    global cropped_subimage
    if not mouse_pressed:
        return
    # print("dilate!")
    # 获取鼠标点击位置
    # 计算要显示的图像位置和大小
    x = max(0, mouse_x - max_sq_size // 2)
    y = max(0, mouse_y - max_sq_size // 2)
    # 设置“mask”
    # width = min(sq_size, canvas_width - x)
    # height = min(sq_size, canvas_height - y)
    # sub_image = image_pil.crop((x, y, x + width, y + height))
    # # sub_image = np.array(sub_image)
    # print(np.sum(sub_image))
    # Image.fromarray(sub_image).show()

    # 裁剪多边形
    new_polygon = old_polygon.update_polygon(sq_size)

    # print(new_polygon.distances)
    cropped_sub_small = crop_polygon(np.array(cropped_subimage),
                                     new_polygon)
    # Image.fromarray(cropped_sub_small).show()
    # Image.fromarray(cropped_subimage).show()

    # dilate
    dilate_index -= 1
    dilate_index = max(0, dilate_index)
    cropped_sub_small = dilate2(cropped_sub_small, dilate_index, 128 - 2 * dilate_index)
    # screenshot = get_screenshot(canvas)
    # screenshot.show()

    # sub_photo = ImageTk.PhotoImage(Image.fromarray(cropped_sub_small))
    # canvas.create_image(x, y, anchor=tk.NW, image=sub_photo, tags="revealed_image")
    pil_cropped_sub_small = Image.fromarray(cropped_sub_small)
    mask.paste(pil_cropped_sub_small, (x, y))
    # mask.show()
    screenshot = np.array(mask)
    # screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    matrix = screenshot
    row = matrix.shape[0]
    col = matrix.shape[1]
    first_square = square(0, 0, row - 1, col - 1)
    square_arr = [first_square]
    square_arr = get_quad_tree(matrix, square_arr, min_sq=sq_size / (2 ** 2))
    for i in square_arr:
        for col in range(i.ly, i.ry):
            screenshot[i.rx][col] = 255
        for row in range(i.lx, i.rx):
            screenshot[row][i.ry] = 255
    # Image.fromarray(screenshot).show()
    screenshot_photo = ImageTk.PhotoImage(Image.fromarray(screenshot))
    canvas.create_image(0, 0, anchor=tk.NW, image=screenshot_photo, tags="revealed_mask")

    # 保留对sub_photo的引用
    # canvas.sub_photo = sub_photo
    canvas.screenshot_photo = screenshot_photo
    if mouse_pressed:
        window.update()
        window.after(80, lambda: draw_dilate(mouse_x, mouse_y, min(sq_size + 10, 50)))


def draw_erode(mouse_x, mouse_y, sq_size):
    global dilate_index, mouse_pressed, cropped_subimage
    if mouse_pressed:
        return
    # print("erode!")
    # 获取鼠标点击位置
    # 计算要显示的图像位置和大小
    # create subimage
    x = max(0, mouse_x - sq_size // 2)
    y = max(0, mouse_y - sq_size // 2)
    # width = min(sq_size, canvas_width - x)
    # height = min(sq_size, canvas_width - y)
    # sub_image = image_pil.crop((x, y, x + width, y + height))
    # sub_image = np.array(sub_image)

    k_size = 2
    kernel = np.ones((k_size, k_size), np.uint8)
    # 开始腐蚀
    # sub_image = dilate2(sub_image, abs(dilate_index), 128 + 2 * dilate_index)
    eroded_subimage = cv2.erode(cropped_subimage, kernel, iterations=dilate_index)

    sub_photo = ImageTk.PhotoImage(Image.fromarray(eroded_subimage))
    canvas.create_image(x, y, anchor=tk.NW, image=sub_photo, tags="revealed_image")

    # 更新参数
    dilate_index += 1
    dilate_index = min(10, dilate_index)
    # 保留对sub_photo的引用
    canvas.sub_photo = sub_photo
    if not mouse_pressed:
        window.update()
        window.after(150, lambda: draw_erode(mouse_x, mouse_y, sq_size))


def on_mouse_press(event):
    global mouse_pressed, dilate_index, cropped_subimage, mask
    global old_polygon
    dilate_index = init_dilate
    pressed_x, pressed_y = event.x, event.y


    # init_sq_size = 5
    # 现在开始1）裁剪图像 2）使用sub_image内的相对坐标
    x = max(0, pressed_x - max_sq_size // 2)
    y = max(0, pressed_y - max_sq_size // 2)
    width = min(max_sq_size, canvas_width - x)
    height = min(max_sq_size, canvas_height - y)
    sub_image = image_pil.crop((x, y, x + width, y + height))

    # 设置蒙版
    mask = Image.new('L', (canvas_width, canvas_height), color=0)

    # 为了让多边形的形状固定 先生成一个固定的“大多边形”
    sub_image = np.array(sub_image)
    sub_image_center = (sub_image.shape[0] // 2, sub_image.shape[1] // 2)
    old_polygon = Polygon_112(n=poly_n,
                              center=sub_image_center,
                              size=max_sq_size)
    cropped_subimage = crop_polygon(np.array(sub_image), old_polygon)
    if not mouse_pressed:
        mouse_pressed = True
        draw_dilate(pressed_x, pressed_y,
                    init_sq_size)


def on_mouse_release(event):
    global mouse_pressed, dilate_index
    x, y = event.x, event.y
    if mouse_pressed:
        mouse_pressed = False
        draw_erode(x, y, max_sq_size)
    # canvas.delete("revealed_image")


# 创建主窗口
window = tk.Tk()
window.title("Image Revealer")
window.configure(bg="black")

# 加载图片
image_path = "pics/calligraphy.JPG"  # 替换为你的图片路径
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
max_sq_size = 50
init_sq_size = 10
poly_n = 15
poly_range = (init_sq_size, max_sq_size)
mouse_pressed = False
init_dilate = 9

# 绑定鼠标点击事件
canvas.bind("<Button-1>", on_mouse_press)
canvas.bind("<ButtonRelease-1>", on_mouse_release)

# 运行主循环
window.mainloop()
