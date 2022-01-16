import tkinter as tk
import csv
import geopy
import tksheet
from tkinter import filedialog
from geopy.geocoders import Nominatim


## Create window
window = tk.Tk()
window.title("AddressBook")

## Create Canvas (easy sizing)
canvas = tk.Canvas(window, width = 600, height = 300)
canvas.grid(columnspan = 5, rowspan = 3)

## Create table
sheet = tksheet.Sheet(window)

# Table functionalities
sheet.enable_bindings(("single_select",
                       "row_select",
                       "column_width_resize",
                       "arrowkeys",
                       "right_click_popup_menu",
                       "rc_select",
                       "rc_insert_row",
                       "rc_delete_row",
                       "copy",
                       "cut",
                       "paste",
                       "delete",
                       "undo",
                       "edit_cell"))


# Change table column names
sheet.headers(["Name", "Street", "ZIP", "City", "Phone"])
sheet.highlight_rows(rows =list(range(1,1000000, 2)), bg = "whitesmoke") # Highlight every second row - increase readability
sheet.align_columns(columns = [1,2,3,4], align = "e") # Align columns
sheet.header_font(newfont = ("Arial", 10, "normal"))
sheet.change_theme("light green")
for i in range(0, len(sheet.headers())):
    sheet.highlight_cells(column = i, bg="lightgrey", fg="darkgreen", canvas="header")



## Functions for buttons and menus
def open_file():
    file = filedialog.askopenfilename(parent = window, title = "Choose a CSV file", filetype = [("CSV file", "*.csv")])
    if file:
        with open(file) as csv_file:
            reader = csv.reader(csv_file, delimiter = ",")
            csv_output = list(reader)

        # Update table/sheet
        sheet.set_sheet_data(csv_output)


def save_file():
    data = [("csv file(*.csv)", "*.csv")]
    file = filedialog.asksaveasfilename(filetypes=data, defaultextension=data)

    with open(file, "w", newline = "") as myfile:
        csvwriter = csv.writer(myfile, delimiter=",")
        for d in sheet.get_sheet_data():
            csvwriter.writerow(d)


def cmdExit():
    window.destroy()


def counterButton():
    c = sum(txt.get() in s for s in sheet.get_column_data(0))
    number_of_counts.config(text = "{}".format(c))


def lokalize():
    row_data = sheet.get_row_data(sheet.get_currently_selected()[0])
    bundesland, plz, street = row_data[3], row_data[2], row_data[1]
    indy_500_address = f"{street}, {plz} {bundesland}"
    try:
        indy_500 = Nominatim(user_agent = "hausuebung 8").geocode(indy_500_address)
        gps_data.config(text = "{}: {} {}".format(bundesland, indy_500.latitude, indy_500.longitude))
    except AttributeError:
        gps_data.config(text = f"No GPS data found. Check Input!")



## Create menu
menu = tk.Menu(window)
about = tk.Menu(menu)
about.add_command(label = "Load", command = open_file)
about.add_command(label = "Save", command = save_file)
about.add_command(label="Exit",command = cmdExit)
menu.add_cascade(label = "File", menu=about)
window.config(menu=menu)


## Labels & Buttons
# Name label
name_string = tk.Label(window, text="Name:")
name_string.grid(column=0,row=1)

# Text field
txt = tk.Entry(window, width = 50)
txt.grid(columnspan = 2, column=1,row=1)

# Count button
count_btn = tk.Button(window, text = "Count", command = counterButton,
                      bg = "firebrick", fg = "white")
count_btn.grid(column = 3, row = 1)

# Count button output
number_of_counts = tk.Label(window)
number_of_counts.grid(column=4, row=1)

# Locate button
locate_btn = tk.Button(window, text = "Locate", command = lokalize,
                       bg = "black", fg = "white", height = 2, width = 10)
locate_btn.grid(column = 0, row = 2)

# GPS data label
gps_data = tk.Label(window)
gps_data.grid(column = 1, row = 2, columnspan = 2)



## Resizing of the window
window.grid_columnconfigure(1, weight=1)
# First column gets 100% weight by resizing window
window.grid_rowconfigure(0, weight=1)
# First row gets 100% weight by resizing window
sheet.grid(column=0, row=0, columnspan=5, sticky="nswe")
# Sticky attribut

# Add space at the bottom with canvas grid
canvas = tk.Canvas(window, width = 600, height = 10)
canvas.grid(columnspan = 5)


window.mainloop()
