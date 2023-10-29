import mh_z19  #This module only works on Pi's
import os #this code is written for a pi, which uses linux. This code won't work on windows or mac

import tkinter as tk
from tkinter import * 
from tkinter import ttk #importing all the tkinter stuff

co = 0 #Not sure why i named the CO2 variable "co", but i did
update_int = 1


root = Tk() #creating our root tkinter object

def add_co(): #add_co and remove_co are functions i use while debuging. They have no other use
    global co
    co += 10
  
def remove_co():
    global co
    co -= 10
    
def spin_box(): #spin_box and spin_box2 are for handling when the values of the 2 spin boxes change.
    global update_int
    update_int = int(thing.get())
  
def spin_box2():
    global text_size
    co_level.config(font=('Times', text_size))
    text_size = int(thing2.get())
    update_labels()

#add = Button(root, command=add_co, text = "Add 10 CO2")
#add.pack()
#remove = Button(root, command=remove_co, text = "Remove 10 CO2")  #this is code for debugging when a sensor isnt available. They simulate the co2 changing
#remove.pack()


text_size = 10 #default font size - TODO: find a way to set the default spinbox value to this aswell

padding_label = Label(root, text=" ", font=("Times", 20))
padding_label.pack() #creating an object for padding (probably a better way but whatever)

co_level = tk.Label(root, text="CO2: ", font=('Times', text_size))
co_level.pack() #The CO2 level label cant be .place()'d because it becomes off-centre when the size is changed.


thing = ttk.Spinbox(root, wrap=True, from_ = 1, to=10, width=3, command=spin_box)
thing.place(x=250,y=70+text_size)

label1 = Label(root, text="Update interval: ")
label1.place(x=150, y=70+text_size)
label2 = Label(root, text="seconds")
label2.place(x=310, y =70+text_size)

thing2 = ttk.Spinbox(root, wrap=False, from_ = 5, to=35, width=3, command=spin_box2)
thing2.place(x=250,y=90+text_size)

label3 = Label(root, text="Font size: ")
label3.place(x=150, y=90+text_size)

full = tk.IntVar()
full_c = ttk.Checkbutton(root, text='Show full ppm',variable=full, onvalue=1, offvalue=0)
full_c.place(x=150, y = 120+text_size)

label4 = Label(root, text="", fg="red")
label4.place(x=100, y = 150+text_size)

def update_labels(): #this function moves the position of everything below the co2 level label whenever its size changes
    global text_size
    thing.pack_forget()
    label1.pack_forget()
    label2.pack_forget()
    thing2.pack_forget()
    label3.pack_forget()
    full_c.pack_forget()
    label4.pack_forget()
    thing.place(x=250,y=73+text_size)
    label1.place(x=150, y=73+text_size)
    label2.place(x=310, y =73+text_size)
    thing2.place(x=250,y=93+text_size)
    label3.place(x=150, y=93+text_size)
    full_c.place(x=150, y = 120+text_size)
    label4.place(x=100, y = 150+text_size)




def loop(): # this code runs every update_int seconds. It is responsible for checking the CO2 level and displaying error.
    global update_int
    global co
    if int(os.getuid()) == 1000:
        label4.config(text="""The program is not running as admin!
Please restart as admin [1]""")
    else:
        if "[1]" in label4.cget("text"):
            label4.config(text="")
    print("updating co2")
    try:
        co = mh_z19.read()['co2']
    except:
        label4.config(text="No data recieved. Sensor may be disconnected [2]")
    else:
        if "[2]" in label4.cget("text"):
            label4.config(text="")
    print(co)
    if co == 436 or co == 550: #436 and 550 are the magic values you recieve when the sensors re-calibrating. E.g. when its turned on, and when it's data cables get disconnected
        label4.config(text="""Sensor is re-calibrating. Data cables may have been
re-connected. This may take a few minutes [3]""")
    else:
        if "[3]" in label4.cget("text"):
            label4.config(text="")
    if full.get() == 1:
        co_level.config(text = "CO2: " + str(co) + " Parts Per Million")
    else:
        co_level.config(text = "CO2: " + str(co) + " ppm")
        
    root.after(update_int*1000, loop) #recursion after update_int * 1000 miliseconds


root.after(100, loop)
root.geometry("500x500") #sets up window size. TODO- make window a bit shorter
root.title("CO2 Sensor") #names the window
root.mainloop() #starts the tkinter mainloop
