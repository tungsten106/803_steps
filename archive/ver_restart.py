import cv2
import numpy as np

# 读取黑白图像
image = cv2.imread('xiaoyaoyou.jpeg', cv2.IMREAD_GRAYSCALE)

# 创建一个空白图像，用于渐变效果
gradient = np.zeros_like(image)

# 设置窗口和鼠标事件回调函数
window_name = 'Text Revealer'
cv2.namedWindow(window_name)

# 鼠标位置和方块大小
mouse_position = (-1, -1)
square_size = 20

def reveal_text(event, x, y, flags, param):
    global mouse_position

    if event == cv2.EVENT_MOUSEMOVE:
        mouse_position = (x, y)
    elif event == cv2.EVENT_LBUTTONDOWN:  # 当按下鼠标左键时
        # 恢复原始图像作为蒙版
        mask = image.copy()

        # 获取方块位置和大小
        square_x = max(0, mouse_position[0] - square_size // 2)
        square_y = max(0, mouse_position[1] - square_size // 2)
        square_width = min(square_size, image.shape[1] - square_x)
        square_height = min(square_size, image.shape[0] - square_y)

        # 创建方块蒙版
        mask[square_y:square_y + square_height, square_x:square_x + square_width] = 255

        # 逐渐增加腐蚀程度，显示出文字
        for i in range(1, 20):
            kernel = np.ones((i, i), dtype=np.uint8)
            eroded = cv2.erode(mask, kernel)
            cv2.imshow(window_name, cv2.bitwise_and(image, eroded))
            cv2.waitKey(30)  # 调整此处的延迟时间以控制特效速度

        # 使用膨胀操作还原图像
        for i in range(1, 20):
            kernel = np.ones((i, i), dtype=np.uint8)
            dilated = cv2.dilate(eroded, kernel)
            cv2.imshow(window_name, cv2.bitwise_and(image, dilated))
            cv2.waitKey(30)

cv2.setMouseCallback(window_name, reveal_text)

# 显示原始图像
cv2.imshow(window_name, image)
cv2.waitKey(0)

# 清理窗口和退出程序
cv2.destroyAllWindows()
