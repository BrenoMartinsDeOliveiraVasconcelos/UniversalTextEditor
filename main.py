from lib import utils, menus, colorscheme, runtime, events
from sys import argv
import platform
import tkinter as tk
from tkinter import messagebox
import sys

scriptpath = runtime.scriptpath()
argv.append('')
systema = platform.system()
configs = runtime.readconfig()
ui = colorscheme.loadui()
mainui = ui["main"]
menui = mainui["menu"]
textui = mainui["text"]
scrollbarui = mainui["scrollbar"]
labelui = mainui["label"]

defaulttext = ""


def main(args):
    global defaulttext

    root = tk.Tk()
    root.title("UTE_INIT")

    if args[1] == "-macromaker":
        menus.macromaker()
        sys.exit()
    elif args[1] == "-secret":
        menus.secretmenu()
    else:
        if args[1].startswith("-file="):
            args[1] = args[1].replace("-file=", "")
            try:
                defaulttext = open(''.join(args[1:])).read()
                open(f"{scriptpath}/stuffs/saveas.txt", "w").write(''.join(args[1:]))
            except FileNotFoundError:
                messagebox.showerror("Error", f"File {''.join(args[1:])} not found!\n"
                                              f"Check if the file exists and if there is no spaces and try again.")
            except IsADirectoryError:
                messagebox.showerror("Error", f"Specified file is a directory!")
            except PermissionError:
                messagebox.showerror("Error", "Permission Denied!")

    root.title(f"Universal Text Editor v{configs['version']} "
               f"{configs['build'] if configs['build'] != 'release' else ''}")

    if defaulttext != "":
        root.title(f"Universal Text Editor - {''.join(args[1:])}")

    root.resizable(True, True)
    root["bg"] = mainui["bg"]
    if systema == "Windows":
        root.iconbitmap(f"{scriptpath}/stuffs/ute.ico")

    # Menu
    menu = tk.Menu(root, bg=menui["bg"], fg=menui["fg"],
                   activebackground=menui["abg"], activeforeground=menui["afg"],
                   disabledforeground=menui["dfg"], relief="flat", border=0)

    root.config(menu=menu)

    # Text
    labelstring = f"v{configs['version']}"
    if configs['debug']:
        labelstring += \
            f" {configs['build']} - OS: {platform.system()} {platform.release()}, " \
            f"Kernel: {platform.version()}, Python: {platform.python_version()}"

    tframe = tk.Frame(root)
    text = tk.Text(tframe, bg=textui["bg"], fg=textui["fg"],
                   font=(configs['font'], configs['fontsize']), wrap="word", undo=True)
    text.insert("1.0", defaulttext)
    text.pack(fill="both", expand=True)
    tk.Label(tframe, text=labelstring, bg=mainui["bg"],
             font=("Calibri", 10)).pack(side=tk.LEFT,
                                        expand=True, fill="x")
    tframe.pack(fill="both", expand=True, side=tk.LEFT)

    # Scrollbar
    frame = tk.Frame(root)
    frame.pack(side=tk.TOP, expand=True, fill="both")
    scrollbar = tk.Scrollbar(frame, command=text.yview,
                             bg=scrollbarui["bg"], activebackground=scrollbarui["abg"],
                             activerelief="flat")
    scrollbar.pack(fill="both", expand=True)
    text.config(yscrollcommand=scrollbar.set)

    utils.configmenu(menu, text, root)
    root.protocol("WM_DELETE_WINDOW", lambda: events.close(root, text))

    root.mainloop()


if __name__ == "__main__":
    main(argv)
