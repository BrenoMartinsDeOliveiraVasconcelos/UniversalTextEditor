import json
import os

from lib.consoledb import consoledb, errorprint
from lib import tools
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pyperclip

pc = True


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


def about(mode="g"):
    cfg = tools.readconfig()
    if mode == "g":
        abt = tk.Tk()
        tools.windowmaker(abt, "About", bg="#ffffff")

        ix = -1

        for i in [f"Universal Text Editor",
                  "Made by Breno Martins",
                  "This software is distribuited under the GPLv2 license.",
                  f"Version: {cfg['version']}",
                  f"Build: {cfg['build']}",
                  f"Release: {cfg['releasebuild']}"]:
            ix += 1
            tk.Label(abt, bg="#ffffff", text=i, fg="#000000").grid(row=ix, column=0)

        tk.Button(abt, bg="#ffffff", command=abt.destroy,
                  text="Ok", width=10, fg="#000000") .grid(row=ix+1, column=0)

        abt.mainloop()
    elif mode == "c":
        print(f"""
Universal Text Editor v{cfg["version"]} ({cfg['build']})
Made by Breno Martins
This software is distribuited under the GPLv2 license

        """)
        input("Enter when done: ")


def documentation():
    print("""
Universal Text Editor - Command Line mode

:exit: - Exit the editor
:save: - Save the typed text
    :cancel: - Exit menu without saving
:delete: - Delete a line
    :cancel: - Exit the menu without deleting anything
    :last: - Delete the last line
    :first: - Delete the first line
    :all: - Delete all lines
:open: - Open a file and get its contents
    :cancel: - Cancel it.
:help: - This "menu"
:about: - About Universal Editor
:cp: Copy or paste a text
    :cancel: - Cancel it
:macro: - Replace a specific string by a text
    """)
    input("Enter when done: ")


def cp(tezto):
    if not cp:
        print("Library pyperclip is not avaliable, install it.")
        input()
        return tezto
    else:
        copyorpaste = input("[C]opy or [p]aste? ").lower()
        if copyorpaste in ["c", "p"]:
            if copyorpaste == "c":
                line = input("Copy line number: ")
                if line == ":all:":
                    pyperclip.copy('\n'.join(tezto))
                    return tezto
                elif line == ":cancel:":
                    return tezto
                else:
                    try:
                        pyperclip.copy((tezto[int(line)]))
                    except (ValueError, TypeError, IndexError):
                        return tezto
            elif copyorpaste == "p":
                pas = pyperclip.paste().split("\n")
                for i in pas:
                    tezto.append(i)

                return tezto
            elif copyorpaste == ":cancel:":
                return tezto

    return tezto


def macromaker(mode="g"):
    macros = f"{tools.scriptpath()}/macros/"
    if mode == "g":
        mk = tk.Tk()

        tools.windowmaker(root=mk, title="Macro maker", size="200x90")

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
    elif mode == "c":
        ce = input("[C]reate or [e]dit a macro? ")
        if ce.lower() == "c":
            name = input("Name: ")
            macrodict = {
                "shortcut": input("Shortcut: "),
                "text": input("Text: ")
            }
            open(f"{tools.scriptpath()}/macros/{name}.json", "w+").write(
                json.dumps(macrodict, indent=2))
        elif ce.lower() == "e":
            macrolist = os.listdir(macros)
            which = input("Macro name: ") + ".json"
            if which in macrolist:
                macrodict = json.load(open(f"{macros}/{which}"))
                for k in macrodict.keys():
                    macrodict[k] = input(f"{k.capitalize()}: ")

                    open(f"{macros}/{which}", "w+").write(json.dumps(macrodict,
                                                                     indent=2))

        elif ce == ":cancel:":
            pass


def replacetxt(text):
    consoledb("Replacetxt", "Bruh")

    rep = tk.Tk()
    tools.windowmaker(rep, "Replace", "175x75")

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
