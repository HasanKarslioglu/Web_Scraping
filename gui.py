import tkinter as tk
from ttkbootstrap.constants import *
import ttkbootstrap as tb
import csv


root = tb.Window(themename="superhero", size=[800,600], maxsize=[1080,720])
root.position_center()
root.title("Semusu çok seviyorum!")

# Sol Frame
frame_left = tb.Frame(root, style='primary')
frame_left.grid(row=0, column=0, sticky='nswe')
root.grid_columnconfigure(0, weight=2)

# Sağ Frame
frame_right = tb.Frame(root, style='secondary')
frame_right.grid(row=0, column=1, sticky='nswe')
root.grid_columnconfigure(1, weight=1)


root.grid_rowconfigure(0, weight=1)

# CSV dosyasından verileri okuyup bir liste olarak döndüren fonksiyon
def read_csv(filename):
    data = []
    with open(filename, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        count = 0
        for row in reader:
            if count > 5:
              break
            count += 1
            data.append(row)
    data = data[1:]
    print(data)
    data.sort(key=lambda x: float(x[4]), reverse=True)
    return data

# Verileri ekrana yazdıran fonksiyon
def display_data(data):
    for row_index, row in enumerate(data):
        for col_index, value in enumerate(row):
            label = tb.Label(frame_right, text="   "+value, style='Normal.TLabel')
            label.grid(row=row_index, column=col_index, pady=2, sticky='nsew')

# CSV dosyasından verileri oku
filename = "test_hotels.csv"
data = read_csv(filename)

# Verileri ekrana yazdır
display_data(data)

# Tabloyu düzenle
for i in range(len(data)):
    frame_right.grid_rowconfigure(i, weight=1)

for j in range(len(data[0])):
    frame_right.grid_columnconfigure(j, weight=1)

root.mainloop()
