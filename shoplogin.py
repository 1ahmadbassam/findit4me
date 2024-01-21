from dbhelper import DatabaseHelper as db
import tkinter as tk
import tkinter.ttk as ttk
import utils
import configparser
import ctypes
import shopmain

def complete_signup(shopname, password, location, phonenumber, window):
    conn = db.create_connection(db.dbfile)
    if conn is not None:
        if db.locate_shopname(conn, shopname) == 0:
            ctypes.windll.user32.MessageBoxW(
                0, "Shop already exists!", utils.SIGNUP_ERROR, 0)
            conn.close()
        else:
            if not shopname and not password and not phonenumber:
                ctypes.windll.user32.MessageBoxW(
                    0, "Entries can't be empty!", utils.SIGNUP_ERROR, 0)
            elif len(shopname) < 6:
                ctypes.windll.user32.MessageBoxW(
                    0, "Shop name is too short! It should at least be 6 characters!", utils.SIGNUP_ERROR, 0)
            elif len(password) < 8:
                ctypes.windll.user32.MessageBoxW(
                    0, "Password is too short! It should at least be 8 characters!", utils.SIGNUP_ERROR, 0)
            elif len(phonenumber) < 8 or not phonenumber.isalnum():
                ctypes.windll.user32.MessageBoxW(
                    0, "Phone number is not valid!", utils.SIGNUP_ERROR, 0)
            else:
                db.create_shops_table(conn)
                db.create_shop(conn, (str(shopname), str(password), str(location), str(phonenumber)))
                conn.close()

                # handle config
                utils.save_shop_config(shopname, password)
                window.destroy()
                shopmain.main(shopname, password)
    else:
        print(utils.DATABASE_ERROR)
        
