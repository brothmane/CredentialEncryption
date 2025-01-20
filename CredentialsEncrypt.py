import os
import datetime
import tkinter as tk
from tkinter import ttk, messagebox, StringVar
from tkinter.filedialog import askopenfilename, asksaveasfile
from tkinter.font import nametofont
import shutil
from pathlib import Path
from control import SessionVar, AccountControl
from cryptography.fernet import Fernet

my_db = Path("file.db")
my_archive = "archive" 
if not os.path.exists(my_archive):
    os.makedirs(my_archive)
    os.system(f'attrib +h "{my_archive}"')

time_now = datetime.datetime.now()

if my_db.is_file():
    shutil.copy2(my_db, f"archive/file-{time_now.strftime("%d%m%Y")}.db")

def init_check_key():
    account = AccountControl()
    if not len(account.getall()):
        return True
    elif account.decrypt(keyVar.get()):
        return True
    else:
        return False


def create_db():
    accountctl = AccountControl()
    if accountctl.create_db():
        messagebox.showinfo("info", "Data Base create successfully")
        btn_create_db["state"] = "disabled"
        sessionvar.db_created = True
    else: 
        messagebox.showwarning("warnning", "Data Base not created")

def cleartbl():
    for i in table.get_children():
        table.delete(i)

def refrechtbl():
    cleartbl()
    for i, account in enumerate(accounts):
        table.insert("", index=tk.END, values=(account["id"], account["user"], account["site"], account["password"]), tags=f"t{account['id']}")
        if i % 2:
            table.tag_configure(f"t{account['id']}", font=("ARIAL", 12), background="#b386fc")
        else:
            table.tag_configure(f"t{account['id']}", font=("ARIAL", 12), background="#8d85f2")
        table.column("user", anchor="center")
        table.column("site", anchor="center")
        table.column("password", anchor="center")

    style = ttk.Style(frm)
    style.theme_use("clam")
    style.configure("Treeview", fieldbackground="#b386fc")
    style.configure("Treeview.heading", background="#8d85f2")
    nametofont("TkHeadingFont").configure(size=10, family="ARIAL", weight="bold")

def add():
    if sessionvar.db_created:
        if keyVar.get():
            if init_check_key():
                if userVar.get() and sitVar.get() and passwordVar.get():
                    accountctl = AccountControl()
                    accountctl.set(userVar.get(), sitVar.get(), passwordVar.get(), keyVar.get())
                        
                    if accountctl.add():
                        messagebox.showinfo("info", "Account added succefully")
                        user_idVar.set(0)
                        userVar.set("")
                        sitVar.set("")
                        passwordVar.set("")
                        if sessionvar.tbl_dycript_state:
                            decrypt()
                        else:
                            encrypt()
                    else:
                        messagebox.showerror("Error", "Traitement error")
                else:
                    messagebox.showwarning("Warnning", "Missing data")
            else:
                messagebox.showwarning("Warnning", "Possibly used a wrong key")
        else:
            messagebox.showwarning("Warnning", "Check key entry")
    else:
        messagebox.showwarning("Warnning", "Create data base first")

def update(id):
    if sessionvar.db_created:
        if keyVar.get():
            if init_check_key():
                if userVar.get() and sitVar.get() and passwordVar.get():
                    accountctl = AccountControl()
                    accountctl.set(userVar.get(), sitVar.get(), passwordVar.get(), keyVar.get())

                    messagebox.showinfo("info", accountctl.edit(id, encrypt=True)["msg"])
                    user_idVar.set(0)
                    userVar.set("")
                    sitVar.set("")
                    passwordVar.set("")
                    if sessionvar.tbl_dycript_state:
                        decrypt()
                    else:
                        encrypt()
                else:
                    messagebox.showwarning("Warnning", "Missing data")
            else:
                messagebox.showwarning("Warnning", "Possibly used a wrong key")
        else:
            messagebox.showwarning("Warnning", "Check key entry")
    else:
        messagebox.showwarning("Warnning", "Create data base first")

def delete(id):
    if sessionvar.db_created:
        if keyVar.get():
            accountctl = AccountControl()
            if int(id):
                messagebox.showinfo("info", accountctl.remove(id)["msg"])
                user_idVar.set(0)
                userVar.set("")
                sitVar.set("")
                passwordVar.set("")
                if sessionvar.tbl_dycript_state:
                    decrypt()
                else:
                    encrypt()
            else:
                messagebox.showwarning("Warnning", "No selected item")
        else:
            messagebox.showwarning("Warnning", "Check key entry")
    else:
        messagebox.showwarning("Warnning", "Create data base first")

def generate_key():
    if messagebox.askquestion("Info", "Please if use this key please keep it in secured place.") == "yes":
        keyVar.set(Fernet.generate_key().decode())
    
def save_key():
    if keyVar.get():
        file_name = asksaveasfile()
        if file_name:
            file_name.write(keyVar.get())
            file_name.close()
               
    else:
        messagebox.showwarning("Warnning", "Check key field empty")

def openfile():
    file = None
    try:
        file_name = askopenfilename()
        if file_name:
            file = open(file_name)
            key = file.read()
            if len(key) < 50:
                keyVar.set(key)
            else:
                messagebox.showwarning("Warnning", "Very large file")
            file.close()
    except:
        messagebox.showwarning("Warnning", "Check file")
        if file:
            file.close()

