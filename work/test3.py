import re
import matplotlib.pyplot as plt
#实例化
'''
[数量, ['product':{},'material':{},'country':{}], {0:数量,1:数量,2:数量,3:数量,4:数量,5:数量,6:数量,7:数量}]
                                        # {0:'啥也没有',1:'地区',2:'物料',3:'物料+地区',4:'产品',5:'产品+地区',6:'产品+物料',7:'产品+物料+地区'}
'''
class TextData(object):
    def __init__(self,read_path=r'C:\Users\CYG\Desktop\result2.txt'):
        self.product_path = r'./config/产品.txt'
        self.material_path = r'./config/物料词.txt'
        self.country_path = r'./config/国家.txt'
        self.read_path = read_path
        pass

    '''
           说明：匹配字符串 将匹配结果进行返回
           返回结果：[product, material, country]
       '''
    def analyze_data(self,string='',product_list=[],material_list=[],country_list=[]):
        product=[]
        material=[]
        country=[]
        for line in product_list:#判断时候含有产品
            pattern = re.compile("^"+line+"")
            pattern2 = re.compile("[\s]" + line + "([s\s]|$)")
            res=pattern.search(string)
            res2=pattern2.search(string)
            if res or res2:
                product = [line]
                break

        for line in material_list:#判断时候含有物料词
            pattern = re.compile("^" + line + "")
            pattern2 = re.compile("[\s]" + line + "([s\s]|$)")
            res = pattern.search(string)
            res2 = pattern2.search(string)
            if res or res2:
                material = [line]
                break
        for line in country_list:#判断时候含有指定的国家
            pattern = re.compile("" + line + "")
            res = pattern.search(string)
            if res :
                country = [line]
                break

        # print([product,material,country])
        if product and material:
            if material[0] in product[0].split():
                material.clear()
        return [product,material,country]

    def read_txt_write(self):
        file_path=r'E:\红星办公文件\数据分析资料\产品.txt'
        product_list=[]
        with open(file_path,mode='r',encoding='utf-8') as ff:
            for line in ff.readlines():
                line=line.lower()
                if line not in product_list:
                    product_list.append(line)
        print(product_list)
        product_write = r'E:\红星办公文件\数据分析资料\product.txt'
        with open(product_write,mode='a',encoding='utf-8') as ff:
            for line in product_list:
                ff.write(line)

    '''
          说明：字典形式的[product,material,country] 返回相应分类的数量 {0:'啥也没有',1:'地区',2:'物料',3:'物料+地区',4:'产品',5:'产品+地区',6:'产品+物料',7:'产品+物料+地区'}
          返回结果：{0:数量,1:数量,2:数量,3:数量,4:数量,5:数量,6:数量,7:数量}
      '''
    def count_num(self,dicts={},lists=[]):#八种状态 每种状态进行累加
        i=0
        b_string='0b'
        for index,list_one in enumerate(lists):#产品 物料 地区 （100=》4 产品）（101=》5 产品+国家） （110=》6 产品+物料）（111=》7 产品+物料+地区）
            if list_one:
                b_string+='1'
            else:
                b_string+='0'
        i = eval(b_string)
        if i in dicts:
            dicts[i]+=1
        else:
            dicts[i]=1

    '''
       说明：读取txt文本 并返回需要的结果
       返回结果：[数量, ['product':{},'material':{},'country':{}], {0:数量,1:数量,2:数量,3:数量,4:数量,5:数量,6:数量,7:数量}]
   '''

    def read_txt(self):
        product_list=[]
        material_list=[]
        country_list=[]
        result_list={'product':{'num':0},'material':{'num':0},'country':{'num':0}}
        with open(self.product_path,mode='r',encoding='utf-8') as ff:
            for line in ff.readlines():
                line=line.lower().strip()
                if line not in product_list:
                    product_list.append(line)
        with open(self.material_path,mode='r',encoding='utf-8') as ff:
            for line in ff.readlines():
                line=line.lower().strip()
                if line not in material_list:
                    material_list.append(line)
        with open(self.country_path,mode='r',encoding='utf-8') as ff:
            for line in ff.readlines():
                line=line.lower().strip()
                if line not in country_list:
                    country_list.append(line)

        # print(product_list)
        dicts = {}
        with open(self.read_path,mode='r',encoding='utf-8') as ff:
            lines =ff.readlines()
            line_num=len(lines)
            print(line_num)
            for line in lines:
                res = self.analyze_data(line,product_list,material_list,country_list)
                self.count_num(dicts,res)

                if res[0]:
                    result_list['product']['num']=result_list['product']['num']+1
                    if res[0][0] in result_list['product']:
                        result_list['product'][res[0][0]]=result_list['product'][res[0][0]]+1
                    else:
                        result_list['product'][res[0][0]] =1
                if res[1]:
                    result_list['material']['num'] = result_list['material']['num'] + 1
                    if res[1][0] in result_list['material']:
                        result_list['material'][res[1][0]] = result_list['material'][res[1][0]] + 1
                    else:
                        result_list['material'][res[1][0]] = 1
                if res[2]:
                    result_list['country']['num'] = result_list['country']['num'] + 1
                    if res[2][0] in result_list['country']:
                        result_list['country'][res[2][0]] = result_list['country'][res[2][0]] + 1
                    else:
                        result_list['country'][res[2][0]] = 1
                # print(result_list['country'])
        # print(result_list)
        # print(dicts)
        return [line_num,result_list,dicts]
