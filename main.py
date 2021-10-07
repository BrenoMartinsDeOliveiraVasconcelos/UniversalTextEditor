from lib import utils, menus, colorscheme, scriptinfo, events
from lib.consoledb import consoledb
from sys import argv
import platform
import tkinter as tk
import sys

scriptpath = scriptinfo.scriptpath()
argv.append('')
systema = platform.system()
configs = scriptinfo.readconfig()
ui = colorscheme.loadui()
mainui = ui["main"]
menui = mainui["menu"]
textui = mainui["text"]
scrollbarui = mainui["scrollbar"]
labelui = mainui["label"]


def main(args):
    if args[1] == "-macromaker":
        menus.macromaker()
        sys.exit()
    elif args[1] == "-secret":
        menus.secretmenu()

    root = tk.Tk()
    root.title(f"Universal Text Editor v{configs['version']}")
    root.resizable(True, True)
    root["bg"] = mainui["bg"]  # "#d6d6d6"
    if systema == "Windows":
        root.iconbitmap(f"{scriptpath}/stuffs/ute.ico")

    # Menu
    menu = tk.Menu(root, bg=menui["bg"], fg=menui["fg"],
                   activebackground=menui["abg"], activeforeground=menui["afg"],
                   disabledforeground=menui["dfg"], relief="flat", border=0)

    root.config(menu=menu)

    # Text
    text = tk.Text(root, bg=textui["bg"], fg=textui["fg"],
                   font=("Calibri", 12), wrap="word", undo=True,
                   insertbackground=textui["ibg"], selectbackground=textui["sbg"])
    text.pack(fill="both", expand=True, side=tk.LEFT)

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
    try:
        main(argv)
        consoledb("Global/main.py", "Fechada inesperada!")
    except KeyboardInterrupt:
        consoledb("Global/main.py", "Abortado.", tp=3)
