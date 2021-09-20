from lib.consoledb import consoledb, errorprint
from lib import tools
try:
    import tkinter as tk
    from tkinter import filedialog
    from tkinter import messagebox
except (ImportError, ModuleNotFoundError):
    tk = None
    filedialog = None
    messagebox = None
    consoledb(
        "Global/menus.py", "Please install Tkinter in your operating system!",
        tp=2)
try:
    import pyperclip
except (ImportError, ModuleNotFoundError):
    pyperclip = None
    consoledb("Global/menus.py", "Pyperclip requested but not found", tp=1)


def saveas(text, root=None, mode="g"):
    if mode == "g":
        text = text.get("1.0", tk.END)
        consoledb("SaveAs", text)

        fn = filedialog.asksaveasfilename()
        consoledb("SaveAs", fn)

        try:
            open(fn, "w+").write(text)
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
                    open(fn, "w+").write(text)
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
        abt.title("About Universal Text Editor")

        abt.resizable(False, False)
        abt["bg"] = "#ffffff"

        ix = -1

        for i in [f"Universal Text Editor v{cfg['version']}",
                  "Made by Breno Martins",
                  "This software is distribuited under the GPLv2 license."]:
            ix += 1
            tk.Label(abt, bg="#ffffff", text=i, fg="#000000").grid(row=ix, column=0)

        tk.Button(abt, bg="#ffffff", command=abt.destroy,
                  text="Ok", width=10, fg="#000000") .grid(row=ix+1, column=0)

        abt.mainloop()
    elif mode == "c":
        print(f"""
Universal Text Editor v{cfg["version"]}
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

    """)
    input("Enter when done: ")
