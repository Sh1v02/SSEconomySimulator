from tkinter import *

slider = Tk()
slider.configure(bg = "aqua")
slider.geometry("800x800")

w = Scale(slider, bg = "aqua", borderwidth = 2, highlightbackground = "aqua", from_=0, to=50, length = 780, tickinterval = 10,
          orient=HORIZONTAL, resolution = 0.5)
w.set(14)
w.place(x = 10, y = 250, height = 100)


def showit():
    print(w.get())
    
Confirm = Button(slider, text = "Confirm", bg = "light grey", foreground = "black",
                     command = lambda: showit()).place(x = 300, y = 650, width = 200, height = 100)








