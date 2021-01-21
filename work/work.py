import os
import time
import re
import math
import random
# from datetime import date,datetime
# print(time.strftime("%Y-%m-%d", time.localtime()))
#对文件的操作 包括打乱顺序 查询指定txt文件 组装txt
class handleTxt:
    '''
    #说明：①需要遍历组装的文件夹目录（self.readdir）
    #说明：②将新组装txt文件放入的目录（self.writedir）
    #说明：③将新组装txt文件写入的文件名字（self.write_filename）
    #说明：④读取文件的名字（self.read_filename）
    '''
    def __init__(self):
        self.read_filename=''
        self.write_filename='result26.txt'
        self.readdir=r'D:\pydata\data\组装txt'
        self.writedir=r'D:\pydata\data\组装结果txt'
        self.make_num=60000
        self.open_filename=r'C:\Users\CYG\Desktop\linshi.txt'
        self.write_filename=r'C:\Users\CYG\Desktop\linshi2.txt'
    '''
    #判断文件是否存在 不存在就创建文件
    '''
    def make_file(self,path=r'E:\红星办公文件\关键词\抓取工具\生成的数据'):
        # path=r'E:\红星办公文件\关键词\抓取工具\生成的数据'
        if os.path.exists(path):
            self.open_filename=open(path, mode='w', encoding='utf-8')
            print('第一种刚开启文件:{}'.format(path))
        else:
            if self.open_filename :
                pass
            else:
                self.open_filename=open(path, mode='w', encoding='utf-8')
                print('第二种刚开启文件:{}'.format(path))
    '''
    测试方法
    '''
    def improve(self):
        str='error-test.txt'
        # pattern = re.compile(r'(.*)(?!test(.*))(\.)txt')
        # pattern = re.compile(r'((?!test).)*(\.)txt')
        pattern = re.compile(r'(((?!test\.txt).)*)')
        # flag = pattern.search(str)
        flag = pattern.match(str)
        print(flag)

    '''
    # 测试方法
    '''
    def test(self):
        # pattern=r'(.*)([^test]).txt'
        # pattern=r'(.*)(^-)(.*).txt'
        pattern=re.compile(r'(.*)(?!test)(.*)(\.)txt')
        file_dir=r'E:\红星办公文件\关键词\抓取工具\spider1.7'
        dir=time.strftime("%Y-%m-%d", time.localtime())
        for root, dirs, files in os.walk(file_dir):
            for filename in files:
                print(filename)
                # flag=re.match(pattern,filename)
                # flag=pattern.match(filename)
                flag=pattern.search(filename)
                print(flag)
            # print(files)
        pass
    '''
    向打开的文件中写入数据
    '''
    def write_txt(self,keyword,filename):
        if self.open_filename :
            self.open_filename.write(keyword)
        else:
            self.make_file(filename)
    '''
    遍历根据指定文件夹中的文件 并且根据每个文件中的行数按照比例随机抽取行数 并合成新的txt文件
    '''
    def read_txt_make(self):
        make_num=self.make_num
        data=[]
        file_rows=[]
        for root, dirs, files in os.walk(self.readdir):
            for filename in files:
                with open(self.readdir+'\\'+filename, mode='r',encoding='utf-8') as f:
                    if filename=='description_product5.txt':
                        file_rows.append(8000)
                    else:
                        file_rows.append(len(f.readlines()))
        all = sum(file_rows)
        prop_num=[ math.ceil(i*make_num/all) for i in file_rows]
        i=0
        for root, dirs, files in os.walk(self.readdir):
            for filename in files:
                with open(self.readdir + '\\' + filename, mode='r', encoding='utf-8') as ff:
                    print('文件:{},取出{}数量的的关键词'.format(filename,prop_num[i]))
                    get_rows=random.sample(ff.readlines(),prop_num[i])
                    i = i + 1
                    for keyword in get_rows :
                        self.write_txt(keyword, self.writedir+'/'+self.write_filename)
                    # print(get_rows)
    '''
    打乱txt文件中的顺序
    '''
    def txt_shuffle(self):
        out = open(r"E:\红星办公文件\关键词\关键词txt备份\临时\temp.txt", 'w',encoding='utf-8')
        lines = []
        with open(r"E:\红星办公文件\关键词\关键词txt备份\组装词\description_product7.txt", 'r',encoding='utf-8') as infile:
            for line in infile:
                lines.append(line)
        random.shuffle(lines)
        random.shuffle(lines)
        random.shuffle(lines)
        random.shuffle(lines)
        random.shuffle(lines)
        for line in lines:
            out.write(line)

    '''
    去除txt文档中 每行左边的空格 以及空行 全是特殊字符
    '''
    def filter_txt(self):
        filename = self.open_filename
        file2 = open(self.write_filename, 'a', encoding='utf-8')
        with open(filename, mode='r', encoding='utf-8') as ff:
            for i in ff.readlines():
                str = i.lstrip()
                str=self.filter_nochar(str)
                if str == '\n' :
                    str = str.strip('\n')
                print(str)
                file2.write(str)

    '''
        去除字符串中全是特殊字符
        '''
    def filter_nochar(self,text=''):
        cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9^\n^\s^.]")  # 匹配不是中文、大小写、数字的其他字符
        text = cop.sub('',text)
        return text
    '''
    将字符串中的数字替换掉  将txt里的除了a 以外的单个字符删除掉
    open_file:读取文件
    fwrite_file：写入文件名字
    fileter_digital:true 过滤数字  false:不过滤数字
    '''
    # def filter_digital_txt(self,open_file='',fwrite_file='',fileter_digital=true):
    #     write_filename = open(r'C:\Users\CYG\Desktop\linshi.txt', 'a', encoding='utf-8')
    #     readfile=self.writedir+'\\'+self.write_filename
    #     with open(readfile, 'r',encoding='utf-8') as infile:
    #         for line in infile:
    #             if fileter_digital:
    #                 write_line=re.sub('\d+','',line)
    #             # write_line=line
    #             write_line = [i for i in write_line.split() if len(i) > 1 or i == 'a']
    #             write_line = ' '.join(write_line)
    #             write_filename.write(write_line+'\n')
    '''
    过滤文本中连续的空格
    '''
    def filter_space_txt(self):
        open_filename = self.open_filename
        write_filename = open(self.write_filename, 'a', encoding='utf-8')
        with open(open_filename, mode='r', encoding='utf-8') as ff:
            for i in ff.readlines():
                str = i.lstrip()
                str=' '.join(str.split())
                if len(str.split())>1:
                    flag=self.filter_keyword(str)
                    if flag is True:
                        write_filename.write(str+'\n')

    '''
        判断长尾关键词是否含有关键词
    '''

    def filter_keyword(self,words):
        arr=['crusher','crushing','crushers','dryer','drying','dryers','jaw','grinding','sand','sanding','machine','plant','mill','mills']
        word_list=words.split()
        for word in word_list:
            if word.lower() in arr:
                return True
            else:
                pass
        return False
    '''
    将txt里的内容分成等数量的多个txt文本
    '''
    def split_num_txt(self):
        pass

    '''
        将txt里的内容删除多行
    '''
    def del_txt(self):
        filename=r'D:\pydata\data\test.txt'
        with open(filename, mode='r', encoding='utf-8') as ff:
            get_rows = random.sample(ff.readlines(), 5)
        pass

    '''
        过滤文本中连续的空格
    '''
    def filter_space(self,str=''):
        str = ' '.join(str.split())
        return str
    '''
       过滤文本中连续的空格
    '''
    def url_txt(self):
        open_filename = r'C:\Users\CYG\Desktop\url.txt'
        write_filename = open(r'C:\Users\CYG\Desktop\url2.txt','a',encoding='utf-8')
        with open(open_filename,mode='r',encoding='utf-8') as ff:
            for i in ff.readlines():
                str=i.replace('\r','').replace('\n','').replace('\t','')+'|'
                write_filename.write(str)
if __name__=='__main__':
    hd=handleTxt()
    # 根据txt文件生成一定数量关键词的txt文件
    # hd.read_txt_make()
    # hd.filter_digital_txt()
    # hd.filter_space_txt()
    hd.filter_txt()
    print('运行结束')
    # str=' a s  svadaf12 ad    adsfa '
    # str = str.lstrip()
    # str = ' '.join(str.split())
    # print(str)