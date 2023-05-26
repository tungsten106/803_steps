import cv2
from quad_tree_csdn_new import *

image_path = "../pics/803step.jpg"  # 替换为你的图片路径
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像
image = color_inv(image)
mask_np = image
# mask_np = resize(mask_np, 224)
matrix = mask_np

min_sq = 3
row = matrix.shape[0]
col = matrix.shape[1]
first_square = square(0, 0, row - 1, col - 1)
square_arr = [first_square]
square_arr = get_quad_tree(matrix, square_arr, min_sq,
                           subimage_coord=(0,0, 170, 260))

# 划分界限，方便看
for i in square_arr:
    for col in range(i.ly, i.ry):
        mask_np[i.rx][col] = 255
    for row in range(i.lx, i.rx):
        mask_np[row][i.ry] = 255

Image.fromarray(mask_np).show()