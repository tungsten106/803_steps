import numpy as np
# 设置画布大小
canvas_width, canvas_height = 1086, 600

# 四个角的坐标，需要人工校对
# 顺序是屏幕的左上-右上-右下-左下，依次校对。
input_points = np.float32([[1136,1147],     # 左上
                           [-1227,1250],    # 右上
                           [-1345,2400],    # 右下
                           [1300,2430]])    # 左下