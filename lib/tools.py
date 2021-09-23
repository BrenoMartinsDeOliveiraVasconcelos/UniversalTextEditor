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


def macro(text):
    macrof = f"{scriptpath()}/macros"
    macros = os.listdir(macrof)

    consoledb("Macro", macros)

    for n in macros:
        index = -1
        if n.endswith(".json"):
            minfo = json.load(open(f"{macrof}/{n}"))
            txt = text.get("1.0", tk.END).split(" ")
            for k in txt:
                index += 1
                if "\n" in k:
                    a = k.split("\n")
                    txt[index] = a[0] + "\n"
                    txt.insert(index + 1, a[1])
                    if a[1] == "":
                        del txt[index + 1]
                        txt[index] = a[0] + "\n"
            index = -1
            consoledb("Macro", ' '.join(txt).replace("\n", "+"))
            for loop in txt:
                index += 1
                if loop.replace("\n", "") == minfo["shortcut"]:
                    if "\n" not in loop:
                        txt[index] = minfo["text"]
                    else:
                        txt[index] = minfo["text"] + "\n"
                    consoledb("Macro", txt[index])
            consoledb("Macro", txt[index])
            text.delete("1.0", tk.END)

            text.insert("1.0", " ".join(txt))


def readconfig():
    path = scriptpath() + "/config.json"

    with open(path) as json_file:
        data = json.load(json_file)
        return data


def opt(option, text, root):
    consoledb("Opt", option)
    if option == 10:
        yn = messagebox.askyesno("Exit",
                                 "Do you really want to exit? Unsaved changes may be "
                                 "lost forever!")
        if yn == 1:
            exit()
    elif option == 9:
        consoledb("Opt", "About")
        menus.about()
    elif option == 8:
        menus.replacetxt(text)
    elif option == 7:
        text.delete("1.0", tk.END)
    elif option == 6:
        macro(text)
    elif option == 5:
        menus.editmacro()
    elif option == 4:
        menus.macromaker()
    elif option == 3:
        copypaste("p", text)
    elif option == 2:
        copypaste("c", text)
    elif option == 1:
        menus.saveas(text, root=root)
    elif option == 0:
        menus.opn(text, root)


def configmenu(menu, text, root):
    opts = ["Open", "Save as", "Copy", "Paste"]
    mopts = ["Create a Macro", "Edit a Macro", "Macronize"]
    spopt = ["Clear", "Replace"]
    topts = ["About", "Exit"]

    emenu = tk.Menu(root)
    tmenu = tk.Menu(root)
    mmenu = tk.Menu(root)
    pmenu = tk.Menu(root)
    menu.add_cascade(label="File", menu=emenu)
    i = 0
    for i in range(len(opts)):
        emenu.add_command(label=opts[i],
                          command=lambda x=i: opt(x, text, root))

    menu.add_cascade(label="Macro", menu=mmenu)
    for e in range(len(mopts)):
        consoledb("Configuremenu", e)
        i += 1
        mmenu.add_cascade(label=mopts[e],
                          command=lambda x=i: opt(x, text, root))

    menu.add_cascade(label="Text", menu=tmenu)
    for o in range(len(spopt)):
        i += 1
        tmenu.add_command(label=spopt[o],
                          command=lambda x=i: opt(x, text, root))

    menu.add_cascade(label="Help", menu=pmenu)
    for u in range(len(topts)):
        i += 1
        pmenu.add_command(label=topts[u],
                          command=lambda x=i: opt(x, text, root))


def clear(sys):
    if sys == "Windows":
        os.system("cls")
    elif sys == "Linux":
        os.system("export TERM=xterm && clear")
    else:
        os.system("clear")


def createmacro(entries, text):
    args = []
    path = scriptpath() + "/macros"
    for i in entries:
        consoledb("Createmacro", i.get())
        args.append(str(i.get()))

    args.append(text.get("1.0", tk.END))
    consoledb("Createmacro", args)

    macrodict = {
        "shortcut": args[0],
        "text": args[2].strip("\n")
    }

    if macrodict["shortcut"] == "" or macrodict["text"] == "" \
            or args[1] == "":
        messagebox.showerror("Error", "Some entries are empty!")
        return

    open(f"{path}/{args[1]}.json",
         "w+").write(json.dumps(macrodict, indent=2))

    messagebox.showinfo("Done", f"Created {args[1]}")


def windowmaker(root, title, size="", bg="#ffffff", resizable=(False, False)):
    root.title(title)
    if size != "":
        root.geometry(size)
    root["bg"] = bg
    root.resizable(resizable[0], resizable[1])


def subs(text, entries):
    string = text.get("1.0", tk.END).split(" ")
    index = -1
    for i in string:
        index += 1
        if "\n" in i:
            a = i.split("\n")
            string[index] = a[0] + "\n"
            string.insert(index + 1, a[1])

    wrep = entries[0].get()
    repwith = entries[1].get()
    if wrep == "" or repwith == "":
        messagebox.showerror("Error", "Some entries are empty!")
        return

    index = -1
    occour = 0
    for i in string:
        index += 1
        if i.replace("\n", "") == wrep:
            occour += 1
            consoledb("Subs", f"{string[index]}")
            if "\n" not in i:
                string[index] = repwith
            else:
                string[index] = repwith + "\n"

    text.delete("1.0", tk.END)
    text.insert("1.0", " ".join(string))
    messagebox.showinfo("Done", f"Replaced {occour} occourence(s) of {wrep}.")


def editmacro(entry, text, value):
    path = scriptpath() + "/macros"
    madict = json.load(open(f"{path}/{value}.json"))
    vedit = [entry.get(), text.get("1.0", tk.END)]
    madict["shortcut"] = vedit[0]
    madict["text"] = vedit[1]

    consoledb("Editmacro", madict)
    open(f"{path}/{value}.json", "w+").write(json.dumps(madict, indent=2))

    messagebox.showinfo("Done", "Done")


def madit(root, var):
    value = var.get()
    path = scriptpath() + "/macros"
    minfo = json.load(open(f"{path}/{value}.json"))
    defaultvals = [
        minfo["shortcut"], minfo["text"]
    ]

    index = 1
    labels = ["Shortcut: ", "Text: "]
    for i in labels:
        index += 1
        tk.Label(root, text=i, bg="#ffffff", fg="#000000").grid(row=index,
                                                                column=0, sticky="nw")

    sentry = tk.Entry(root, width=20, font=("Segoe", 10))
    nentry = tk.Text(root, height=5, width=20, font=("Segoe", 10))

    sentry.grid(row=2, column=1)
    nentry.grid(row=3, column=1)

    scrollbar = tk.Scrollbar(root, command=nentry.yview,
                             bg="#ffffff", activebackground="#e0e0e0",
                             activerelief="flat")
    scrollbar.grid(row=3, column=2, sticky="nsew")
    nentry.config(yscrollcommand=scrollbar.set)

    sentry.insert(0, defaultvals[0])
    nentry.insert("1.0", defaultvals[1])

    tk.Button(root, text="Ok", width=10,
              command=lambda: editmacro(sentry, nentry, value)
              ).grid(row=4, column=1, sticky="e")
