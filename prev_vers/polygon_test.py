from old.polygons import *
def draw_polygon(canvas, polygon):
    vertices = polygon.vertices
    # polygon.vertices = polygon.fix_vertex_order(polygon.vertices)

    canvas.create_polygon(vertices, outline='black', fill='gray', width=2)


# 创建Tkinter窗口和Canvas
# # 创建Tkinter窗口和Canvas
window = tk.Tk()
canvas = tk.Canvas(window, width=400, height=400)
canvas.pack()
# #
# # # 创建一个多边形对象
polygon = Polygon(8, 100, (200, 200))
point = (200, 100)
px, py = point
print(polygon.is_in_polygon(point))  # 判断点是否在多边形内部

#
# # 在Canvas上绘制多边形
# # canvas.bind("<Button-1>", on_mouse_press)
#
# #
# draw_polygon(canvas, polygon)
vertices = polygon.vertices

canvas.create_polygon(vertices, outline='black', fill='white', width=1)




# mouse event: test if is_in_poly() correct -> correct!
def on_mouse_press(event):

    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    canvas.create_oval(x1, y1, x2, y2, fill="#476042")
    print(polygon.is_in_poly((event.x, event.y)))

    # draw_polygon(canvas, polygon)
    # print(polygon.is_in_polygon((50,50)))
# 在Canvas上绘制多边形
canvas.bind("<Button-1>", on_mouse_press)
# 启动主循环
window.mainloop()





