
'''
    说明：从偶数个元素的数组中 将两个元素两两组合，并将使用所有的 有多少种组合方式
    eg:arr=[0, 1, 2, 3, 4, 5] 
    组合情况1： ['0,1','2,3','4,5']
    组合情况1： ['0,1','2,4','3,5']
    组合情况3： ['0,1','2,5','3,4']
    arr[]:所有元素列表
    delarr:需要删除的组素
    cur_list：遍历的元素序号
    combine_list：每种组合情况
    arr=[i for i in range(4)]
'''
def rnnList(arr=[],delarr=[],layer=1,n=0,combine_arr=[]):
    # print('需要剔除的元素:{}'.format(delarr))
    temp_list=[val for val in arr if val not in delarr]
    del_temp=[val for val in delarr]
    min_list = min(temp_list)
    cur_list = [val for val in temp_list if val != min_list]
    if len(temp_list)<=2:
        combine_list=del_temp+[min_list]
        last_list=[val for val in arr if val not in combine_list]
        combine_list=combine_list+last_list
        print('组合元素：{}'.format(combine_list))
        return n

    # print('遍历的元素:{}'.format(cur_list))
    for i in cur_list:
        temp=del_temp+[min_list]+[i]
        rnnList(arr,temp,++layer,n)
'''
    说明：从数组中 将元素按照指定数量按顺序进行组合，并返回组合的结果
    eg:arr=[0, 1, 2, 3, 4, 5] 
    组合情况1： ['0,1','2,3','4,5']
    组合情况1： ['0,1','2,4','3,5']
    组合情况3： ['0,1','2,5','3,4']
    arr[]:所有元素列表
    cur:当前下标位置
    num：组合数量
    combine：组合结果
'''
def rnnNum(arr=[],cur=0,num=1,combine=[]):
    num = num - 1
    if num<0:
        print(combine)
        # yield combine
        return combine
    for index,i in enumerate(arr):
        if index >=cur:
            cur=cur+1
            temp=combine+[cur]
            rnnNum(arr,cur,num,temp)

    # print(return_list)

# rnnList(arr,[],1,int(0))
arr=[i for i in range(8)]
rnnNum(arr,0,3,[])


