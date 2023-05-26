from polygons_1_1_2 import *
from prev_vers.quad_tree_csdn import *
import cv2


# 创建主窗口
window = tk.Tk()
window.title("Image Revealer")
window.configure(bg="black")

# 设置画布大小
canvas_width = 1086
canvas_height = 600

# 加载图片
image_path = "../pics/803step.bmp"  # 图片路径
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像
image = color_inv(image)
image.resize(new_shape=(200,200))




