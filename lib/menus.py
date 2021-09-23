import os

from lib.consoledb import consoledb, errorprint
from lib import tools
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


def saveas(text, root=None, mode="g"):
    if mode == "g":
        text = text.get("1.0", tk.END)
        consoledb("SaveAs", text)

        fn = filedialog.asksaveasfilename()
        consoledb("SaveAs", fn)

        try:
            open(fn, "w+").write(text.strip('\n'))
            root.title(f"Universal Text Editor - {fn}")
        except PermissionError:
            consoledb("SaveAs", "Permissão negada!", tp=1)
            messagebox.showerror("Error", "Permission denied!")
        except OSError:
            messagebox.showerror("Error", "Invalid argument")
    elif mode == "c":
        while True:
            try:
                fn = input("Path: ")
                if fn != ":cancel:":
                    open(fn, "w+").write(text.strip('\n'))
                    break
                else:
                    break
            except PermissionError:
                errorprint("Permission denied or it is a directory!", tp=1)
            except FileNotFoundError:
                errorprint("FIle not found", tp=0)
            except IsADirectoryError:
                errorprint("It is a directory", tp=0)
            except OSError:
                errorprint("Permission denied?", tp=1)


def opn(text, root):
    fn = filedialog.askopenfilename()
    consoledb("Opn", fn)

    index = -1
    while True:
        index += 1
        codecs = ["utf-8", "latin1", "utf8", "iso-88691-1",
                  "mac_cyrilic", "mac_greek", "mac_iceland",
                  "mac_latin2", "mac_roman", "mac_turkish"]
        try:
            txt = ''.join(open(fn, "r", encoding=codecs[index]).readlines())
            break
        except UnicodeError:
            consoledb("Opn", codecs[index])
        except PermissionError:
            messagebox.showerror("Error", "Permission denied")

    text.delete("1.0", tk.END)
    text.insert("1.0", txt)
    root.title(f"Universal Text Editor - {fn}")


def delete(text):
    while True:
        index = input("Line number: ")
        if index == ":last:":
            index = -1
            break
        elif index == ":first:":
            index = 0
            break
        elif index == ":cancel:":
            index = None
            break
        elif index == ':all:':
            index = None
            text = []
            break
        else:
            try:
                index = int(index) - 1
                break
            except (ValueError, TypeError):
                errorprint("Invalid value!", tp=1)

    try:
        text.pop(index)
    except IndexError:
        print("\033[31mNo such line.\033[0m")
    except TypeError:
        pass

    return text


def cmdopn():
    while True:
        fn = input("Path: ")
        try:
            if fn != ":cancel:":
                return open(fn, "r").readlines()
            else:
                break
        except PermissionError:
            errorprint("Permission denied!", tp=1)
        except IsADirectoryError:
            errorprint("It is a directory!", tp=0)
        except FileNotFoundError:
            errorprint("File not found", tp=0)


def about():
    cfg = tools.readconfig()
    abt = tk.Tk()
    tools.windowmaker(abt, "About", bg="#ffffff")

    ix = -1

    for i in [f"Universal Text Editor v{cfg['version']}",
              "Made by Breno Martins",
              "This software is distribuited under the GPLv2 license."]:
        ix += 1
        tk.Label(abt, bg="#ffffff", text=i, fg="#000000").grid(row=ix, column=0)

    tk.Button(abt, bg="#ffffff", command=abt.destroy,
              text="Ok", width=10, fg="#000000").grid(row=ix + 1, column=0)

    abt.mainloop()


def macromaker():
    mk = tk.Tk()

    tools.windowmaker(root=mk, title="Macro maker")

    indx = -1
    labels = ["Name", "Shortcut", "Text"]
    for i in labels:
        indx += 1
        tk.Label(mk, text=i, bg="#ffffff", fg="#000000").grid(row=indx,
                                                              column=0, sticky="w")

    nentry = tk.Entry(mk, bg="#ffffff", fg="#000000")
    shentry = tk.Entry(mk, bg="#ffffff", fg="#000000")
    tentry = tk.Entry(mk, bg="#ffffff", fg="#000000")

    nentry.grid(row=0, column=1)
    shentry.grid(row=1, column=1)
    tentry.grid(row=2, column=1)

    tk.Button(mk, text="Create",
              command=lambda: tools.createmacro([shentry, tentry, nentry]),
              bg="#ffffff", fg="#000000", width=10,
              font=("Segoe", 10)).grid(row=3, column=1)

    mk.mainloop()


def replacetxt(text):
    consoledb("Replacetxt", "Bruh")

    rep = tk.Tk()
    tools.windowmaker(rep, "Replace")

    labels = ["Target", "Result"]
    index = -1
    for i in labels:
        index += 1
        tk.Label(rep, text=i, font=("Segoe", "10"),
                 bg="#ffffff", fg="#000000").grid(row=index, column=0,
                                                  sticky="w")

        tentry = tk.Entry(rep, bg="#ffffff", fg="#000000")
        rentry = tk.Entry(rep, bg="#ffffff", fg="#000000")

        tentry.grid(row=0, column=1)
        rentry.grid(row=1, column=1)

        tk.Button(rep, text="Replace", font=("Segoe", 10), bg="#ffffff",
                  fg="#000000", command=lambda: tools.subs(text,
                                                           [tentry, rentry]),
                  width=10).grid(
            row=2, column=1)

    rep.resizable(False, False)

    rep.mainloop()


def editmacro():
    path = tools.scriptpath() + "/macros"
    macros = os.listdir(path)
    names = []

    for i in macros:
        if i.endswith(".json"):
            names.append(i.replace(".json", ""))

    medit = tk.Tk()
    tools.windowmaker(medit, "Macro editor")

    var = tk.StringVar(medit)
    var.set(names[0])

    tk.Label(medit, text="Macro: ", bg="#ffffff",
             fg="#000000").grid(row=0, column=0, sticky="w")
    optmenu = tk.OptionMenu(medit, var, *names)

    optmenu.grid(row=0, column=1)

    tk.Button(medit, text="Edit", bg="#ffffff", fg="#000000",
              command=lambda: tools.madit(medit, var),
              width=10).grid(row=1, column=1)

    medit.mainloop()


def secretmenu():
    # Essa função contém uma tela que é feito apenas para testes
    # de futuras novas features
    # essa função só poderá ser ativada com argumentos específicos

    secret = tk.Tk()

    tools.windowmaker(secret, "MENU SECRETO")
    consoledb("Shhh", "SEGREDO", tp=1, verifydebug=False)

    secret.mainloop()
