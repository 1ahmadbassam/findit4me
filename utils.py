import tkinter as tk
import configparser

locations = ["Beirut", "Saida", "Jbeil"]
config_section_name = 'shop'
config_option_shopname = 'shopname'
config_option_password = 'password'
config_file = 'settings.ini'
appname = "FindIt4me"
appicon = 'outline_shopping_cart_black_36dp.png'
searchicon='search_icon2.png'
placeholder = 'NoImageAvailable.png'

SIGNUP_ERROR = "Error during signup"
ADDITEM_ERROR = "Error during adding item"
EDITITEM_ERROR = "Error during adding item"
DATABASE_ERROR = "[E] Database error."

titlefont = "Trebuchet MS"
labelfont = "Sticka"
entryfont = "Consolas"
buttonfont = "Tahoma"
hintfont = "Microsoft Sans Serif"
hintfontsize = 10
stdfontsize = 14
largefontsize = 20
hugefontsize= 30
bold="bold"
italic="italic"
YES="yes"

shopname="Shop Name"
itemname="Item Name"
itemquantity="Item Quantity"

shopname_hint="My Shop"
password_hint="12345678"
phonenumber_hint="0015555555555"
itemname_hint="My Valuable Item"
itemquantity_hint="4"

class MultiListbox(tk.Frame):
    def __init__(self, master, lists):
        tk.Frame.__init__(self, master)
        self.lists = []
        #print(lists)
        for l,w in lists:
            frame = tk.Frame(self)
            frame.pack(side='left', expand='yes', fill='both')
            tk.Label(frame, text=l, borderwidth=1, relief='raised').pack(fill='x')
            lb = tk.Listbox(frame, width=w, borderwidth=0, selectborderwidth=0,
                         relief='flat', exportselection=False, height=16)
            lb.pack(expand='yes', fill='both')
            self.lists.append(lb)
            #lb.bind('<B1-Motion>', self._select)
            lb.bind('<<ListboxSelect>>', self._select)
            #lb.bind('<Leave>', lambda e: 'break')
            lb.bind('<MouseWheel>', lambda e, s=self: s._scroll_mouse(e))
            #lb.bind('<Button-2>', lambda e, s=self: s._button2(e.x, e.y))
        frame = tk.Frame(self)
        frame.pack(side='left', fill='y')
        tk.Label(frame, borderwidth=1, relief='raised').pack(fill='x')
        sb = tk.Scrollbar(frame, orient='vertical', command=self._scroll)
        sb.pack(expand='yes', fill='y')
        self.lists[0]['yscrollcommand']=sb.set

    def _select(self, event):
##        print('on _select({})'.format(event.type))
        w = event.widget
        curselection = w.curselection()

        if curselection:
            self.event_generate('<<MultiListboxSelect>>', when='tail')
            self.selection_clear(0, self.size())
            self.selection_set(curselection[0])

    def _button2(self, x, y):
        for l in self.lists:
            l.scan_mark(x, y)
        return 'break'

    def _b2motion(self, x, y):
        for l in self.lists: l.scan_dragto(x, y)
        return 'break'

    def _scroll(self, *args):
        for l in self.lists:
            l.yview(*args)
        return 'break'

    def _scroll_mouse(self, event):
        for l in self.lists:
            l.yview_scroll(int(-1*(event.delta/120)), 'units')
        return 'break'

    def curselection(self):
        return self.lists[0].curselection()

    def delete(self, first, last=None):
        for l in self.lists:
            l.delete(first, last)

    def get(self, first, last=None):
        result = []
        for l in self.lists:
            result.append(l.get(first,last))
        if last: return apply(map, [None] + result)
        return result

    def index(self, index):
        self.lists[0].index(index)

    def insert(self, index, *elements):
        for e in elements:
            for i, l in enumerate(self.lists):
                l.insert(index, e[i])

    def size(self):
        return self.lists[0].size()

    def see(self, index):
        for l in self.lists:
            l.see(index)

    def selection_anchor(self, index):
        for l in self.lists:
            l.selection_anchor(index)

    def selection_clear(self, first, last=None):
        for l in self.lists:
            l.selection_clear(first, last)

    def selection_includes(self, index):
        return self.lists[0].selection_includes(index)

    def selection_set(self, first, last=None):
        for l in self.lists:
            l.selection_set(first, last)
            
def create_entry_hint(entry, hint, fontsize=stdfontsize):
    if not entry.get():
        entry.insert(0, hint)
        entry.configure(font=(entryfont, fontsize, italic))
    def entry_focus(event):
        if entry.get() == hint:
            entry.delete('0', tk.END)
            entry.configure(font=(entryfont, fontsize))
    entry.bind("<FocusIn>", entry_focus)
    def entry_unfocus(text):
        if not text:
            entry.insert(0, hint)
            entry.configure(font=(entryfont, fontsize, italic))
    entry.bind("<FocusOut>", lambda args: entry_unfocus(entry.get()))

def set_window_icon(window):
    window.tk.call('wm', 'iconphoto', window._w,
                   tk.PhotoImage(file=appicon))
w='w'
def save_shop_config(shopname, password):
    config = configparser.ConfigParser()
    config[config_section_name] = {}
    config[config_section_name][config_option_shopname] = str(
        shopname)
    config[config_section_name][config_option_password] = str(
        password)
    with open(config_file, w) as configfile:
        config.write(configfile)
