import os
from tkinter import *
from PIL import Image, ImageTk
import  cv2 as cv
import numpy as np
# os.chdir('D:/programe/matlab/img')




class GUI():
    def __init__(self,window):
        self.window = window
        #title
        self.window.title("HsvMaster")
        #siz=800*600,position=(500,200)
        self.window.geometry('1000x600+500+200')
        self.window["bg"] = "DimGray"
        # icon
        self.icon = ImageTk.PhotoImage(file='photo/favicon.ico')
        self.window.call('wm','iconphoto',self.window._w,self.icon)
        self.temp_img=''
        self.hmin=0
        self.hmax=0
        self.smin=0
        self.smax=0
        self.vmin=0
        self.vmax=0

    def create_widgets(self):

        #scale
        self.hmin_label = Label(self.window,text='色调下限',fg='WhiteSmoke',bg="DimGray")
        self.hmin_scale = Scale(self.window,orient=HORIZONTAL,from_=0,to=255,resolution=1,tickinterval=50,length=200,width=7,fg='WhiteSmoke',bg="DimGray",command=lambda value, name='hmin': self.report_change(name, value))
        self.hmax_label = Label(self.window,text='色调上限',fg='WhiteSmoke',bg="DimGray")
        self.hmax_scale = Scale(self.window,orient=HORIZONTAL,from_=0,to=255,resolution=1,tickinterval=50,length=200,width=7,fg='WhiteSmoke',bg="DimGray",command=lambda value, name='hmax': self.report_change(name, value))
        self.smin_label = Label(self.window,text='饱和度下限',fg='WhiteSmoke',bg="DimGray")
        self.smin_scale = Scale(self.window,orient=HORIZONTAL,from_=0,to=255,resolution=1,tickinterval=50,length=200,width=7,fg='WhiteSmoke',bg="DimGray",command=lambda value, name='smin': self.report_change(name, value))
        self.smax_label = Label(self.window,text='饱和度上限',fg='WhiteSmoke',bg="DimGray")
        self.smax_scale = Scale(self.window,orient=HORIZONTAL,from_=0,to=255,resolution=1,tickinterval=50,length=200,width=7,fg='WhiteSmoke',bg="DimGray",command=lambda value, name='smax': self.report_change(name, value))
        self.vmin_label = Label(self.window,text='明度下限',fg='WhiteSmoke',bg="DimGray")
        self.vmin_scale = Scale(self.window,orient=HORIZONTAL,from_=0,to=255,resolution=1,tickinterval=50,length=200,width=7,fg='WhiteSmoke',bg="DimGray",command=lambda value, name='vmin': self.report_change(name, value))
        self.vmax_label = Label(self.window,text='明度上限',fg='WhiteSmoke',bg="DimGray")
        self.vmax_scale = Scale(self.window,orient=HORIZONTAL,from_=0,to=255,resolution=1,tickinterval=50,length=200,width=7,fg='WhiteSmoke',bg="DimGray",command=lambda value, name='vmax': self.report_change(name, value))

        # scale position
        self.hmin_label.grid(row=0, column=0,padx=15)
        self.hmin_scale.grid(row=0,column=1,pady=2)
        self.hmax_label.grid(row=1, column=0)
        self.hmax_scale.grid(row=1,column=1,pady=2)
        self.smin_label.grid(row=2, column=0)
        self.smin_scale.grid(row=2,column=1,pady=2)
        self.smax_label.grid(row=3, column=0)
        self.smax_scale.grid(row=3,column=1,pady=2)
        self.vmin_label.grid(row=4, column=0)
        self.vmin_scale.grid(row=4,column=1,pady=2)
        self.vmax_label.grid(row=5, column=0)
        self.vmax_scale.grid(row=5,column=1,pady=2)

        #img
        self.img = Image.open('photo/1.jpg')
        self.img = self.img.resize((300, 300))
        print(self.img)
        self.img_box = ImageTk.PhotoImage(self.img)

        self.orign = Label(self.window,image=self.img_box,width=300,height=300)
        self.work = Label(self.window,image=self.img_box,width=300,height=300)
        #img position
        self.orign.place(x=320, y=30)
        self.work.place(x=650,y=30)

        #Button
        self.import_button = Button(self.window, text='导入原图',font=('隶书',45), height=2, width=9,fg='WhiteSmoke',bg="BurlyWood")
        self.clear_button = Button(self.window, text='删除所有',font=('隶书',12), height=2, width=15,fg='WhiteSmoke',bg="BurlyWood")
        self.delete_button = Button(self.window, text='删除当前',font=('隶书',12), height=2, width=15,fg='WhiteSmoke',bg="BurlyWood")
        self.switch_button = Button(self.window,text='区域切换',font=('隶书',12), height=2, width=15,fg='WhiteSmoke',bg="BurlyWood")
        self.save_button = Button(self.window, text='区域暂存',font=('隶书',12), height=2, width=15,fg='WhiteSmoke',bg="BurlyWood")
        self.merge_button = Button(self.window, text='合并区域',font=('隶书',12), height=2, width=15,fg='WhiteSmoke',bg="BurlyWood")
        self.picture_button = Button(self.window, text='生成图片',font=('隶书',12), height=2, width=15,fg='WhiteSmoke',bg="BurlyWood")

        #button position
        self.import_button.place(x=18,y=400)
        self.clear_button.place(x=370,y=420)
        self.delete_button.place(x=570,y=420)
        self.switch_button.place(x=770,y=420)
        self.save_button.place(x=370,y=500)
        self.merge_button.place(x=570,y=500)
        self.picture_button.place(x=770,y=500)
    def report_change(self,name,value):
        print(name,value)
        name=getattr(self,name)
        name = value
        print(name)
        print(self.hmin)
        # print(self.name=name)
    def print_selection(self,v):

        if self.hmax<int(v):
            print(v)
            self.hmax=int(v)
            self.hmax_scale.set(self.hmax)
        # print(self.img)
        self.temp_img=np.array(self.img)
        # print(img)
        self.temp_img = cv.GaussianBlur(self.temp_img,(9,9),int(v))
        _,binary = cv.threshold(self.temp_img,int(v),255,cv.THRESH_TOZERO)
        cv.imshow('blur',binary)
        cv.imshow('gua',self.temp_img)
        # print(img)
        img_gauss = Image.fromarray(cv.cvtColor(self.temp_img,cv.COLOR_BGR2RGB))
        # self.img = Image.fromarray(cv.cvtColor(img,cv.COLOR_BGR2RGB))
        # print(temp+int(v))
        # self.img_box = ImageTk.PhotoImage(img_gauss)
        # self.orign.configure(image=self.img_box)


        # self.window.update()
        # self.orign = Label(self.window,image=self.img_box,width=300,height=300)

def gui_start():

    my_window = Tk()
    my_gui = GUI(my_window)
    my_gui.create_widgets()
    my_window.mainloop()


gui_start()
