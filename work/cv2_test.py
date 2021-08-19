import cv2 as cv
import numpy as np
import os
import re
import pytesseract
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import easyocr as ocr

def orc_detect():
    reader = ocr.Reader(['ch_sim','en'])
    result = reader.readtext(r'C:\Users\CYG\Desktop\2.png')

    print(result)
# orc_detect()
def find_square():
    img=cv.imread(r'C:\Users\CYG\Desktop\2.png')
    cv.imshow('origin',img)
    gray_img=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    cv.imshow('gray',gray_img)
    gauss_img=cv.GaussianBlur(gray_img,(3,3),5)
    cv.imshow('gauss_img',gauss_img)
    ret,binary = cv.threshold(gray_img,150,255,cv.THRESH_TOZERO)
    cv.imshow('binary',binary)
    contours, s = cv.findContours(binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(img,contours,-1,(0,0,255),3)  # 把轮廓画在原图上（0,0,255） 表示 RGB 三通道，红色

    cv.imshow("image",img)  # 显示原图
    cv.waitKey(0)
def test_cv():
    img = cv.imread(r'C:\Users\CYG\Desktop\jaw-crusher1.jpg')
    cv.imshow('origin',img)
    gray_img = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    cv.imshow('gray',gray_img)
    cv.calcHist()
    cv.waitKey(0)
# test_cv()
def hist_cv(img):
    (b,g,r) = cv.split(img)
    bH = cv.equalizeHist(b)
    gH = cv.equalizeHist(g)
    rH = cv.equalizeHist(r)
    # 合并每一个通道
    result = cv.merge((bH,gH,rH))
    return result
# hist_cv()
def three_d():
    fig = plt.figure()
    ax = Axes3D(fig)
    X = np.arange(0,8,0.25)
    Y = np.arange(0,8,0.25)
    X,Y = np.meshgrid(X,Y)  # x-y 平面的网格
    # Z = np.sqrt(X ** 2 + Y ** 2)
    # Z =4-np.sqrt(X ** 2 + Y ** 2)
    Z =np.multiply(X,Y)
    print(Z)
    # height value
    # Z = np.sin(R)
    ax.plot_surface(X,Y,Z,rstride=1,cstride=1,cmap=plt.get_cmap('rainbow'))
    plt.show()
# three_d()
def img_kernel(img):
#     kernel=np.ones([5,5],np.float32)/25
    kernel=np.array([[1,0,-1],[1,0,-1],[1,0,-1]],np.float32)
    dst=cv.filter2D(img,-1,kernel)
    return dst

def show_img(img,name='img'):
    cv.imshow(name, img)
    cv.waitKey(0)
    cv.destroyAllWindows()
def img_threshold(img):
    Grayimg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # cv.imwrite(r"C:\Users\CYG\Desktop\rest.jpg",Grayimg)
    # ret, thresh = cv.threshold(Grayimg, 40, 125, cv.THRESH_BINARY)
    ret, thresh = cv.threshold(Grayimg, 150,255,cv.THRESH_TOZERO)
    show_img(Grayimg)
    return thresh

def add_mask(img):
    text='naprawavolvolodz'
    length=len(text)
    print(length)
    h, w = img.shape[0], img.shape[1]
    #添加文字，（200, 100）left top 是初始的位置，1.2表示字体大小，(255,255,255)表示颜色，2表示粗细
    cv.putText(img, text, (0, h-10), cv.FONT_HERSHEY_COMPLEX, 1, (125, 125, 125),2)
    show_img(img)
    pass

def blur(img):
    return_img=cv.blur(img,(2,2))
    return return_img
def gaussianblur(img=''):
    cv.imshow('original',img)
    b=cv.GaussianBlur(img,(3,3),1)
    cv.imshow('result',b)
    cv.waitKey(0)
    cv.destroyAllWindows()

def medianblur(img=''):
    a=cv.imread('4.jpg')#
    b=cv.medianBlur(a,3)
    cv.imshow('original',a)
    cv.imshow('result',b)
    cv.waitKey(0)
    cv.destroyAllWindows()
def contrast_demo(img):  # 亮度就是每个像素所有通道都加上b
    rows, cols, chunnel = img.shape
    blank = np.ones([rows, cols, chunnel], img.dtype)  # np.zeros(img1.shape, dtype=uint8)
    return_img = cv.addWeighted(img, 1.3, blank, 0.5, 3)
    return return_img
# img=cv.imread("8.jpg")
# return_img=contrast_demo(img)
# show_img(return_img)
def my_action(img=''):
    img = cv.imread('4.jpg')
    img_np=np.array(img)
    b = np.dot(img_np,0.5,np=int)
    cv.imshow('original', img)
    cv.imshow('result', b)
    cv.waitKey(0)
    cv.destroyAllWindows()
# my_action(img='')
def img_flip(img):
    #水平镜像
    return_img = cv.flip(img, 1, dst=None)
    return return_img
    # cv.imwrite(r'C:\Users\CYG\Desktop\修改之后的\1.jpg',return_img)
    # 对角
    # xImg1 = cv.flip(img, -1, dst=None)
def resize_img(img):
    return_img=cv.resize(img,(300,225))
    return return_img
def bilateralfilter_img(img):
    src1=cv.bilateralFilter(src=img,d=0,sigmaColor=80,sigmaSpace=20)
    return src1
def img_rotation(img):
    cols,rows,chunnel = img.shape
    M = cv.getRotationMatrix2D((cols / 2,rows / 2),5,1.1)#中心点 角度 缩放因子
    dst = cv.warpAffine(img,M,(rows,cols))
    return dst
    # cv.imshow('1',img)
    # cv.imshow('2',dst)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

# img=cv.imread('./photo/test1.jpg')
# img_rotation(img)
def img_dir_all():
    # dir=r'E:\红星办公文件\通用的模版文件\photo\ProImages'
    dir_path=r'E:\product-photo\infoimages'
    dir_path2=r'E:\product-photo\infoimageshist'
    for root, dirs, files in os.walk(dir_path):
        if dirs:
            for dir in dirs:
                if os.path.exists(dir_path2+'/'+dir):
                    pass
                else:
                    print('创建文件:{}'.format(dir_path2+'/'+dir))
                    os.makedirs(dir_path2+'/'+dir)
        for file in files:
            last_dir=root.split('\\')[-1]
            last_dir_path=dir_path2+'\\'+last_dir+'\\'
            if os.path.exists(last_dir_path+file):
                pass
            else:
                img_save=cv.imdecode(np.fromfile(root+'\\'+file, dtype=np.uint8), -1)
                # img_save=bilateralfilter_img(img_save)
                # img_save=img_rotation(img_save)
                img_save=hist_cv(img_save)
                # img_save=cv.cvtColor(img_save,cv.COLOR_BGR2GRAY)
                # if last_dir.rstrip('/')=='hot-products':
                #     file=last_dir+file
                # if last_dir.rstrip('/')=='briquette-machine':
                #     cop = re.compile("[\s()]")  # 匹配不是中文、大小写、数字的其他字符
                #     file = cop.sub('',file)
                #     file='-'.join(file.split('_'))
                # img_save=contrast_demo(img)
                cv.imencode('.jpg', img_save)[1].tofile(last_dir_path+file)
                # cv.imwrite(last_dir_path+file, img)
                print(last_dir_path + file)
# img_dir_all()
def img_file_all():
    # dir=r'E:\红星办公文件\通用的模版文件\photo\ProImages'
    dir_path=r'E:\product-photo\images'
    dir_path2=r'E:\product-photo\images2'
    for root, dirs, files in os.walk(dir_path):
        if dirs:
            for dir in dirs:
                if os.path.exists(dir_path2+'/'+dir):
                    pass
                else:
                    print('创建文件:{}'.format(dir_path2+'/'+dir))
                    os.makedirs(dir_path2+'/'+dir)
        for file in files:
            last_dir=root.split('\\')[-1]
            last_dir_path=dir_path2+'\\'
            if os.path.exists(last_dir_path+file):
                pass
            else:
                img=cv.imdecode(np.fromfile(root+'\\'+file, dtype=np.uint8), -1)
                # img = cv.imread(root+'\\'+file)
                print(root+'\\'+file)
                img_save=img_flip(img)

                cv.imencode('.jpg', img_save)[1].tofile(last_dir_path+file)
                # cv.imwrite(last_dir_path+file, img)
                print(last_dir_path+file)
# img_file_all()
def watermark(src_path, mask_path, alpha = 0.3):
    img = cv.imread(src_path)
    h,w = img.shape[0], img.shape[1]
    mask = cv.imread(mask_path, cv.IMREAD_UNCHANGED)
    if w > h:
        rate = int(w * 0.1) / mask.shape[1]
    else:
        rate = int(h * 0.1) / mask.shape[0]
    mask = cv.resize(mask, None, fx=rate, fy=rate)
    mask_h, mask_w = mask.shape[0], mask.shape[1]
    mask_channels = cv.split(mask)
    dst_channels = cv.split(img)
    b, g, r, a = cv.split(mask)

    # 计算mask在图片的坐标
    ul_points = (int(h * 0.9), int(int(w/2) - mask_w / 2))
    dr_points = (int(h * 0.9) + mask_h, int(int(w/2) + mask_w / 2))
    for i in range(3):
        dst_channels[i][ul_points[0] : dr_points[0], ul_points[1] : dr_points[1]] = dst_channels[i][ul_points[0] : dr_points[0], ul_points[1] : dr_points[1]] * (255.0 - a * alpha) / 255
        dst_channels[i][ul_points[0]: dr_points[0], ul_points[1]: dr_points[1]] += np.array(mask_channels[i] * (a * alpha / 255), dtype=np.uint8)
    dst_img = cv.merge(dst_channels)
    show_img(dst_img)

def compare_img(file1='',file2=''):
    file1 = r'C:\Users\CYG\Desktop\ball-mill2.jpg'
    file2 = r'C:\Users\CYG\Desktop\ball-mill3.jpg'
    im1 = cv.imread(file1)
    im2 = cv.imread(file2)
    if im1.shape == im2.shape:
        print('shape一样')
    else:
        print('shape not equal')
    difference = cv.subtract(im1,im2)
    # print(difference)
    result = not np.any(difference)
    if result is False:
        print('不一样')
        cv.imwrite('reslult.jpg',difference)
    else:
        print('一样')
def bilateralfilter_img2(img):
    # img = cv.cvtColor(img,cv.COLOR_BGR2RGB)
    # print(img)
    src1=cv.bilateralFilter(src=img,d=0,sigmaColor=80,sigmaSpace=20)
    cv.imshow('test',src1)
    # print(src1)
    return src1
def nothing(x):
    pass
def hsv():
    # icol = (36,202,59,71,255,255)  # Green
    #icol = (18, 0, 196, 36, 255, 255)  # Yellow
    #icol = (89, 0, 0, 125, 255, 255)  # Blue
    icol = (0, 100, 80, 10, 255, 255)   # Red
    cv.namedWindow('colorTest')
    # Lower range colour sliders.
    cv.createTrackbar('lowHue','colorTest',icol[0],255,nothing)
    cv.createTrackbar('lowSat','colorTest',icol[1],255,nothing)
    cv.createTrackbar('lowVal','colorTest',icol[2],255,nothing)
    # Higher range colour sliders.
    cv.createTrackbar('highHue','colorTest',icol[3],255,nothing)
    cv.createTrackbar('highSat','colorTest',icol[4],255,nothing)
    cv.createTrackbar('highVal','colorTest',icol[5],255,nothing)

    # Raspberry pi file path example.
    #frame = cv.imread('/home/pi/python3/opencv/color-test/colour-circles-test.jpg')
    # Windows file path example.
    frame = cv.imread('./photo/4.jpg')

    while True:
        # Get HSV values from the GUI sliders.
        lowHue = cv.getTrackbarPos('lowHue','colorTest')
        lowSat = cv.getTrackbarPos('lowSat','colorTest')
        lowVal = cv.getTrackbarPos('lowVal','colorTest')
        highHue = cv.getTrackbarPos('highHue','colorTest')
        highSat = cv.getTrackbarPos('highSat','colorTest')
        highVal = cv.getTrackbarPos('highVal','colorTest')

        # Show the original image.
        cv.imshow('frame',frame)

        # Blur methods available, comment or uncomment to try different blur methods.
        frameBGR = cv.GaussianBlur(frame,(7,7),0)
        #frameBGR = cv.medianBlur(frameBGR, 7)
        #frameBGR = cv.bilateralFilter(frameBGR, 15 ,75, 75)
        """kernal = np.ones((15, 15), np.float32)/255
        frameBGR = cv.filter2D(frameBGR, -1, kernal)"""

        # Show blurred image.
        cv.imshow('blurred',frameBGR)

        # HSV (Hue, Saturation, Value).
        # Convert the frame to HSV colour model.
        hsv = cv.cvtColor(frameBGR,cv.COLOR_BGR2HSV)

        # HSV values to define a colour range.
        colorLow = np.array([lowHue,lowSat,lowVal])
        colorHigh = np.array([highHue,highSat,highVal])
        mask = cv.inRange(hsv,colorLow,colorHigh)
        # Show the first mask
        cv.imshow('mask-plain',mask)

        kernal = cv.getStructuringElement(cv.MORPH_ELLIPSE,(7,7))
        mask = cv.morphologyEx(mask,cv.MORPH_CLOSE,kernal)
        mask = cv.morphologyEx(mask,cv.MORPH_OPEN,kernal)

        # Show morphological transformation mask
        cv.imshow('mask',mask)

        # Put mask over top of the original image.
        result = cv.bitwise_and(frame,frame,mask=mask)

        # Show final output image
        cv.imshow('colorTest',result)

        k = cv.waitKey(5) & 0xFF
        if k == 27:
            break
# hsv()
# img=cv.imread(r"./photo/test1.jpg")
# cv.imshow('image',img)
# return_img=bilateralfilter_img2(img)
# show_img(return_img)
