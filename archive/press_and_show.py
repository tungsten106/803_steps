from PIL import ImageTk, Image

from ver1_1_2_polygon.utils import *

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

# parameters
sq_size = 50
mouse_pressed = False
init_dilate = 9


def draw(mouse_x, mouse_y):
    global dilate_index, mouse_pressed
    canvas.delete("revealed_image")

    # if not mouse_pressed or dilate_index <= 0:
    #     return
    # 获取鼠标点击位置
    # 计算要显示的图像位置和大小
    x = max(0, mouse_x - sq_size // 2)
    y = max(0, mouse_y - sq_size // 2)
    width = min(sq_size, canvas_width - x)
    height = min(sq_size, canvas_width - y)
    sub_image = image_pil.crop((x, y, x + width, y + height))
    sub_image = np.array(sub_image)

    # 在画布上显示方块和图像
    # canvas.create_image(x, y, anchor=tk.NW, image=sub_photo, tags="revealed_image")
    k_size = 3
    kernel = np.ones((k_size, k_size), np.uint8)
    # dilate
    print(dilate_index)
    if mouse_pressed:
        dilate_index -= 1
        dilate_index = max(0, dilate_index)
        # print(dilate_index)
        # sub_image = cv2.dilate(sub_image, kernel, iterations=dilate_index)
        sub_image = dilate2(sub_image, dilate_index, 128 - 2 * dilate_index)
    # elif mouse_pressed and mouse_pressed > -2:
    #     dilate_index -= 1
    #     dilate_index = max(-2, dilate_index)
    #     print(dilate_index)
    #     sub_image = cv2.dilate(sub_image, kernel, iterations=abs(dilate_index))
    #erode
    else:
        dilate_index += 1
        dilate_index = min(10, dilate_index)
        sub_image = dilate2(sub_image, abs(dilate_index), 128 + 2 * dilate_index)
        # sub_image = cv2.erode(sub_image, kernel, iterations=dilate_index)
    sub_photo = ImageTk.PhotoImage(Image.fromarray(sub_image))
    canvas.create_image(x, y, anchor=tk.NW, image=sub_photo, tags="revealed_image")

    # 保留对sub_photo的引用
    canvas.sub_photo = sub_photo

    # # 延长效果
    # 调用自身，定时更新图像显示
    if mouse_pressed:
        window.update()
        window.after(80, lambda: draw(mouse_x, mouse_y))
    else:
        window.update()
        window.after(80, lambda: draw(mouse_x, mouse_y))


def mousePressed(event):
    # print("Mouse position: (%s %s)" % (event.x, event.y))
    global mouse_pressed, dilate_index
    canvas.delete("revealed_image")
    dilate_index = init_dilate
    x, y = event.x, event.y
    if not mouse_pressed:
        mouse_pressed = True
        draw(x, y)


def hide_image(event):
    global mouse_pressed, dilate_index
    x, y = event.x, event.y
    if mouse_pressed:
        mouse_pressed = False
        # canvas.delete("revealed_image")
        # dilate_index = init_dilate
        draw(x, y)




# 绑定鼠标点击事件
canvas.bind("<Button-1>", mousePressed)
# canvas.bind("<ButtonRelease-1>", hide_image)

# 运行主循环
window.mainloop()
