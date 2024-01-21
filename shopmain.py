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

def update_item_list():
    conn = db.create_connection(db.dbfile)
    if conn is not None:
        rows = db.get_shop_items(conn, shopname)
        if rows is not None:
            item_list.delete(0, tk.END)
            for row in rows:
                item_list.insert(tk.END,(str(row[0]), str(row[1])))
            conn.close()
        else:
            print(utils.DATABASE_ERROR)
    else:
        print(utils.DATABASE_ERROR)


def complete_additem(itemname, quantity, window):
    global image_loc
    if not quantity:
        quantity = "0"
    conn = db.create_connection(db.dbfile)
    if conn is not None:
        if db.locate_item_exist_in_shop(conn, shopname, itemname) == 0:
            ctypes.windll.user32.MessageBoxW(
                0, "Item already exists!", utils.ADDITEM_ERROR, 0)
            conn.close()
        else:
            if not itemname and not quantity:
                ctypes.windll.user32.MessageBoxW(
                    0, "Entries can't be empty!", utils.ADDITEM_ERROR, 0)
            elif len(itemname) < 4:
                ctypes.windll.user32.MessageBoxW(
                    0, "Item name is too short! It should at least be 4 characters!", utils.ADDITEM_ERROR, 0)
            elif not quantity.isnumeric():
                ctypes.windll.user32.MessageBoxW(
                    0, "Invalid quantity!", utils.ADDITEM_ERROR, 0)
            else:
                db.add_item_to_shop(conn, shopname, (itemname, quantity, image_loc))
                conn.close()
                update_item_list()
                image_loc = None
                window.destroy()
    else:
        print(utils.DATABASE_ERROR)

def complete_updateitem(originalname, itemname, quantity, window):
    global image_loc
    if not quantity:
        quantity = "0"
    conn = db.create_connection(db.dbfile)
    if conn is not None:
        if not itemname and not quantity:
            ctypes.windll.user32.MessageBoxW(
                0, "Entries can't be empty!", utils.EDITITEM_ERROR, 0)
        elif len(itemname) < 4:
            ctypes.windll.user32.MessageBoxW(
                0, "Item name is too short! It should at least be 4 characters!", utils.EDITITEM_ERROR, 0)
        elif not quantity.isnumeric():
            ctypes.windll.user32.MessageBoxW(
                0, "Invalid quantity!", utils.EDITITEM_ERROR, 0)
        else:
            db.update_item(conn, shopname, originalname, itemname, quantity, image_loc)
            conn.close()
            update_item_list()
            image_loc = None
            window.destroy()
    else:
        print(utils.DATABASE_ERROR)