def encrypt():
    account = AccountControl()
    try:
        global accounts
        accounts = account.getall()
        refrechtbl()
        sessionvar.tbl_dycript_state = False
    except:
        messagebox.showwarning("Warnning", "Check key")

def decrypt():
    account = AccountControl()
    try:
        global accounts
        accounts = account.decrypt(keyVar.get())
        refrechtbl()
        sessionvar.tbl_dycript_state = True
    except:
        messagebox.showwarning("Warnning", "Check key")

def selectItem(event):
    if sessionvar.tbl_dycript_state:
        selectedrow = table.focus()
        item = table.item(selectedrow)
        if item:
            if item["values"]:
                user_idVar.set(item["values"][0])
                userVar.set(item["values"][1])
                sitVar.set(item["values"][2])
                passwordVar.set(item["values"][3])
    

def search_site(event):
    if sessionvar.db_created:
        if sessionvar.tbl_dycript_state:
            account = AccountControl()
            global accounts
            accounts.clear()
            pre_accounts = account.decrypt(keyVar.get())
            for pre_account in pre_accounts:
                if search_siteVar.get().casefold() in pre_account["site"].casefold():
                    accounts.append(pre_account)
            refrechtbl()

    else:
        messagebox.showwarning("Warnning", "Create data base first")


sessionvar = SessionVar()
pre_accounts = AccountControl()
accounts = pre_accounts.getall()

root = tk.Tk()
root.title("Credentials Encryption")

user_idVar = StringVar()
user_idVar.set(0)
userVar = StringVar()
sitVar = StringVar()
passwordVar = StringVar()
keyVar = StringVar()
search_siteVar = StringVar()

frm = ttk.Frame(root, padding=10, width=800, height=700)
frm.pack(fill='both')

lbl_set_inf = ttk.Label(frm)
lbl_set_inf.grid(row=0, column=0)

ttk.Label(lbl_set_inf, text="User").grid(row=0, column=0, padx=10, sticky="w")
ttk.Entry(lbl_set_inf, width=50, textvariable=userVar).grid(row=0, column=1, columnspan=3, padx=10, pady=5)

ttk.Label(lbl_set_inf, text="Key").grid(row=0, column=4, padx=10, sticky="w")
ttk.Entry(lbl_set_inf, width=50, textvariable=keyVar, state="disabled").grid(row=0, column=5, columnspan=2, padx=10, pady=5)

ttk.Button(lbl_set_inf, text="Generate Key", command=generate_key).grid(row=0, column=7, padx=5)
ttk.Button(lbl_set_inf, text="Get Key", command=openfile).grid(row=1, column=5, padx=5)
ttk.Button(lbl_set_inf, text="Save Key", command=save_key).grid(row=1, column=6, padx=5)

ttk.Label(lbl_set_inf, text="Site").grid(row=1, column=0, padx=10, sticky="w")
ttk.Entry(lbl_set_inf, width=50, textvariable=sitVar).grid(row=1, column=1, columnspan=3, padx=10, pady=5)

ttk.Label(lbl_set_inf, text="Password").grid(row=2, column=0, padx=10, sticky="w")
ttk.Entry(lbl_set_inf, width=50, textvariable=passwordVar).grid(row=2, column=1, columnspan=3, padx=10, pady=5)

ttk.Button(lbl_set_inf, text="Add", command=add).grid(row=3, column=1, padx=10, pady=10)
ttk.Button(lbl_set_inf, text="Update", command=lambda: update(user_idVar.get())).grid(row=3, column=2, padx=10, pady=10)
ttk.Button(lbl_set_inf, text="Delete", command=lambda: delete(user_idVar.get())).grid(row=3, column=3, padx=10, pady=10)

lbl_search = ttk.Label(frm)
lbl_search.grid(row=2, column=0, pady=10)

ttk.Label(lbl_search, text="Search a site").grid(row=0, column=0, padx=10)
search_entry = ttk.Entry(lbl_search, width=50, textvariable=search_siteVar)
search_entry.grid(row=0, column=1, padx=5)

search_entry.bind('<KeyRelease>', search_site)



table = ttk.Treeview(frm, columns=("id", "user", "site", "password"), show="headings", height=25)
table.heading("id", text="ID")
table.heading("user", text="Username")
table.heading("site", text="Site")
table.heading("password", text="Password")
table.column("id", width=10)
table.column("user", width=300)
table.column("site", width=400)
table.column("password", width=300)

table["displaycolumns"]=("user", "site", "password")

refrechtbl()

table.grid(row=3, column=0)

table.bind('<<TreeviewSelect>>', selectItem)

lbl_btn = ttk.Label(frm)
lbl_btn.grid(row=4, column=0, pady=10)

ttk.Button(lbl_btn, text="Decrypt", command=decrypt).grid(row=0, column=0, padx=5)
ttk.Button(lbl_btn, text="Encrypt", command=encrypt).grid(row=0, column=1, padx=5)
btn_create_db = ttk.Button(lbl_btn, text="Create DB", state=sessionvar.db_btn_state, command=create_db)
btn_create_db.grid(row=0, column=2, padx=5)

frm.grid_rowconfigure(0, weight=1)
frm.grid_columnconfigure(0, weight=1)


root.mainloop()
