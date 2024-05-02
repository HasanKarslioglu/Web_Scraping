from tkinter import *
from ttkbootstrap.constants import *
import ttkbootstrap as tb

counter = 0
def changer():
  global counter
  counter += 1
  if counter % 2 == 0:
    my_label.config(text="Hello World!", bootstyle="success")
  else:
    my_label.config(text="Goodby World!", bootstyle="danger")
    
root = tb.Window(themename="superhero", size=[800,600], maxsize=[1080,720])
root.position_center()
root.title("Semusu çok seviyorum!")


my_label = tb.Label(text="Hello World", font=("Helvetica", 28), bootstyle="success")
my_label.pack(pady=50)


B = Button(root, text ="Hello")
B.pack(pady=10)

my_button = tb.Button(text="Click Me!", bootstyle="primary, outline", command=changer)
my_button.pack(pady=20)

root.mainloop()