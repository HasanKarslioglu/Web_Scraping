import ttkbootstrap as tb
from ttkbootstrap.dialogs import Messagebox
import csv
from datetime import date, timedelta, datetime
import request as rq

def display_hotels():
    filename = "myhotels.csv"
    data = read_csv(filename)
    
    for row_index, row in enumerate(data):
        for col_index, value in enumerate(row):
            if len(value) > 25:
                value = value[:22] + "..."
            label = tb.Label(right_frame_middle, text=value, style='Normal.TLabel', font=("Helvetica", 10))
            label.grid(row=row_index, column=col_index, pady=2, sticky='nsew')

    for i in range(len(data)):
        right_frame_middle.grid_rowconfigure(i, weight=1)

    for j in range(len(data[0])):
        right_frame_middle.grid_columnconfigure(j, weight=1)    
    right_frame_middle.configure(background="gray")

def change_city(x):
    global selected_city_var
    selected_city_var = x
    update_city()

def is_just_currency_changed():
    return old_check_in == selected_checkIn and old_check_out == selected_checkOut and old_city == selected_city_var and allowReRequest

def update_old_informations():
    global selected_city_var, selected_checkIn, selected_checkOut, old_check_in, old_check_out, old_city
    old_check_in = selected_checkIn
    old_check_out = selected_checkOut
    old_city = selected_city_var
    global allowReRequest 
    allowReRequest = True

def is_dates_correct():
    global selected_checkIn, selected_checkOut
    dateformat = "%Y-%m-%d"
    try:
        checkIn_date = datetime.strptime(selected_checkIn, dateformat).date()
        checkOut_date = datetime.strptime(selected_checkOut, dateformat).date()
        current_date = datetime.now().date()
    except ValueError:
        Messagebox.show_error("Invalid date format! Please enter the date in the 'YYYY-MM-DD' format.!","Invalid Date-Time!")
        return False
    
    if checkIn_date < current_date:
        Messagebox.show_error("Check-in date cannot be in the past!","Invalid Date-Time!")
        return False
    if checkIn_date > checkOut_date:
        Messagebox.show_error("Check-out date cannot be before the check-in date!","Invalid Date-Time!")
        return False
    return True

def show_date_error_message():
    mb = Messagebox.show_error("Please Enter Correct Date!","Invalid Date-Time!")

def submit_pressed():
    update_checkIn()
    update_checkOut()
    if not is_dates_correct():
        return
    update_city()
    if not is_just_currency_changed():
        update_downsize_info()
        if not rq.request(selected_city_var,selected_checkIn,selected_checkOut):
            Messagebox.show_error("An exception occurred during the request from 'booking.com'. Please check your Internet connection.","Request Error!")
            global allowReRequest 
            allowReRequest = False
            return
    update_price()
    display_hotels()
    update_old_informations()
    
def update_price():
    hotels = rq.read_csv('myhotels.csv')
    if hotels['price'][1] == "NOT GIVEN":
        display_hotels()
        return

    if isEuro.get() == 1:
        if str(hotels['price'][1]).startswith('Euro'):
            return
        hotels['price'] = hotels['price'].replace('TL', '', regex=True).replace(',', '', regex=True).replace(' ', '', regex=True).replace('\u00a0', '', regex=True).astype(float)
        hotels['price'] = round(hotels['price'] / 30, 1) 
        hotels['price'] = 'Euro ' + hotels['price'].astype(str)

        hotels.to_csv('myhotels.csv', index=False)
        display_hotels()
    else:
        if str(hotels['price'][1]).startswith('TL'):
            return
        hotels['price'] = hotels['price'].replace('Euro ', '', regex=True).astype(float)
        hotels['price'] = round(hotels['price'] * 30, 0)
        hotels['price'] = 'TL ' + hotels['price'].astype(str)

        hotels.to_csv('myhotels.csv', index=False)
        display_hotels()

def update_checkIn():
    global selected_checkIn
    selected_checkIn = check_in_date.entry.get()

def update_checkOut():
    global selected_checkOut
    selected_checkOut = check_out_date.entry.get()

def update_city():
    global selected_city_var 
    if selected_city_var == "":
        selected_city_var = "Rome"
    city_menu.configure(text=selected_city_var)

def update_downsize_info():
    selected_city_checkIn.config(text="Check In Date = "+ selected_checkIn)
    selected_city_label.config(text="City: "+ selected_city_var)
    selected_city_checkOut.config(text="Check Out Date= "+ selected_checkOut)

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
    data.sort(key=lambda x: float(x[4]), reverse=True)
    return data

selected_city_var = ""
selected_checkIn = ""
selected_checkOut = ""
old_check_in = ""
old_check_out = ""
old_city = ""
allowReRequest = True

root = tb.Window(themename="superhero", size=[1080,600], minsize=[800,600])
root.position_center()
root.title("Find Hotels!")
isEuro = tb.IntVar()
frame_left = tb.Frame(root, style='Normal.TLabel')
frame_left.grid(row=0, column=0, sticky='nswe', padx=10, pady=10)
frame_right = tb.Frame(root, style='Normal.TLabel')
frame_right.grid(row=0, column=1, sticky='nswe', padx=20, pady=10)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)
root.grid_rowconfigure(0, weight=1)

right_frame_top = tb.Label(frame_right)
right_frame_top.pack(side="top", pady=25, fill="x")
right_frame_middle = tb.Label(frame_right, style='secondary')
right_frame_middle.pack(side="top", expand = True, fill="both")
right_frame_bottom = tb.Label(frame_right)
right_frame_bottom.pack(side="bottom", pady=25, fill="x")

city_menu = tb.Menubutton(frame_left, text=next(iter(rq.city_destId)), bootstyle="primary, outline")
city_menu.pack(side="top", pady=55, padx=5)
inside_city_menu = tb.Menu(city_menu)
for x in rq.city_destId:
    inside_city_menu.add_radiobutton(label=x, variable=selected_city_var, command=lambda x=x: change_city(x))
city_menu["menu"] = inside_city_menu

check_in_name = tb.Label(frame_left, text="Check In", font=("Helvetica", 14))
check_in_name.pack(side="top")
check_in_date = tb.DateEntry(frame_left, bootstyle="primary",dateformat="%Y-%m-%d", firstweekday=7, startdate = date.today()  + timedelta(days=1))
check_in_date.pack(side="top", pady=6, padx=5)

check_out_name = tb.Label(frame_left, text="Check Out", font=("Helvetica", 14))
check_out_name.pack(side="top", pady=11, padx=5)
check_out_date = tb.DateEntry(frame_left,bootstyle="primary",dateformat="%Y-%m-%d",firstweekday=7, startdate = date.today()  + timedelta(days=4))
check_out_date.pack(side="top", padx=5)

separator = tb.Separator(frame_left, bootstyle="secondary")
separator.pack(side="top", pady=30, padx=30, fill="x")

checkButton = tb.Checkbutton(
    frame_left,
    bootstyle="info-round-toggle",
    text=" TL - EURO",
    variable=isEuro,
    onvalue=1,
    offvalue=0)
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