def create_login_gui():
    window = tk.Tk()
    window.title(utils.appname)

    welcome_label = tk.Label(
        window, text="Welcome to " + utils.appname, font=(utils.titlefont, utils.hugefontsize, utils.bold))
    welcome_label.pack(padx=10, pady=(10, 0))
    welcome_label2 = tk.Label(
        window, text="Shop Manager", font=(utils.titlefont, 16))
    welcome_label2.pack(pady=(0, 20))

    shopname_frame = tk.Frame(window)
    shopname_frame.pack(fill=tk.X, padx=10)
    shopname_label = tk.Label(
        shopname_frame, text="Shop Name:", font=(utils.labelfont, utils.stdfontsize))
    shopname_label.pack(side=tk.LEFT, padx=(0, 4))
    shopname_entry = tk.Entry(shopname_frame, borderwidth=2, font=(utils.entryfont, utils.stdfontsize))
    shopname_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
    utils.create_entry_hint(shopname_entry, utils.shopname_hint)

    password_frame = tk.Frame(window)
    password_frame.pack(fill=tk.X, padx=10, pady=10)
    password_label = tk.Label(
        password_frame, text="Password:", font=(utils.labelfont, utils.stdfontsize))
    password_label.pack(side=tk.LEFT, padx=(0, 4))
    password_entry = tk.Entry(password_frame, show="*", borderwidth=2, font=(utils.entryfont, utils.stdfontsize))
    password_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
    utils.create_entry_hint(password_entry, utils.password_hint)

    def signin(shopname, password):
        conn = db.create_connection(db.dbfile)

        if conn is not None:
            if db.locate_shop(conn, shopname, password) == 0:
                # handle config
                utils.save_shop_config(shopname, password)
                window.destroy()
                shopmain.main(shopname, password)
            else:
                ctypes.windll.user32.MessageBoxW(
                    0, "Incorrect shopname or password.", "Error during sign-in", 0)
        else:
            print(utils.DATABASE_ERROR)

    signin_button = tk.Button(window, text="Sign in", borderwidth=4,
                              command=lambda: signin(shopname_entry.get(), password_entry.get()),
                              font=(utils.buttonfont, utils.stdfontsize))
    signin_button.pack(pady=10)

    # handle signup
    def signup(shopname, password):
        signup_window = tk.Toplevel()
        signup_window.title("Sign up your shop")
        utils.set_window_icon(signup_window)
        signup_title = tk.Label(
            signup_window, text="Ready to Share your Items?", font=(utils.titlefont, 26, utils.bold))
        signup_title.pack(padx=10, pady=10)

        signup_shopname_frame = tk.Frame(signup_window)
        signup_shopname_frame.pack(fill=tk.X, padx=10)
        signup_shopname_label = tk.Label(
            signup_shopname_frame, text="Shop Name:", font=(utils.labelfont, utils.stdfontsize))
        signup_shopname_label.pack(side=tk.LEFT, padx=(0, 4))
        signup_shopname_entry = tk.Entry(
            signup_shopname_frame, borderwidth=2, font=(utils.entryfont, utils.stdfontsize))
        signup_shopname_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
        signup_shopname_entry.delete(0, tk.END)
        signup_shopname_entry.insert(0, shopname)
        utils.create_entry_hint(signup_shopname_entry, utils.shopname_hint)
        
        signup_password_frame = tk.Frame(signup_window)
        signup_password_frame.pack(fill=tk.X, padx=10, pady=10)
        signup_password_label = tk.Label(
            signup_password_frame, text="Password:", font=(utils.labelfont, utils.stdfontsize))
        signup_password_label.pack(side=tk.LEFT, padx=(0, 4))
        signup_password_entry = tk.Entry(
            signup_password_frame, show="*", borderwidth=2, font=(utils.entryfont, utils.stdfontsize))
        signup_password_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
        signup_password_entry.delete(0, tk.END)
        signup_password_entry.insert(0, password)
        utils.create_entry_hint(signup_password_entry, utils.password_hint)

        signup_location_frame = tk.Frame(signup_window)
        signup_location_frame.pack(fill=tk.X, padx=10)
        signup_location_label = tk.Label(
            signup_location_frame, text="Location:", font=(utils.labelfont, utils.stdfontsize))
        signup_location_label.pack(side=tk.LEFT, padx=(0, 4))
        signup_location_combox = ttk.Combobox(
            signup_location_frame, state='readonly', font=(utils.entryfont, utils.stdfontsize))
        signup_location_combox['values'] = utils.locations
        signup_location_combox.current(0)
        signup_location_combox.pack(side=tk.RIGHT, expand=True, fill=tk.X)

        signup_phonenumber_frame = tk.Frame(signup_window)
        signup_phonenumber_frame.pack(fill=tk.X, padx=10)
        signup_phonenumber_label = tk.Label(
            signup_phonenumber_frame, text="Phone Number:", font=(utils.labelfont, utils.stdfontsize))
        signup_phonenumber_label.pack(side=tk.LEFT, padx=(0, 4))
        signup_phonenumber_entry = tk.Entry(
            signup_phonenumber_frame, borderwidth=2, font=(utils.entryfont, utils.stdfontsize))
        signup_phonenumber_entry.pack(
            side=tk.RIGHT, expand=True, fill=tk.X, pady=10)
        utils.create_entry_hint(signup_phonenumber_entry, utils.phonenumber_hint)

        

        signup_signup_button = tk.Button(
            signup_window, text="Sign me up!", borderwidth=4, command=lambda: complete_signup(signup_shopname_entry.get(), signup_password_entry.get(), signup_location_combox.get(), signup_phonenumber_entry.get(), window),
                              font=(utils.buttonfont, utils.stdfontsize))
        signup_signup_button.pack(pady=10)

    signup_button = tk.Button(window, text="Sign up your shop", borderwidth=4,
                              command=lambda: signup(shopname_entry.get(), password_entry.get()),
                              font=(utils.buttonfont, utils.stdfontsize))
    signup_button.pack(pady=(0, 10))

    window.mainloop()


config_shopname = None
config_password = None


def check_existing_user():
    config = configparser.ConfigParser()
    config.read(utils.config_file)

    if config.has_section(utils.config_section_name) and config.has_option(utils.config_section_name, utils.config_option_shopname) and config.has_option(utils.config_section_name, utils.config_option_password):
        global config_shopname
        global config_password
        config_shopname = config[utils.config_section_name][utils.config_option_shopname]
        config_password = config[utils.config_section_name][utils.config_option_password]


def main():
    check_existing_user()
    if config_shopname == None or config_password == None or not config_shopname or not config_password:
        create_login_gui()
    else:
        shopmain.main(config_shopname, config_password)


if __name__ == '__main__':
    main()