def main(p_shopname, p_password):
    global shopname
    global password
    shopname = p_shopname
    password = p_password

    window = tk.Tk()
    window.title(utils.appname)
    utils.set_window_icon(window)

    welcome_label = tk.Label(
        window, text="Welcome, " + shopname, font=(utils.titlefont, utils.hugefontsize))
    welcome_label.grid(column=0, row=0, padx=10, pady=10)

    item_list_frame = tk.Frame(window)
    item_list_frame.grid(column=0, row=1, sticky=tk.NSEW, padx=10, pady=10)

    global item_list
    item_list = MultiListbox(
        item_list_frame, ((utils.itemname, 50), (utils.itemquantity, 20)))
    item_list.pack(expand=True, fill=tk.BOTH)
    update_item_list()

    hint_label = tk.Label(item_list_frame, text="Hint: select an item to see its image.", font=(utils.hintfont, utils.hintfontsize))
    hint_label.pack()
    def select_list_item(event):
        cs = item_list.curselection()
        selectlistitem_window = tk.Toplevel()
        selectlistitem_window.title("Viewing details for " + item_list.get(cs)[0])
        utils.set_window_icon(selectlistitem_window)
        global selectlistitem_canvas
        selectlistitem_canvas = tk.Canvas(selectlistitem_window)  
        selectlistitem_canvas.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
        conn = db.create_connection(db.dbfile)
        if conn is not None:
            image_loc = db.get_image_for_item(conn, shopname, item_list.get(cs)[0])[0]
            global image2
            if image_loc:
                image2 = ImageTk.PhotoImage(Image.open(image_loc))  
                selectlistitem_canvas.create_image(20, 20, anchor=tk.NW, image=image2)
            else:
                image2 = ImageTk.PhotoImage(Image.open(utils.placeholder))  
                selectlistitem_canvas.create_image(20, 20, anchor=tk.NW, image=image2)
        else:
            print(utils.DATABASE_ERROR)
    item_list.bind('<<MultiListboxSelect>>', select_list_item)
    
    # handle adding an item similar to the sign up button using a toplevel
    def additem():
        global image_loc
        image_loc = ''
        additem_window = tk.Toplevel()
        additem_window.title("Add Item")
        utils.set_window_icon(additem_window)

        additem_label = tk.Label(
            additem_window, text="Great, what do you have to offer?", font=(utils.titlefont, utils.largefontsize))
        additem_label.pack(padx=10, pady=10)

        additem_itemname_frame = tk.Frame(additem_window)
        additem_itemname_frame.pack(fill=tk.X, padx=10, pady=10)
        additem_itemname_label = tk.Label(
            additem_itemname_frame, text="Item Name:", font=(utils.labelfont, utils.stdfontsize))
        additem_itemname_label.pack(side=tk.LEFT, padx=(0, 4))
        additem_itemname_entry = tk.Entry(
            additem_itemname_frame, borderwidth=3, font=(utils.entryfont, utils.stdfontsize))
        additem_itemname_entry.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        utils.create_entry_hint(additem_itemname_entry, utils.itemname_hint)

        additem_itemquantity_frame = tk.Frame(additem_window)
        additem_itemquantity_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        additem_itemquantity_frame.grid_rowconfigure(0, weight=1)
        additem_itemquantity_frame.grid_columnconfigure(0, weight=1)
        additem_itemquantity_frame.grid_columnconfigure(1, weight=1)
        additem_itemquantity_label = tk.Label(
            additem_itemquantity_frame, text="Qunatity:", font=(utils.labelfont, utils.stdfontsize))
        additem_itemquantity_label.grid(
            column=0, row=0, sticky=tk.E, padx=(0, 4))
        additem_itemquantity_entry = tk.Entry(
            additem_itemquantity_frame, borderwidth=3, font=(utils.entryfont, utils.stdfontsize))
        additem_itemquantity_entry.grid(column=1, row=0, sticky=tk.W)
        utils.create_entry_hint(additem_itemquantity_entry, utils.itemquantity_hint)

        def get_image():
            filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select an Image",
                                          filetypes = [("Image Files",
                                                        ".JPG .PNG .GIF .WEBP .TIFF .PSD .RAW .BMP .HEIF .INDD .JPEG .SVG .AI .EPS .PDF")])

            f, extension = os.path.splitext(filename)
            global image_loc
            image_loc = os.getcwd() + "\\images\\" + str(int(round(time.time() * 1000))) + extension
            os.makedirs(os.path.dirname(image_loc), exist_ok=True)
            shutil.copyfile(filename,image_loc)

            global image
            image = ImageTk.PhotoImage(Image.open(image_loc))  
            additem_canvas.create_image(20, 20, anchor=tk.NW, image=image) 
            
        additem_browseimage_button = tk.Button(
            additem_window, text="Browse for Image..", borderwidth=4, command=get_image,
                              font=(utils.buttonfont, utils.stdfontsize))
        additem_browseimage_button.pack(pady=10)

        global additem_canvas
        additem_canvas = tk.Canvas(additem_window, width = 300, height = 300)  
        additem_canvas.pack(padx=10, pady=10)
        global image4
        image4 = ImageTk.PhotoImage(Image.open(utils.placeholder))  
        additem_canvas.create_image(20, 20, anchor=tk.NW, image=image4)

        additem_additem_button = tk.Button(
            additem_window, text="Add Item", borderwidth=4, command=lambda: complete_additem(additem_itemname_entry.get(), additem_itemquantity_entry.get(), additem_window),
                              font=(utils.buttonfont, utils.stdfontsize))
        additem_additem_button.pack(pady=10)

    button_frame = tk.Frame(window)
    button_frame.grid(column=1, row=1, padx=(0, 10), pady=(0, 10))

    

    additem_button = tk.Button(
        button_frame, text="Add Item", font=(utils.buttonfont, utils.stdfontsize), command=additem)
    additem_button.pack()

    def deleteitem():
        WarningBox = tk.messagebox.askquestion ('Delete Item','Are you sure you want to delete this item?',icon = 'warning')
        if WarningBox == utils.YES:
            conn = db.create_connection(db.dbfile)
            if conn is not None:
                db.delete_item(conn, shopname, item_list.get(item_list.curselection()[0])[0].strip())
                conn.close()
                update_item_list()
            else:
                print(utils.DATABASE_ERROR)

    deleteitem_button = tk.Button(
        button_frame, text="Delete Item", font=(utils.buttonfont, utils.stdfontsize), command=deleteitem)
    deleteitem_button.pack(pady=10)

    def updateitem(itemname, itemquantity):
        global image_loc
        image_loc = ''
        originalname = itemname
        updateitem_window = tk.Toplevel()
        updateitem_window.title("Edit Item")
        utils.set_window_icon(updateitem_window)

        updateitem_label = tk.Label(
            updateitem_window, text="Make your changes", font=(utils.titlefont, utils.largefontsize))
        updateitem_label.pack(padx=10, pady=10)

        updateitem_itemname_frame = tk.Frame(updateitem_window)
        updateitem_itemname_frame.pack(fill=tk.X, padx=10, pady=10)
        updateitem_itemname_label = tk.Label(
            updateitem_itemname_frame, text="Item Name:", font=(utils.labelfont, utils.stdfontsize))
        updateitem_itemname_label.pack(side=tk.LEFT, padx=(0, 4))
        updateitem_itemname_entry = tk.Entry(
            updateitem_itemname_frame, borderwidth=3, font=(utils.entryfont, utils.stdfontsize))
        updateitem_itemname_entry.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        updateitem_itemname_entry.delete(0, tk.END)
        updateitem_itemname_entry.insert(0, itemname)
        utils.create_entry_hint(updateitem_itemname_entry, utils.itemname_hint)

        updateitem_itemquantity_frame = tk.Frame(updateitem_window)
        updateitem_itemquantity_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        updateitem_itemquantity_frame.grid_rowconfigure(0, weight=1)
        updateitem_itemquantity_frame.grid_columnconfigure(0, weight=1)
        updateitem_itemquantity_frame.grid_columnconfigure(1, weight=1)
        updateitem_itemquantity_label = tk.Label(
            updateitem_itemquantity_frame, text="Qunatity:", font=(utils.labelfont, utils.stdfontsize))
        updateitem_itemquantity_label.grid(
            column=0, row=0, sticky=tk.E, padx=(0, 4))
        updateitem_itemquantity_entry = tk.Entry(
            updateitem_itemquantity_frame, borderwidth=3, font=(utils.entryfont, utils.stdfontsize))
        updateitem_itemquantity_entry.grid(column=1, row=0, sticky=tk.W)
        updateitem_itemquantity_entry.delete(0, tk.END)
        updateitem_itemquantity_entry.insert(0, itemquantity)
        utils.create_entry_hint(updateitem_itemquantity_entry, utils.itemquantity_hint)

        def get_image():
            filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select an Image",
                                          filetypes = [("Image Files",
                                                        ".JPG .PNG .GIF .WEBP .TIFF .PSD .RAW .BMP .HEIF .INDD .JPEG .SVG .AI .EPS .PDF")])

            f, extension = os.path.splitext(filename)
            global image_loc
            image_loc = os.getcwd() + "\\images\\" + str(int(round(time.time() * 1000))) + extension
            os.makedirs(os.path.dirname(image_loc), exist_ok=True)
            shutil.copyfile(filename,image_loc)

            global image
            image = ImageTk.PhotoImage(Image.open(image_loc))  
            updateitem_canvas.create_image(20, 20, anchor=tk.NW, image=image) 
            
        updateitem_browseimage_button = tk.Button(
            updateitem_window, text="Browse for Image..", borderwidth=4, command=get_image,
                              font=(utils.buttonfont, utils.stdfontsize))
        updateitem_browseimage_button.pack(pady=10)

        global updateitem_canvas
        updateitem_canvas = tk.Canvas(updateitem_window, width = 300, height = 300)  
        updateitem_canvas.pack(padx=10, pady=10)
        conn = db.create_connection(db.dbfile)
        if conn is not None:
            image_loc = db.get_image_for_item(conn, shopname, item_list.get(item_list.curselection()[0])[0])[0]
            global image3
            if image_loc:
                image3 = ImageTk.PhotoImage(Image.open(image_loc))  
                updateitem_canvas.create_image(20, 20, anchor=tk.NW, image=image3)
            else:
                image3 = ImageTk.PhotoImage(Image.open(utils.placeholder))  
                updateitem_canvas.create_image(20, 20, anchor=tk.NW, image=image3)
        else:
            print(utils.DATABASE_ERROR)

        updateitem_updateitem_button = tk.Button(
            updateitem_window, text="Edit Item", borderwidth=4, command=lambda: complete_updateitem(originalname, updateitem_itemname_entry.get(), updateitem_itemquantity_entry.get(), updateitem_window),
                              font=(utils.buttonfont, utils.stdfontsize))
        updateitem_updateitem_button.pack(pady=10)

    updateitem_button = tk.Button(
        button_frame, text="Edit Item", font=(utils.buttonfont, utils.stdfontsize), command=lambda: updateitem(item_list.get(item_list.curselection()[0])[0].strip(), item_list.get(item_list.curselection()[0])[1].strip()))
    updateitem_button.pack(pady=(0,10))

    def signout():
        # handle config
        utils.save_shop_config('','')
        window.destroy()

    signout_button = tk.Button(
        button_frame, text="Sign out", font=(utils.buttonfont, utils.stdfontsize), command=signout)
    signout_button.pack(pady=(50,10))

    def deleteallitems():
        WarningBox = tk.messagebox.askquestion ('Delete ALL Items','Are you sure you want to delete ALL Items? This acction cannot be undone!',icon = 'warning')
        if WarningBox == utils.YES:
            conn = db.create_connection(db.dbfile)
            if conn is not None:
                db.delete_all_items(conn, shopname)
                conn.close()
                update_item_list()
            else:
                print(utils.DATABASE_ERROR)

    deleteallitems_button = tk.Button(
        button_frame, text="DELETE ALL ITEMS", font=(utils.buttonfont, utils.stdfontsize), fg='red', command=deleteallitems)
    deleteallitems_button.pack(pady=10)

    def deleteaccount():
        WarningBox = tk.messagebox.askquestion ('Delete ACCOUNT','Are you sure you want to delete your ACCOUNT? This acction cannot be undone!',icon = 'warning')
        if WarningBox == utils.YES:
            conn = db.create_connection(db.dbfile)
            if conn is not None:
                db.delete_account(conn, shopname)
                conn.close()
                signout()
            else:
                print(utils.DATABASE_ERROR)

    deleteaccount_button = tk.Button(
        button_frame, text="DELETE ACCOUNT", font=(utils.buttonfont, utils.stdfontsize), fg='red', command=deleteaccount)
    deleteaccount_button.pack(pady=10)

    window.mainloop()


if __name__ == '__main__':
    print("[E] Execute the login program instead")
    
