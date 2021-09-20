import os
import json
from lib.consoledb import consoledb
from lib import menus
try:
    import pyperclip
    pc = True
except (ImportError, ModuleNotFoundError):
    pyperclip = None
    pc = False
    consoledb("Global/tools.py", "Pyperclip was requested but it was not found.",
              tp=1, verifydebug=False)
try:
    import tkinter as tk
    from tkinter import messagebox
except (ImportError, ModuleNotFoundError):
    messagebox = None
    consoledb("Global/tools.py", "Install tkinter in your system to use GUI!",
              tp=2)


def copypaste(mode, text):
    string = text.get("1.0", tk.END)

    if mode == "c":
        pyperclip.copy(string)
        messagebox.showinfo("Ok", "Copied")
    elif mode == "p":
        consoledb("Copypaste", pyperclip.paste())
        if "\n" in pyperclip.paste():
            string = pyperclip.paste().split("\n")
            string = '\n'.join((string[:-1]))
            consoledb("Copypaste", f"{string}")
        else:
            string = pyperclip.paste()
            consoledb("Copypaste", "Ok")
        text.insert("-1.0", string)


def scriptpath():
    script = os.path.dirname(os.path.realpath(__file__))
    return '/'.join(script.replace("\\", "/").split("/")[:-1])


def readconfig():
    path = scriptpath() + "/config.json"

    with open(path) as json_file:
        data = json.load(json_file)
        return data


def opt(option, text, root):
    consoledb("Opt", option)
    if option == 6:
        yn = messagebox.askyesno("Exit", "Do you really want to exit? Unsaved changes may be "
                                         "lost forever!")
        if yn == 1:
            exit()
    elif option == 5:
        consoledb("Opt", "About")
        menus.about()
    elif option == 4:
        text.delete("1.0", tk.END)
    elif option == 3:
        copypaste("p", text)
    elif option == 2:
        copypaste("c", text)
    elif option == 1:
        menus.saveas(text, root=root)
    elif option == 0:
        menus.opn(text, root)


def configmenu(menu, text, root):
    opts = ["Open", "Save as",  "Copy",  "Paste", "Clear", "About", "Exit"]

    for i in range(len(opts)):
        menu.add_command(label=opts[i],
                         command=lambda x=i: opt(x, text, root))


def clear(sys):
    if sys == "Windows":
        os.system("cls")
    elif sys == "Linux":
        os.system("export TERM=xterm && clear")
    else:
        os.system("clear")
