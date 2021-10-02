import os
import json
from lib.consoledb import consoledb
from lib import menus, scriptinfo, colorscheme
import pyperclip
import tkinter as tk
from tkinter import messagebox
import sys

pc = True
ui = colorscheme.loadui()
menui = ui["menus"]
ibg = menui["bg"]
labelui = menui["label"]
buttonui = menui["button"]
enui = menui["entry"]
textui = menui["text"]
scrollbarui = menui["scrollbar"]


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


def macro(text):
    macrof = f"{scriptinfo.scriptpath()}/macros"
    macros = os.listdir(macrof)

    consoledb("Macro", macros)

    mnum = 0
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
                    mnum += 1
                    if "\n" not in loop:
                        txt[index] = minfo["text"]
                    else:
                        txt[index] = minfo["text"] + "\n"
                    consoledb("Macro", txt[index])
            consoledb("Macro", txt[index - 1])
            text.delete("1.0", tk.END)

            text.insert("1.0", " ".join(txt))

    txt = text.get("1.0", tk.END)
    stxt = txt.split("\n")
    for i in range(len(stxt)):
        if i > 0:
            stxt[i] = stxt[i][1:] if stxt[0] == " " else stxt[i][0:]

    text.delete("1.0", tk.END)
    text.insert("1.0", "\n".join(stxt))
    messagebox.showinfo("Done", f"Applied {mnum} macro calls.")


def opt(option, text, root):
    consoledb("Opt", option)
    if option == 11:
        yn = messagebox.askyesnocancel("Do you want save?", "Do you want to "
                                                            "exit without saving?")
        consoledb("Opt", yn)
        if yn is True:
            sys.exit()
        elif yn is False:
            menus.saveas(text, root=root)
            sys.exit()
        elif yn is None:
            consoledb("Opt", "Cancelado")
    elif option == 10:
        consoledb("Opt", "About")
        menus.about()
    elif option == 9:
        copypaste("p", text)
    elif option == 8:
        copypaste("c", text)
    elif option == 7:
        menus.replacetxt(text)
    elif option == 6:
        text.delete("1.0", tk.END)
    elif option == 5:
        macro(text)
    elif option == 4:
        menus.editmacro()
    elif option == 3:
        menus.macromaker()
    elif option == 2:
        menus.savenote(text)
    elif option == 1:
        menus.saveas(text, root=root)
    elif option == 0:
        menus.opn(text, root)


def configmenu(menu, text, root):
    opts = ["Open", "Save as text", "Save as note"]
    mopts = ["Create a Macro", "Edit a Macro", "Apply macros"]
    spopt = ["Clear", "Replace", "Copy", "Paste"]
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
        mmenu.add_command(label=mopts[e],
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


def clear(sistema):
    if sistema == "Windows":
        os.system("cls")
    elif sistema == "Linux":
        os.system("export TERM=xterm && clear")
    else:
        os.system("clear")


def createmacro(entries, text):
    args = []
    path = scriptinfo.scriptpath() + "/stuffs]macros"
    for i in entries:
        consoledb("Createmacro", i.get())
        args.append(str(i.get()))

    args.append(text.get("1.0", tk.END))
    if " " in args[0]:
        messagebox.showerror("Error", "Shorcuts cannot cointain spaces!")
        return

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
         "w+").write(json.dumps(macrodict, indent=4))

    messagebox.showinfo("Done", f"Created {args[1]}")


def windowmaker(root, title, size="", bg=ibg, resizable=(False, False)):
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
    elif " " in wrep or " " in repwith:
        messagebox.showerror("Error", "For now, you can only replace words!")
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

    txt = text.get("1.0", tk.END)
    stxt = txt.split("\n")
    for i in range(len(stxt)):
        if i > 0:
            stxt[i] = stxt[i][1:] if stxt[0] == " " else stxt[i][0:]

    text.delete("1.0", tk.END)
    text.insert("1.0", "\n".join(stxt))
    messagebox.showinfo("Done", f"Replaced {occour} occourence(s) of {wrep}.")


def editmacro(entry, text, value):
    path = scriptinfo.scriptpath() + "/stuffs/macros"
    madict = json.load(open(f"{path}/{value}.json"))
    vedit = [entry.get(), text.get("1.0", tk.END)]
    madict["shortcut"] = vedit[0]
    madict["text"] = vedit[1]

    if " " in madict["shortcut"]:
        messagebox.showerror("Error", "Shortcuts cannot cointain spaces!")
        return

    consoledb("Editmacro", madict)
    open(f"{path}/{value}.json", "w+").write(json.dumps(madict, indent=2))

    messagebox.showinfo("Done", "Done")


def madit(root, var):
    value = var.get()
    path = scriptinfo.scriptpath() + "/stuffs/macros"
    minfo = json.load(open(f"{path}/{value}.json"))
    defaultvals = [
        minfo["shortcut"], minfo["text"]
    ]

    index = 1
    labels = ["Shortcut: ", "Text: "]
    for i in labels:
        index += 1
        tk.Label(root, text=i, bg=labelui["bg"], fg=labelui["fg"]).grid(row=index,
                                                                        column=0, sticky="nw")

    sentry = tk.Entry(root, width=20, font=("Segoe", 10),
                      bg=enui["bg"], fg=enui["fg"])
    nentry = tk.Text(root, height=5, width=20, font=("Segoe", 10),
                     bg=textui["bg"], fg=textui["fg"], insertbackground=textui["ibg"], selectbackground=textui["sbg"])

    sentry.grid(row=2, column=1)
    nentry.grid(row=3, column=1)

    scrollbar = tk.Scrollbar(root, command=nentry.yview,
                             bg=scrollbarui["bg"], activebackground=scrollbarui["abg"],
                             activerelief="flat")
    scrollbar.grid(row=3, column=2, sticky="nsew")
    nentry.config(yscrollcommand=scrollbar.set)

    sentry.insert(0, defaultvals[0])
    nentry.insert("1.0", defaultvals[1])

    tk.Button(root, text="Ok", width=10,
              command=lambda: editmacro(sentry, nentry, value),
              bg=buttonui["bg"], fg=buttonui["fg"]).grid(row=4, column=1,
                                                         sticky="e")
