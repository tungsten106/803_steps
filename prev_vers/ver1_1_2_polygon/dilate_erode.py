# from old.polygons import *
import numpy as np

def dilate2_grid(img, size, threshold=128,
                 modes=np.ones((2,3))):
    """
    dilate algo from chatgpt
    :param img: ndarray image to dilate
    :param size: size of block around each pixels to compute average
    :param threshold: default=128, avg>threshold then white
    :return: dilated image
    """
    n_row, n_col = modes.shape
    grid_x = img.shape[0]/n_row
    grid_y = img.shape[1]/n_col
    mode_dict = {1: size, 2: int(size+2),
                 3: int(size//2), 4: 0}

    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            # print(x//grid_x, y//grid_y)
            m = modes[int(x//grid_x)][int(y//grid_y)]
            size_new = mode_dict[m]
            xlim1 = max(x - size_new, 0)
            xlim2 = min(x + size_new + 1, img.shape[0])
            ylim1 = max(y - size_new, 0)
            ylim2 = min(y + size_new + 1, img.shape[1])
            avg = np.mean(img[xlim1:xlim2, ylim1:ylim2])

            if avg > threshold:
                img[x][y] = 225
            else:
                img[x][y] = 0
    return img

def create_mode(gird_size, img, size):
    n_row, n_col = gird_size
    # n_block = n_row * n_col
    # 取不同mode，假设4种
    # mode1: dilate_index const
    # mode2: dilate_index//2
    # mode3: no operations
    modes = np.random.randint(1, 4, size=gird_size)
    grid_x = img.shape[0]/n_row
    grid_y = img.shape[1]/n_col
    mode_dict = {1: size, 2: int(size//2), 3: 0}