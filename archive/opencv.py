import cv2
import numpy as np

# 定义回调函数，处理鼠标点击事件
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # 在鼠标点击位置创建一个腐蚀核
        kernel = np.ones((5, 5), np.uint8)
        # 对图像进行腐蚀处理
        eroded_image = cv2.erode(frame, kernel, iterations=1)
        # 显示腐蚀后的图像
        cv2.imshow("Eroded Image", eroded_image)

# 创建一个VideoCapture对象，打开摄像头
cap = cv2.VideoCapture(0)

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("无法打开摄像头")
    exit()

# 创建一个GUI窗口
cv2.namedWindow("Video")

# 设置鼠标点击回调函数
cv2.setMouseCallback("Video", mouse_callback)

while True:
    # 读取视频帧
    ret, frame = cap.read()

    # 显示视频帧
    cv2.imshow("Video", frame)

    # 检查用户是否按下了Esc键
    if cv2.waitKey(1) == 27:
        break

# 释放摄像头和销毁窗口
cap.release()
cv2.destroyAllWindows()
