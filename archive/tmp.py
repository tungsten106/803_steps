import tkinter as tk
from PIL import Image, ImageTk

def increase_alpha():
    global alpha
    alpha += 30
    if alpha > 255:
        alpha = 255
    update_image()
    if alpha < 255 and mouse_pressed:
        window.after(100, increase_alpha)

def decrease_alpha():
    global alpha
    alpha -= 30
    if alpha < 0:
        alpha = 0
    update_image()
    if alpha > 0 and not mouse_pressed:
        window.after(100, decrease_alpha)

def update_image():
    img = Image.open("../xiaoyaoyou.jpeg")
    img = img.convert("RGBA")
    data = img.getdata()

    new_data = []
    for item in data:
        if item[3] > alpha:
            new_data.append((item[0], item[1], item[2], alpha))
        else:
            new_data.append(item)
    img.putdata(new_data)

    photo = ImageTk.PhotoImage(img)
    canvas.itemconfig(image_item, image=photo)
    canvas.image = photo

def on_mouse_press(event):
    global mouse_pressed
    mouse_pressed = True
    increase_alpha()

def on_mouse_release(event):
    global mouse_pressed
    mouse_pressed = False
    decrease_alpha()

window = tk.Tk()
window.title("图片透明度调整")

canvas = tk.Canvas(window, width=400, height=400, bg="black")
canvas.pack()

image = Image.open("../xiaoyaoyou.jpeg")
photo = ImageTk.PhotoImage(image)
image_item = canvas.create_image(200, 200, image = photo)

alpha = 0
mouse_pressed = False

canvas.bind("<ButtonPress-1>", on_mouse_press)
canvas.bind("<ButtonRelease-1>", on_mouse_release)

window.mainloop()
