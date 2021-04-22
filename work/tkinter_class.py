import tkinter as tk
from redis_scrapy import RedisQueue
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.name = tk.StringVar()
        self.master = master
        self.pack()
        self.master.geometry('380x300')
        self.create_widgets()


    def create_widgets(self):

        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World (click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.input_text()

        self.show = tk.Button(self,text="显示",fg="red",
                              command=self.setlabel)
        self.show.pack(side="bottom")

        self.label_text = tk.StringVar()
        self.label_text.set("----")
        self.lable = tk.Label(self,
                              textvariable=self.label_text,
                              font=('Arial',11),width=15,height=2)
        self.lable.pack()

        self.quit = tk.Button(self,text="QUIT",fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        redis_object=RedisQueue('keyword_url')
        size=redis_object.qsize()
        print(size)

    def get_input(self):
        print(self.name.get())

    def setlabel(self):
        print(self.name)
        self.content=self.name
        self.label_text.set(self.content)

    def input_text(self):

        tk.Label(text='输入框').pack()
        E1 = tk.Entry(bd=5,textvariable=self.name)
        E1.pack(side='left')
        self.submit = tk.Button(self)
        self.submit["text"] = "提交"
        self.submit["command"] = self.get_input
        self.submit.pack(side="right")


root = tk.Tk()
app = Application(master=root)
app.mainloop()