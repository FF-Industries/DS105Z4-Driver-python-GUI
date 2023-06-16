# !/usr/bin/python3
from tkinter import *
from ds1054z import DS1054Z
from tkinter import messagebox

top = Tk()
top.geometry("100x100")

def helloCallBack():
   scope = DS1054Z('169.254.1.5')
   
   #msg = messagebox.showinfo( "Hello Python", "Hello World")

B = Button(top, text = "Connect", command = helloCallBack)
B.place(x = 50,y = 50)

top.mainloop()