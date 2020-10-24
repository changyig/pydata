import xlrd
import xlwt
import os
from datetime import date,datetime

file = 'E:\红星办公文件\关键词\excel关键词整理\谷歌插件关键词.xls'
#判断文件是否存在 不存在便创建它
def make_file(filename):
    if os.path.exists(filename):
        pass
        # with open('filename', mode='r', encoding='utf-8') as ff:
            # print(ff.readlines())
    else:
        with open(filename, mode='w', encoding='utf-8') as ff:
            print("文件创建成功！")
#向指定文件中追加内容
def write_txt(keyword,filename):
    make_file(filename)
    with open(filename, "a", encoding='utf-8') as f:
        f.write(keyword + '\n')
    pass
#读取excel文件 并且根据sheet表单名字 将每第一列内容进行拼接（拼接对象是与内容一样的表单） 并且写入指定的txt文件中
def read_excel():
    filename='../data/description_product5.txt'
    keyword_sheet='keyword'
    country_sheet='allcountry'
    data=[]
    wb = xlrd.open_workbook(filename=file)#打开文件
    print(wb.sheet_names())#获取所有表格名字
    # sheet1 = wb.sheet_by_index(0)#通过索引获取表格
    sheet1 = wb.sheet_by_name(keyword_sheet)#通过名字获取表格
    sheet2 = wb.sheet_by_name(country_sheet)#通过名字获取表格
    for i1 in range(sheet1.nrows):
        str1=sheet1.cell_value(i1,0)
        if str1 != '':
            # print('不为空')
            # print(str1)
            for i2 in range(sheet2.nrows):
                str2 = sheet2.cell_value(i2, 0)
                str=str1+' '+str2
                write_txt(str,filename)
                # print(str)
                try:
                    sheet3 = wb.sheet_by_name(str2)  # 通过名字获取表格
                    for i3 in range(sheet3.nrows):
                        str3 = sheet3.cell_value(i3, 0)
                        # print('存在')
                        str=str1+' '+str2+' '+str3
                        write_txt(str,filename)
                except Exception:
                    # print('没有找到该表单')
                    # print(str)
                    pass
read_excel()
#读取excel文件 并且根据sheet表单名字 将每第一列内容进行拼接（拼接对象是与内容一样的表单） 并且写入指定的txt文件中
def read_excel_test():
    filename='../data/description_product3.txt'
    keyword_sheet='描述性词语'
    country_sheet='product'
    data=[]
    wb = xlrd.open_workbook(filename=file)#打开文件
    print(wb.sheet_names())#获取所有表格名字
    # sheet1 = wb.sheet_by_index(0)#通过索引获取表格
    sheet1 = wb.sheet_by_name(keyword_sheet)#通过名字获取表格
    col=ord('M')-65
    col2=ord('N')-65
    print(col)
    for i1 in range(1,sheet1.nrows):
        str1 = sheet1.cell_value(i1, col)
        if(str1==''):
            pass
        else:
            for i2 in range(1,sheet1.nrows):
                str2= sheet1.cell_value(i2, col2)
                if(str2==''):
                    # print('空的')
                    pass
                else:
                    str=str1+' '+str2
                    print(str)
                    write_txt(str, filename)

    print(ord('A'))
    # print(ord('a'))
# read_excel_test()


# def write_excel():
#     excel_book = xlwt.Workbook()  # 打开文件
#     excel_sheet = excel_book.add_sheet('res', cell_overwrite_ok=True)
#     data=read_excel()
#     print(data)


#去除txt文档中 每行左边的空格 以及空行
def filter_keyword():
    filename=r'C:\Users\CYG\Desktop\临时 - 副本.txt'
    file2 = open(r'C:\Users\CYG\Desktop\linshi.txt', 'a', encoding='utf-8')
    with open(filename, mode='r', encoding='utf-8') as ff:
        for i in ff.readlines():
            str=i.lstrip()
            # print(str)
            if str=='\n':
                print('空格')
                print(str)
                str=str.strip('\n')
            print(str)
            file2.write(str)
        # print(ff.readlines())
# filter_keyword()