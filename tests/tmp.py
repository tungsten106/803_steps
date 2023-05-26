import cv2

image_path = "../pics/803step.bmp"  # 图片路径
matrix = cv2.imread(image_path)
matrix = cv2.cvtColor(matrix, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像
# matrix = color_inv(matrix)
row = matrix.shape[0]//2
col = matrix.shape[1]//2

lx, ly, rx, ry = 0, 0, row - 1, col - 1

print(matrix.shape)