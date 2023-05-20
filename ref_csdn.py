import numpy as np
import cv2
from PIL import ImageTk, Image
from utils import *


# 正方形类
class square:
    # lx、ly为左上角坐标(x对应行号，y对应列号)，rx、ry为右下角坐标
    def __init__(self, lx, ly, rx, ry):
        self.lx = lx
        self.ly = ly
        self.rx = rx
        self.ry = ry

    # 检查该矩阵中是否满足条件
    # 参数：原矩阵，阈值
    # 返回值：布尔类型
    def check(self, matrix, threshold, min_sq_size=10):
        # 小于10的块就不再分了，太小没啥意义
        if abs(self.rx - self.lx) <= min_sq_size:
            return True
        min = matrix[self.lx][self.ly]
        max = matrix[self.lx][self.ly]
        for i in range(self.lx, self.rx):
            for j in range(self.ly, self.ry):
                if matrix[i][j] < min:
                    min = matrix[i][j]
                if matrix[i][j] > max:
                    max = matrix[i][j]
        if abs(max - min) >= threshold:
            return False
        return True

    # 打印正方形的坐标
    def print(self):
        print("lx:", self.lx, end=", ")
        print("ly:", self.ly, end=", ")
        print("rx:", self.rx, end=", ")
        print("ry:", self.ry)


# 检查所有块里面是否还有不行的
# 参数：原矩阵、正方形对象列表
# 返回值：若有不行的，返回对象和下标；否则返回空对象
def check_all(matrix, square_arr, min_sq=5):
    for i in range(len(square_arr)):
        if square_arr[i].check(matrix, 10, min_sq_size=min_sq) == False:  # 阈值在此设置
            return square_arr[i], i
    return None, -1


# 得到最终的四叉树
def get_quad_tree(matrix, square_arr, min_sq=5):
    while (True):
        problem_block, index = check_all(matrix, square_arr, min_sq=min_sq)
        if problem_block == None:
            break
        lx = problem_block.lx
        ly = problem_block.ly
        rx = problem_block.rx
        ry = problem_block.ry
        # 左上角
        divide_block1 = square(lx, ly, (lx + rx) // 2, (ly + ry) // 2)
        # 右上角
        divide_block2 = square(lx, (ly + ry) // 2 + 1, (lx + rx) // 2, ry)
        # 左下角
        divide_block3 = square((lx + rx) // 2 + 1, ly, rx, (ly + ry) // 2)
        # 右下角
        divide_block4 = square((lx + rx) // 2 + 1, (ly + ry) // 2 + 1, rx, ry)

        # 检验结果是否正确
        # print("拆分前：")
        # square_arr[index].print()
        # print("拆分后：")
        # divide_block1.print()
        # divide_block2.print()
        # divide_block3.print()
        # divide_block4.print()

        # 删掉原来的大矩阵，把新的四个子矩阵加进列表
        del square_arr[index]
        square_arr.append(divide_block1)
        square_arr.append(divide_block2)
        square_arr.append(divide_block3)
        square_arr.append(divide_block4)
    return square_arr


def resize(img, size):
    # print('src shape: ', img.shape)
    height = img.shape[0]
    width = img.shape[1]
    scalesize = 256.0

    timg = img
    if height > width:
        timg = cv2.resize(img, (256, int(scalesize * height / width)))
    else:
        timg = cv2.resize(img, (int(scalesize * width / height), 256))

    # print('timg shape: ', timg.shape)
    th = timg.shape[0]
    tw = timg.shape[1]
    bh = int((th - size) / 2)
    bw = int((tw - size) / 2)
    rimg = timg[bh:bh + size, bw:bw + size]
    # print('rimg shape: ', rimg.shape)
    return rimg

#
# # mask_np = cv2.imread('pics/xiaoyaoyou.jpeg',0)
# image_path = "pics/xiaoyaoyou.jpeg"  # 替换为你的图片路径
# image = cv2.imread(image_path)
# image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像
# image = color_inv(image)
# mask_np = image
# mask_np = resize(mask_np, 224)
# matrix = mask_np
#
# min_sq = 3
# row = matrix.shape[0]
# col = matrix.shape[1]
# first_square = square(0, 0, row - 1, col - 1)
# square_arr = [first_square]
# square_arr = get_quad_tree(matrix, square_arr, min_sq)
#
# # 划分界限，方便看
# for i in square_arr:
#     for col in range(i.ly, i.ry):
#         mask_np[i.rx][col] = 255
#     for row in range(i.lx, i.rx):
#         mask_np[row][i.ry] = 255
#
# Image.fromarray(mask_np).show()
# cv2.imwrite('/result.png', mask_np)



# # print(matrix)
# # print("最终得到的各种分块如下：")
# # for i in square_arr:
# #     i.print()
#
#
# # ref: https://blog.csdn.net/weixin_44164489/article/details/112853121
