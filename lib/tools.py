import os
import json
from lib.consoledb import consoledb
from lib import menus
import pyperclip
import tkinter as tk
from tkinter import messagebox

pc = True


def copypaste(mode, text):
    string = text.get("1.0", tk.END)

    if not pc:
        messagebox.showerror("Error", "Pyperclip is needed but not avaliable."
                                      "\nPlease install using python3 -m pip install pyperclip or the"
                                      " erquivalent in your system.")

        return

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


def macro(text, mode="g"):
    macrof = f"{scriptpath()}/macros"
    macros = os.listdir(macrof)

    if mode == "g":
        consoledb("Macro", macros)

        for i in macros:
            index = -1
            if i.endswith(".json"):
                minfo = json.load(open(f"{macrof}/{i}"))
                txt = text.get("1.0", tk.END).split(" ")
                consoledb("Macro", ' '.join(txt).replace("\n", "+"))
                for loop in txt:
                    index += 1
                    loop = loop.strip("\n")
                    if loop == minfo["shortcut"] or loop == minfo["shortcut"] + "\n":
                        txt[index] = minfo["text"]
                        consoledb("Macro", txt[index])
                    txt[index] = txt[index].strip("\n")
                consoledb("Macro", txt[index])
                text.delete("1.0", tk.END)
                text.insert("1.0", " ".join(txt))
    elif mode == "c":
        txt = []
        index = -1
        for i in text:
            line = i.split(" ")
            for n in line:
                index += 1
                for d in macros:
                    if d.endswith(".json"):
                        minfo = json.load(open(f"{macrof}/{d}"))
                        if n == minfo["shortcut"] or n == minfo["shortcut"] + "\n":
                            line[index] = minfo["text"]
            txt.append(" ".join(line))
            index = -1

        return txt


def readconfig():
    path = scriptpath() + "/config.json"

    with open(path) as json_file:
        data = json.load(json_file)
        return data


def opt(option, text, root):
    consoledb("Opt", option)
    if option == 9:
        yn = messagebox.askyesno("Exit", "Do you really want to exit? Unsaved changes may be "
                                         "lost forever!")
        if yn == 1:
            exit()
    elif option == 8:
        consoledb("Opt", "About")
        menus.about()
    elif option == 7:
        menus.replacetxt(text)
    elif option == 6:
        text.delete("1.0", tk.END)
    elif option == 5:
        macro(text)
    elif option == 4:
        copypaste("p", text)
    elif option == 3:
        copypaste("c", text)
    elif option == 2:
        menus.macromaker()
    elif option == 1:
        menus.saveas(text, root=root)
    elif option == 0:
        menus.opn(text, root)


def configmenu(menu, text, root):
    opts = ["Open", "Save as", "Create a Macro"]

    emenu = tk.Menu(root)
    menu.add_cascade(label="Edit", menu=emenu)
    i = 0
    for i in range(len(opts)):
        emenu.add_command(label=opts[i],
                          command=lambda x=i: opt(x, text, root))

    spopt = ["Copy", "Paste", "Macro", "Clear", "Replace", "About", "Exit"]
    for o in range(len(spopt)):
        i += 1
        menu.add_command(label=spopt[o],
                         command=lambda x=i: opt(x, text, root))


def clear(sys):
    if sys == "Windows":
        os.system("cls")
    elif sys == "Linux":
        os.system("export TERM=xterm && clear")
    else:
        os.system("clear")


def createmacro(entries):
    args = []
    path = scriptpath() + "/macros"
    for i in entries:
        consoledb("Createmacro", i.get())
        args.append(str(i.get()))

    macrodict = {
        "shortcut": args[0],
        "text": args[1]
    }
    open(f"{path}/{args[2]}.json",
         "w+").write(json.dumps(macrodict, indent=2))

    messagebox.showinfo("Done", f"Created {args[2]}")
