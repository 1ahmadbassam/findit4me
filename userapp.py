from dbhelper import DatabaseHelper as db
import tkinter as tk
from tkinter import messagebox,filedialog
from PIL import ImageTk,Image  
import tkinter.ttk as ttk
import utils
from utils import MultiListbox
import ctypes
import shoplogin
import shutil
import os
import time

def update_item_list(rows):
    item_list.delete(0, tk.END)
    for row in rows:
        item_list.insert(tk.END,(str(row[0]), str(row[2]), str(row[1])))

def search(query, location):
    if query:
        conn = db.create_connection(db.dbfile)
        if conn is not None:
            rows = db.query_string_location(conn, query, location)
            if rows is not None:
                update_item_list(rows)
        else:
            print(utils.DATABASE_ERROR)

def main():
    window = tk.Tk()
    window.title(utils.appname)
    utils.set_window_icon(window)

    welcome_label = tk.Label(
        window, text="Welcome to " + utils.appname, font=(utils.titlefont, 24))
    welcome_label.pack()
    welcome_label2 = tk.Label(
        window, text="What are you searching for today?", font=(utils.titlefont, 16))
    welcome_label2.pack()

    search_box_frame = tk.Frame(window)
    search_box_frame.pack(padx=10, pady=10, fill=tk.BOTH)
    search_box = tk.Entry(search_box_frame, borderwidth=3, font=(utils.entryfont, utils.largefontsize))
    utils.create_entry_hint(search_box, "Search...")
    search_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    global search_image
    search_image = tk.PhotoImage(file=r"search_icon2.png")
    search_button = tk.Button(search_box_frame, image=search_image, command= lambda: search(search_box.get(), location_combox.get()))
##    search_button["bg"] = "white"
##    search_button["border"] = "0"
    search_button.pack(side=tk.RIGHT, padx=(4,0))

    location_frame = tk.Frame(window)
    location_frame.pack(padx=5, pady=5, fill=tk.BOTH)

    location_label = tk.Label(location_frame, text="Your Location:", font=(utils.entryfont, utils.stdfontsize))
    location_label.pack(side=tk.LEFT, padx=(5,0))

    location_combox = ttk.Combobox(
        location_frame, state='readonly', font=(utils.labelfont, utils.stdfontsize))
    location_combox['values'] = utils.locations
    location_combox.current(0)
    location_combox.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=5)

    hint_label = tk.Label(window, text="Hint: select an item to see more information.", font=(utils.hintfont, utils.hintfontsize))
    hint_label.pack()

    def select_list_item(event):
            cs = item_list.curselection()
            selectlistitem_window = tk.Toplevel()
            selectlistitem_window.title("Viewing details for " + item_list.get(cs)[0])
            utils.set_window_icon(selectlistitem_window)

            conn = db.create_connection(db.dbfile)
            if conn is not None:
                phonenumber= db.get_phone_for_shop(conn, item_list.get(cs)[1])[0]
            else:
                print(utils.DATABASE_ERROR)

            selectlistitem_title = tk.Label(selectlistitem_window, font=(utils.titlefont, utils.largefontsize),text=item_list.get(cs)[2] + " of this item present at " + item_list.get(cs)[1] + ". Their phone number is " + phonenumber + ".")
            selectlistitem_title.pack(padx=10, pady=10)
            global selectlistitem_canvas
            selectlistitem_canvas = tk.Canvas(selectlistitem_window)  
            selectlistitem_canvas.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
            conn = db.create_connection(db.dbfile)
            if conn is not None:
                image_loc = db.get_image_for_item(conn, item_list.get(cs)[1], item_list.get(cs)[0])[0]
                global image2
                if image_loc:
                    image2 = ImageTk.PhotoImage(Image.open(image_loc))  
                    selectlistitem_canvas.create_image(20, 20, anchor=tk.NW, image=image2)
                else:
                    image2 = ImageTk.PhotoImage(Image.open(utils.placeholder))  
                    selectlistitem_canvas.create_image(20, 20, anchor=tk.NW, image=image2)
            else:
                print(utils.DATABASE_ERROR)
    global item_list
    item_list = MultiListbox(
        window, ((utils.itemname, 40), (utils.shopname, 40), (utils.itemquantity, 20)))
    item_list.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    item_list.bind('<<MultiListboxSelect>>', select_list_item)

    window.mainloop()

if __name__ == '__main__':
    main()
