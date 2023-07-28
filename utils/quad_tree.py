import cv2
from utils import *
import random


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
    def check(self, matrix, threshold, min_sq_size=10, subimage_coord=(0, 0, 1, 1)):
        # 小于min_sq_size的块就不再分了，太小没啥意义
        # mouse_x, mouse_y = mouse
        ly, lx, ry, rx = subimage_coord
        if abs(self.rx - self.lx) <= min_sq_size:
            return True
        # 判断两个矩形没有重叠
        # if (self.ry < ly) and (self.ly > ry) and (self.rx > lx) and (self.lx < rx):
        # if self.lx > rx or self.ly < ry or self.rx >lx or self.ry > ly: # 没有重叠
        # if self.lx < rx and self.ly > ry and self.rx <lx and self.ry < ly:  # 有重叠
        if self.lx > rx or self.ly > ry or lx > self.rx or ly > self.ry:
            return True
        else:
            if abs(self.rx - self.lx) <= 20:
                # print((self.lx, self.ly, self.rx, self.ry), (subimage_coord))
                minVal, maxVal, _, _ = cv2.minMaxLoc(matrix[self.lx:self.rx, self.ly:self.ry])
                # print(matrix[self.lx:self.rx, self.ly:self.ry].shape, self.lx, self.rx, self.ly, self.ry)
                if abs(minVal - maxVal) >= threshold:
                    return False
                else:
                    return True
            else:
                return False

    # 打印正方形的坐标
    def print(self):
        print("lx:", self.lx, end=", ")
        print("ly:", self.ly, end=", ")
        print("rx:", self.rx, end=", ")
        print("ry:", self.ry)

    def draw_sq(self, img):
        # for col in range(self.ly, self.ry):
        #     img[self.rx][col] = 255
        # for row in range(self.lx, self.rx):
        #     img[row][self.ry] = 255
        img[self.rx, self.ly:self.ry] = 255
        img[self.lx:self.rx, self.ry] = 255
        return


# 检查所有块里面是否还有不行的
# 参数：原矩阵、正方形对象列表
# 返回值：若有不行的，返回对象和下标；否则返回空对象
def check_all(matrix, square_arr, min_sq=5, subimage_coord=(0, 0, 1, 1),
              start=0):
    for i in range(start, len(square_arr)):
        if square_arr[i].check(matrix, 10, min_sq_size=min_sq,
                               subimage_coord=subimage_coord) == False:  # 阈值在此设置
            # print(abs(square_arr[i].lx-square_arr[i].rx))
            return square_arr[i], i
    return None, -1


# 得到最终的四叉树
def get_quad_tree(matrix, square_arr, min_sq=5, subimage_coord=(0, 0, 1, 1)):
    index = 0
    while (True):
        # while True:
        #     problem_block, index = square_arr[i].check(matrix, 10, min_sq_size=min_sq,
        #                        subimage_coord=subimage_coord) == False
        #     i += index
        problem_block, index = check_all(matrix, square_arr, min_sq=min_sq,
                                         subimage_coord=subimage_coord,
                                         start=index)
        if problem_block == None:
            break
        lx = problem_block.lx
        ly = problem_block.ly
        rx = problem_block.rx
        ry = problem_block.ry
        # if abs(lx-rx) < 20 or abs(ly-ry) < 20:
        #     break
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
    # print('utils shape: ', img.shape)
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


def get_quad_grid(screenshot, min_sq=5, subimage_coord=(0, 0, 1, 1),
                  canvas_height=1086, canvas_width=600
                  ):
    # global canvas_height, canvas_width, grid_width, grid_height
    matrix = screenshot
    n_row = 5
    n_col = 9
    grid_width = int(canvas_width / n_col)
    grid_height = int(canvas_height / n_row)
    first_square = square(0, 0, int(grid_height * 8) - 1, int(grid_width * 8))
    second_square = square(0, int(grid_width * 8), int(grid_height * 8) - 1,
                           int(grid_width * 16) - 1)
    square_arr = [first_square, second_square]
    # square_arr = []
    # for i in range(5):
    #     tmp = square(grid_width * 8, grid_height * i,
    #                  canvas_width - 1, grid_height * (i + 1)-1)
    #     print()
    #     square_arr.append(tmp)
    square_arr = get_quad_tree(matrix, square_arr, min_sq=min_sq,
                               subimage_coord=subimage_coord)
    # square_arr2 = get_quad_tree()
    # print(len(square_arr))
    for sq in square_arr:
        # if sq.lx >= canvas_width or sq.ly >= canvas_height:
        #     continue
        # elif sq.rx >= canvas_width or sq.ry >= canvas_height:
        #     sq.rx = min(canvas_width-1, sq.rx)
        #     sq.ry = min(canvas_height-1, sq.ry)
        #     # print((sq.lx, sq.ly, sq.rx, sq.ry))

        # if sq.ry - sq.ly > grid_height or sq.rx- sq.lx > grid_width:
        #     print("sq:", (sq.lx, sq.ly, sq.rx, sq.ry))
        #     for i in range(sq.lx//grid_width, n_col):
        #         for j in range(sq.ly // grid_height, n_row):
        #             new_sq = square(i*grid_width, j*grid_height, (i+1)*grid_width, (j+1)*grid_height)
        #             print(new_sq.lx, new_sq.ly, new_sq.rx, new_sq.ry)
        #             new_sq.draw_sq(screenshot)
        # else:
        #     sq.draw_sq(screenshot)
        # sq.draw_sq(screenshot)
        matrix[sq.rx, sq.ly:sq.ry] = 255
        matrix[sq.lx:sq.rx, sq.ry] = 255
    return matrix

#
#
# # ref: https://blog.csdn.net/weixin_44164489/article/details/112853121
