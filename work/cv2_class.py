import cv2 as cv
import np as np
import os
class Cv2class:
    def img_kernel(self,img):
    #     kernel=np.ones([5,5],np.float32)/25
    #     kernel=np.array([[0,1,0],[0,1,0],[0,1,0]],np.float32)/3
    #过滤片
        kernel=np.array([[1,0,-1],[1,0,-1],[1,0,-1]],np.float32)
        dst=cv.filter2D(img,-1,kernel)
        return dst
    #展示图片
    def show_img(self,img,name='img'):
        cv.imshow(name, img)
        cv.waitKey(0)
        cv.destroyAllWindows()
    #阀值控制
    def img_threshold(self,img):
        Grayimg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # cv.imwrite(r"C:\Users\CYG\Desktop\rest.jpg",Grayimg)
        # ret, thresh = cv.threshold(Grayimg, 40, 125, cv.THRESH_BINARY)
        ret, thresh = cv.threshold(Grayimg, 150,255,cv.THRESH_TOZERO)
        return thresh
    #添加文字
    def add_mask(self,img):
        text='naprawavolvolodz'
        # length=len(text)
        # print(length)
        h, w = img.shape[0], img.shape[1]
        #添加文字，（200, 100）left top 是初始的位置，1.2表示字体大小，(255,255,255)表示颜色，2表示粗细
        cv.putText(img, text, (0, h-10), cv.FONT_HERSHEY_COMPLEX, 1, (125, 125, 125),2)
        return img
    #图像模糊化
    def blur(self,img):
        return_img=cv.blur(img,(2,2))
        return return_img
    #图像高斯模糊化
    def gaussianblur(self,img=''):
        a=cv.imread(img)
        b=cv.GaussianBlur(a,(5,5),0)
        return b
    #图像中值模糊
    def medianblur(self,img=''):
        a=cv.imread('4.jpg')#
        b=cv.medianBlur(a,3)
        return b
    #图像加权叠加
    def contrast_demo(self,img):  # 亮度就是每个像素所有通道都加上b
        rows, cols, chunnel = img.shape
        blank = np.ones([rows, cols, chunnel], img.dtype)  # np.zeros(img1.shape, dtype=uint8)
        return_img = cv.addWeighted(img, 1.3, blank, 0.5, 3)
        return return_img
    #图像调整亮度
    def my_action(self,img):
        img_np=np.array(img)
        b = np.dot(img_np,0.5,np=int)
        # cv.imshow('original', img)
        return b
    #水平反转
    def img_flip(self,img):
        #水平镜像
        return_img = cv.flip(img, 1, dst=None)
        return return_img
    #图像叠加
    def watermark(self,src_path, mask_path, alpha = 0.3):
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
        self.show_img(dst_img)
    def resize_img(self,img):
        return_img=cv.resize(img,(450,320))
        return return_img

    def nothing(self,x):
        pass
    '''
    说明：通过滑块 对图片颜色进行选择
    '''
    def hsv(self,path='./photo/4.jpg'):
        # icol = (36,202,59,71,255,255)  # Green
        #icol = (18, 0, 196, 36, 255, 255)  # Yellow
        #icol = (89, 0, 0, 125, 255, 255)  # Blue
        icol = (0,100,80,10,255,255)  # Red
        cv.namedWindow('colorTest')
        # Lower range colour sliders.
        cv.createTrackbar('lowHue','colorTest',icol[0],255,self.nothing)
        cv.createTrackbar('lowSat','colorTest',icol[1],255,self.nothing)
        cv.createTrackbar('lowVal','colorTest',icol[2],255,self.nothing)
        # Higher range colour sliders.
        cv.createTrackbar('highHue','colorTest',icol[3],255,self.nothing)
        cv.createTrackbar('highSat','colorTest',icol[4],255,self.nothing)
        cv.createTrackbar('highVal','colorTest',icol[5],255,self.nothing)

        frame = cv.imread(path)

        while True:
            lowHue = cv.getTrackbarPos('lowHue','colorTest')
            lowSat = cv.getTrackbarPos('lowSat','colorTest')
            lowVal = cv.getTrackbarPos('lowVal','colorTest')
            highHue = cv.getTrackbarPos('highHue','colorTest')
            highSat = cv.getTrackbarPos('highSat','colorTest')
            highVal = cv.getTrackbarPos('highVal','colorTest')

            cv.imshow('frame',frame)

            frameBGR = cv.GaussianBlur(frame,(7,7),0)

            cv.imshow('blurred',frameBGR)

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

            cv.imshow('mask',mask)
            result = cv.bitwise_and(frame,frame,mask=mask)
            cv.imshow('colorTest',result)

            k = cv.waitKey(5) & 0xFF
            if k == 27:
                break
if __name__=="__main__":
    imgpath=r"D:\pydata\work\photo\1.jpg"
    # imgpath=r"4.jpg"
    img = cv.imread(imgpath)
    cv2class=Cv2class()
    cv2class.show_img(img)
    img=cv2class.resize_img(img)
    print(img)
    cv2class.show_img(img)
