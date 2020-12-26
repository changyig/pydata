import os
import time
import re
import math
import random
import cv2 as cv
from PIL import Image
import matplotlib.pyplot as plt
import pytesseract
class Tools:
    '''
    #说明：实际工作中遇见的一些问题，进行简便操作
    '''
    def __init__(self):
        self.read_filename=''
        self.write_filename=''
        self.handle_dir=r'D:\pydata\data\备份txt\备份'
        self.readdir=r'E:\www\tp584\public\public\about'
        self.writedir=r'D:\pydata\data\组装结果txt'
        self.open_filename=False
    '''
    #说明：批量修改asp后缀文件   
    '''
    def asp_to_html(self):
        for root, dirs, files in os.walk(self.readdir):
            for filename in files:
                list=filename.rsplit('.',1)
                name,ext=list[0],list[-1]
                if ext=='asp':
                    filename=root+'\\'+filename
                    newname=root+'\\'+name+'.html'
                    os.rename(filename,newname)
                    print(newname)

    '''
        #说明：批量修改html错误内容
        '''
    def content_edit(self,content=''):
        replace_str='aaaaaaa'
        # content = 'aaaaa<script> $function(){   sssss</script>aaaaa'
        print(content)
        pattern='<script>.*?</script>'
        result=re.search(pattern,content)
        print(result)
        if result:
            print('存在')
            res=content.replace(pattern,replace_str)
            return res
        else:
            print('bu 存在')
            return None
        # res=re.sub(pattern,'',content)


    '''
    #说明：批量修改html错误内容
    '''

    def html_edit(self):
        for root, dirs, files in os.walk(self.readdir):
            for filename in files:
                list = filename.rsplit('.', 1)
                name, ext = list[0], list[-1]
                if ext == 'html':
                    with open(root+'\\'+filename, "r", encoding="utf-8") as file_obj,open(root+'\\'+"%s.bak" % filename, "w", encoding="utf-8") as fwrite:
                        content=file_obj.read()
                        content=self.content_edit(content)
                        if content:
                            fwrite.write(content)
                            os.remove(root + '\\' + filename)
                            os.rename(root + '\\' + "%s.bak" % filename,root + '\\' + filename)
                            print('已经替换,文件路径:{}，文件名字:{}'.format(root,filename))
                        else:
                            pass



    '''
       将字符串中的数字替换掉  将txt里的除了a 以外的单个字符删除掉
    '''

    def filter_digital_txt(self,word):
        str = word.lstrip()
        str = ' '.join(str.split())
        write_line = re.sub('\d+', '', str)
        write_line = [i for i in write_line.split() if len(i) > 1 or i == 'a']
        write_line = ' '.join(write_line)
        return write_line

    '''
          判断长尾关键词是否含有关键词
    '''

    def filter_keyword(self, words):
        arr = ['crusher', 'crushing', 'crushers', 'dryer', 'drying', 'dryers', 'jaw', 'grinding', 'sand', 'sanding',
               'machine', 'plant', 'mill', 'mills']
        word_list = words.split()
        for word in word_list:
            if word.lower() in arr:
                return True
            else:
                pass
        return False
    '''
        遍历根据指定文件夹中的文件 并且根据每个文件中的行数按照比例随机抽取行数 并合成新的txt文件
    '''

    def read_txt_make(self):
        for root, dirs, files in os.walk(self.handle_dir):
            for filename in files:
                write_filename='D:\pydata\data\备份txt\过滤\\'+filename
                write_file = open(write_filename, 'a', encoding='utf-8')
                with open(self.handle_dir + '\\' + filename, mode='r', encoding='utf-8') as f:
                    for line in f:
                        line=self.filter_digital_txt(line)
                        if self.filter_keyword(line):
                            write_file.write(line+'\n')
                        else:
                            print('没有含有关键词')

    '''
        识别图片上的验证码 （效果不好）
    '''
    def picture_identify(self):
        img_path=r'C:\Users\CYG\Desktop\test.png'
        img=cv.imread(img_path)
        Grayimg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(Grayimg, 12, 255, cv.THRESH_BINARY)
        print(img)
        # pytesseract.pytesseract.tesseract_cmd = r"D:\soft\tesseract-ocr\tesseract.exe"  # 设置pyteseract路径
        # result = pytesseract.image_to_string(img)  # 图片转文字
        # resultj = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", result)  # 去除识别出来的特殊字符
        # result_four = resultj[0:4]  # 只获取前4个字符
        # print(result)  # 打印识别的验证码

    '''
        根据图片路径在窗口中显示图片
    '''
    def read_img(self,src_path='',name='图片'):
        img = Image.open(src_path)
        plt.figure("Image")  # 图像窗口名称
        plt.imshow(img)
        plt.axis('off')  # 关掉坐标轴为 off
        plt.title('image')  # 图像题目
        plt.show()
if __name__=='__main__':
    tools=Tools()
    tools.html_edit()
    # tools.content_edit()
    # scr_path=r'C:\Users\CYG\Desktop\logo.png'
    # tools.read_img(scr_path)