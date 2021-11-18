import cv2.cv2 as cv

window_size = [800, 600]  # 窗体的最大值


# 用于显示图片并且根据相关情况进行缩小放大
def show(Img0, Img, Center, X, Y):
    global img_show  # 需要显示在屏幕上的图片大小
    height = int(Img.shape[0] / 2)
    width = int(Img.shape[1] / 2)
    if Img.shape[1] > window_size[0] and Img.shape[0] > window_size[1]:  # 当图片的长和宽都大于窗口时
        img_show = Img[Center[1] + Y - 300: Center[1] + Y + 300, Center[0] + X - 400: Center[0] + X + 400]  # 对图片进行切片操作
        cv.resizeWindow("img", window_size[0], window_size[1])  # 重新设置窗体大小
    elif Img.shape[1] > window_size[0] and Img.shape[0] < window_size[1]:  # 当图片的宽比窗口大，但长小于窗口时
        cv.resizeWindow("img", window_size[0], Img.shape[0])  # 重新设置窗体大小
        img_show = Img[Center[1] + Y - height: Center[1] + Y + height, Center[0] + X - 400: Center[0] + X + 400]  # 对图片进行切片操作
    elif Img.shape[1] < window_size[0] and Img.shape[0] > window_size[1]:  # 当图片的宽小于窗口，但长大于窗口时
        cv.resizeWindow("img", Img.shape[1], window_size[1])  # 重新设置窗体大小
        img_show = Img[Center[1] + Y - 300: Center[1] + Y + 300, Center[0] + X - width: Center[0] + X + width]  # 对图片进行切片操作
    else:  # 最后，图片小于窗口时
        img_show = Img
        cv.resizeWindow("img", Img.shape[1], Img.shape[0])  # 窗口跟着图片进行变化
    cv.imshow("img", img_show)
    KeyNum = cv.waitKey(0)
    return KeyNum  # 返回键盘的输入


# 获得窗口的大小，以便对移动操作进行判断
def getWindow(Img):
    if Img.shape[1] > window_size[0] and Img.shape[0] > window_size[1]:
        Window_show_size = [window_size[0], window_size[1]]
    elif Img.shape[1] > window_size[0] and Img.shape[0] < window_size[1]:
        Window_show_size = [window_size[0], Img.shape[0]]
    elif Img.shape[1] < window_size[0] and Img.shape[0] > window_size[1]:
        Window_show_size = [Img.shape[1], window_size[1]]
    else:
        Window_show_size = [Img.shape[1], Img.shape[0]]
    return Window_show_size


window_show_size = [0, 0]  # 显示窗口的大小，用于判断是否可移动
cv.namedWindow("img", cv.WINDOW_NORMAL)
cv.moveWindow("img", 400, 120)
img = cv.imread("C:/Users/86159/Pictures/k.jfif", 1)  # 载入图片
img0 = cv.resize(img, (0, 0), fx=1, fy=1, interpolation=cv.INTER_NEAREST)
o_height = img0.shape[0]
o_width = img0.shape[1]
cv.resizeWindow("img", window_size[0], window_size[1])
center = [int(img.shape[1] / 2), int(img.shape[0] / 2)]  # 中心，图片将基于该中心进行移动
times = 0  # 图片放大或缩小的倍数
x = 0
y = 0
KeyNum = show(img0, img, center, x, y)

while (1):
    window_show_size = getWindow(img)
    if KeyNum == 49:  # 当按下1键时，图片缩小
        if x != 0 or y != 0:  # 当缩小时，为防止截取图片范围溢出图片边界
            if x > 0:
                x = x - 5
            if x < 0:
                x = x + 5
            if y > 0:
                y = y - 5
            if y < 0:
                y = y + 5
        times += 1
        img = cv.resize(img0, (0, 0), fx=0.99 ** times, fy=0.99 ** times, interpolation=cv.INTER_AREA)
        center = [int(img.shape[1] / 2), int(img.shape[0] / 2)]
    elif KeyNum == 50:  # 当按下2键时，图片放大
        times -= 1
        img = cv.resize(img0, (0, 0), fx=0.99 ** times, fy=0.99 ** times, interpolation=cv.INTER_LINEAR)
        center = [int(img.shape[1] / 2), int(img.shape[0] / 2)]
    elif KeyNum == 97:  # 按下a时，图片左移
        if img.shape[1] > window_show_size[0]:
            if x - 5 + center[0] > int(window_show_size[0] / 2):
                x -= 5
    elif KeyNum == 100:  # 按下d时，图片右移
        if img.shape[1] > window_show_size[0]:
            if - (x + 5) + center[0] > int(window_show_size[0] / 2):
                x += 5
    elif KeyNum == 115:  # 按下w时，图片上移
        if img.shape[0] > window_show_size[1]:
            if y - 5 + center[0] > int(window_show_size[1] / 2):
                y -= 5
    elif KeyNum == 119:  # 按下s时，图片下移动
        if img.shape[0] > window_show_size[1]:
            if - (y + 5) + center[0] > int(window_show_size[1] / 2):
                y += 5
    else:
        break
    KeyNum = show(img0, img, center, x, y)  # 等待键盘的输入
