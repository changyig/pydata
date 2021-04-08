import cv2 as cv
import numpy as np
import os
import pytesseract
def img_kernel(img):
#     kernel=np.ones([5,5],np.float32)/25
    kernel=np.array([[0,1,0],[0,1,0],[0,1,0]],np.float32)/3
    dst=cv.filter2D(img,-1,kernel)
    return dst
# img=cv.imread("./photo/3.jpg")
# h,w = img.shape[0], img.shape[1]
# print(h,w)
# print(img)
# print(np.array(img).shape)
# print(img.shape)
# cv.namedWindow("test",cv.WINDOW_AUTOSIZE)
# src1=img_blur(img)

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
# img=cv.imread(r"C:\Users\CYG\Desktop\1.png")
# return_img=img_threshold(img)
# pytesseract.pytesseract.tesseract_cmd = r"D:\soft\tesseract-ocr\tesseract.exe"  # 设置pyteseract路径
# result = pytesseract.image_to_string(return_img)  # 图片转文字
# print(result)  # 打印识别的验证码
# show_img(return_img)
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
    a=cv.imread('8.jpg')#
    b=cv.GaussianBlur(a,(5,5),0)
    cv.imshow('original',a)
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
def img_dir_all():
    # dir=r'E:\红星办公文件\通用的模版文件\photo\ProImages'
    dir_path=r'E:\红星办公文件\通用的模版文件\photo\原图片\image450'
    dir_path2=r'E:\红星办公文件\通用的模版文件\photo\原图片\替换\image450-3'
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
                img=cv.imdecode(np.fromfile(root+'\\'+file, dtype=np.uint8), -1)
                print(root+'\\'+file)
                # img_save=img_flip(img)
                img_save=contrast_demo(img)
                cv.imencode('.jpg', img_save)[1].tofile(last_dir_path+file)
                # cv.imwrite(last_dir_path+file, img)
                print(last_dir_path+file)
# img_dir_all()
def img_file_all():
    # dir=r'E:\红星办公文件\通用的模版文件\photo\ProImages'
    dir_path=r'E:\photo\images'
    dir_path2=r'E:\photo\images2'
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
img_file_all()
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
compare_img()