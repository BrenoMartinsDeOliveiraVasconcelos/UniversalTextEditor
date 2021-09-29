from lib import utils, menus, colorscheme, scriptinfo
from lib.consoledb import consoledb
from sys import argv
from sys import version
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
    root.title("Universal Text Editor")
    # Por algum motivo, eu tenho que alterar o geometry de acordo com
    # o sistema...
    if systema == "Linux":
        root.geometry("782x630")
    else:
        root.geometry("686x595")
    root.resizable(False, False)
    root["bg"] = mainui["bg"]  # "#d6d6d6"

    # Menu
    menu = tk.Menu(root, bg=menui["bg"], fg=menui["fg"],
                   activebackground=menui["abg"], activeforeground=menui["afg"],
                   disabledforeground=menui["dfg"], relief="flat", border=0)

    root.config(menu=menu)

    # Text
    text = tk.Text(root, bg=textui["bg"], fg=textui["fg"],
                   font=("TkDefaultFont", 10), wrap="word", undo=True,
                   width=95, height=35, insertbackground=textui["ibg"], selectbackground=textui["sbg"])
    text.grid(row=1, column=0, rowspan=1)

    # Scrollbar
    scrollbar = tk.Scrollbar(root, command=text.yview,
                             bg=scrollbarui["bg"], activebackground=scrollbarui["abg"],
                             activerelief="flat")
    scrollbar.grid(row=1, column=1, sticky="nsew")
    text.config(yscrollcommand=scrollbar.set)

    # Label
    ver = version.split("\n")[0]
    ver = "".join(ver).split(" ")[0]
    if configs["debug"]:
        string = f"DEBUG - v{configs['version']} " \
                 f"{configs['build']}, Dt: {configs['dark']}, " \
                 f"OS: {platform.system()}, Python: {ver}"
    else:
        string = f"v{configs['version']}"

    tk.Label(root, bg=labelui["bg"], text=string, fg=labelui["fg"]).grid(
            row=2, column=0, sticky="w", columnspan=1, rowspan=1)

    utils.configmenu(menu, text, root)

    root.mainloop()


if __name__ == "__main__":
    try:
        main(argv)
        consoledb("Global/main.py", "Fechada inesperada!")
    except KeyboardInterrupt:
        consoledb("Global/main.py", "Abortado.", tp=3)
