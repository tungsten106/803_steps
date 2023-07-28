import numpy as np
# 设置画布大小
canvas_width = 1086
canvas_height = 600

# 四个角的坐标，需要人工校对
# 顺序是屏幕的左上-右上-右下-左下，依次校对。
input_points = np.float32([[1136,1147],
                           [-1227,1250],
                           [-1345,2400],
                           [1300,2430]])

output_points = np.float32([[0, 0], [canvas_width-1, 0],
                            [canvas_width-1, canvas_height-1], [0, canvas_height-1]])