if __name__=='__main__':
    file_path=r'C:\Users\CYG\Desktop\translate4.txt'
    TextObject=TextData()
    res=content=TextObject.read_txt()
    print('总数:{}'.format(res[0]))
    print('产品总数:{},所占百分比:{:.2%}'.format(res[1]['product']['num'],res[1]['product']['num']/res[0]))
    # bar_data_x = ['产品','物料','国家']
    # bar_data_y = [res[1]['product']['num'],res[1]['material']['num'],res[1]['country']['num']]
    # plt.rcParams['font.sans-serif'] = ['SimHei']
    # plt.rcParams['axes.unicode_minus'] = False
    # p1 = plt.bar(bar_data_x,bar_data_y)
    # plt.show()
    for i in res[1]['product'].items():
        print("{}数量:{},所占百分比:{:.2%}".format(i[0],i[1],i[1]/res[0]))
    dict_name = {0:'啥也没有',1:'地区',2:'物料',3:'物料+地区',4:'产品',5:'产品+地区',6:'产品+物料',7:'产品+物料+地区'}
    dict_x=[]
    dict_y=[]
    for xy in res[2].items():
        print(xy)
        dict_x.append(xy[1]),dict_y.append(dict_name[xy[0]])
    print(res[2])
    plt.title('词的分类分析')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    exp = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]
    plt.pie(dict_x,labels=dict_y,autopct='%1.1f%%',shadow=False,
            startangle=90,explode=exp)  # startangle控制饼状图的旋转方向
    plt.axis('equal')  # 保证饼状图是正圆，否则会有一点角度偏斜
    plt.legend()
    plt.show()
    #产品条形图
    # bar_data_x=[]
    # bar_data_y=[]
    # res[1]['country'].pop('num
    # d_order=sorted(res[1]['country'].items(),key=lambda x:x[1],reverse=True)
    # print(d_order)
    # for nm in d_order:
    #     if nm[1]>=10:
    #         bar_data_x.append(nm[0])
    #         bar_data_y.append(nm[1])
    # print(bar_data_x)
    # print(bar_data_y)
    # plt.rcParams['font.sans-serif'] = ['SimHei']
    # plt.rcParams['axes.unicode_minus'] = False
    # p1 = plt.bar(bar_data_x,bar_data_y,bottom=0.217)
    # for a,b in zip(bar_data_x,bar_data_y):
    #     plt.text(a,b + 0.05,'%.0f' % b,ha='center',va='bottom',fontsize=11)
    # plt.xticks(bar_data_x,rotation=-60)
    # plt.show()

# result_list={'product':{'num':0},'material':{'num'}}
# res=result_list.has_key('num')
# if 'num' in result_list['product']:
#     print('sss')
# print(res)