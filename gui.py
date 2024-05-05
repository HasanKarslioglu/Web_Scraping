import tkinter as tk
from ttkbootstrap.constants import *
import ttkbootstrap as tb
import csv
from datetime import date, timedelta


root = tb.Window(themename="superhero", size=[800,600], maxsize=[1080,720])
root.position_center()
root.title("Semusu çok seviyorum!")

# Sol Frame
frame_left = tb.Frame(root, style='Normal.TLabel')
frame_left.grid(row=0, column=0, sticky='nswe', padx=10, pady=10)

root.grid_columnconfigure(0, weight=2)

# Sağ Frame
frame_right = tb.Frame(root, style='secondary')
frame_right.grid(row=0, column=1, sticky='nswe', padx=10, pady=10)

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
            label = tb.Label(frame_right, text=value, style='Normal.TLabel')
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

city_menu = tb.Menubutton(frame_left, text="City", bootstyle="primary, outline")
city_menu.pack(side="top", pady=50, padx=5)

selected_city_var = ""
selected_checkIn = ""
selected_checkOut = ""
isEuro = tb.IntVar()

def change_city(x):
    global selected_city_var
    selected_city_var = x
def change_euro_tl():
    if isEuro.get() == 1:
        print(isEuro.get())
    else:
        print(isEuro.get())

inside_city_menu = tb.Menu(city_menu)
for x in ["Ankara", "Diyarbakır", "Yozgat", "Kırıkkale", "İzmir"]:
    inside_city_menu.add_radiobutton(label=x, variable=selected_city_var, command=lambda x=x: change_city(x))
city_menu["menu"] = inside_city_menu

check_in_name = tb.Label(frame_left, text="Check In", font=("Helvetica", 14))
check_in_name.pack(side="top")

check_in_date = tb.DateEntry(frame_left, bootstyle="primary",dateformat="%d-%m-%Y", firstweekday=7, startdate = date.today()  + timedelta(days=1))
check_in_date.pack(side="top", pady=11, padx=5)

def submit_pressed():
    update_checkIn()
    update_checkOut()
    update_city()

def update_checkIn():
    new_date = check_in_date.entry.get()
    selected_city_checkIn.config(text="Check In = "+ new_date)
    print(check_in_date.entry.get())

def update_checkOut():
    new_date = check_out_date.entry.get()
    selected_city_checkOut.config(text="Check Out = "+ new_date)

def update_city():
    selected_city_label.config(text="City: "+ selected_city_var)


check_out_name = tb.Label(frame_left, text="Check Out", font=("Helvetica", 14))
check_out_name.pack(side="top", pady=11, padx=5)

check_out_date = tb.DateEntry(frame_left,bootstyle="primary",dateformat="%d-%m-%Y",firstweekday=7, startdate = date.today()  + timedelta(days=4))
check_out_date.pack(side="top", padx=5)

separator = tb.Separator(frame_left, bootstyle="secondary")
separator.pack(side="top", pady=30, padx=30, fill="x")
checkButton = tb.Checkbutton(
    frame_left,
    bootstyle="info-round-toggle",
    text=" TL - EURO",
    variable=isEuro,
    onvalue=1,
    offvalue=0,
    command=change_euro_tl)
checkButton.pack(side="top", padx=30)

submit_button = tb.Button(frame_left, text="Submit!", bootstyle="Success, outline", command=submit_pressed)
submit_button.pack(side="top", pady=25, padx=5)

selected_city_label = tb.Label(frame_left, text=selected_city_var,font=("Helvetica", 11), bootstyle="info")
selected_city_label.pack(side="top", pady=2, padx=5)
selected_city_checkIn = tb.Label(frame_left, text=selected_checkIn, font=("Helvetica", 11), bootstyle="info")
selected_city_checkIn.pack(side="top", pady=2, padx=5)
selected_city_checkOut = tb.Label(frame_left, text=selected_checkOut, font=("Helvetica", 11), bootstyle="info")
selected_city_checkOut.pack(side="top", pady=2, padx=5)



root.mainloop()
