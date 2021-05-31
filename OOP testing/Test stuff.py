from tkinter import *

accepted = Toplevel()
accepted.title("Welcome")
Message(accepted, text="Nicee").pack()
accepted.after(2000, accepted.destroy)
