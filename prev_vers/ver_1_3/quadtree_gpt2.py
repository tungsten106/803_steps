from tkinter import *
import math
import noise

posx, posy, variation = 0.0, 0.0, 0.0
maxRectSize, minRectSize = 0.0, 0.0
stackDepth = 0


def setup():
    global maxRectSize, minRectSize, stackDepth
    global window_width, window_height
    window_width, window_height = 800, 600
    stackDepth = 9
    maxRectSize = max(window_width, window_height)
    minRectSize = maxRectSize / (2 ** stackDepth)


def draw():
    global variation
    variation += 0.005
    quadTree(window_width / 2, window_height / 2, maxRectSize * 2)


def mouseDragged(event):
    global posx, posy
    posx += event.x - event.x_root
    posy += event.y - event.y_root


def quadTree(x, y, size):
    if size < minRectSize:
        return

    # n = noise((x + posx) * 0.001, (y + posy) * 0.001, variation)
    n = noise.snoise3((x + posx) * 0.001, (y + posy) * 0.001, variation)
    if abs(n - 0.45) > size / maxRectSize:
        canvas.create_rectangle(x - size / 2, y - size / 2, x + size / 2, y + size / 2, outline="black")
    else:
        size /= 2
        d = size / 2
        quadTree(x + d, y + d, size)
        quadTree(x + d, y - d, size)
        quadTree(x - d, y + d, size)
        quadTree(x - d, y - d, size)


# 创建Tkinter窗口
window = Tk()
window.title("QuadTree")
canvas = Canvas(window, width=800, height=600)
canvas.pack()

# 设置处理函数
canvas.bind("<B1-Motion>", mouseDragged)

# 调用setup函数进行初始化
setup()

# 进入主循环
while True:
    canvas.delete("all")
    draw()
    window.update()
