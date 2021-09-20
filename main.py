from lib import tools, menus
from lib.consoledb import consoledb
from sys import argv
import platform
from random import choice
try:
    import tkinter as tk
    import tkinter.messagebox as msg
except (ImportError, ModuleNotFoundError):
    tk = None
    argv.append("-c")
    consoledb("Global", "ImportError: tkinter not found.", verifydebug=False,
              tp=2)
    consoledb("Global", "Verify how to install it in your OS.", verifydebug=False,
              tp=2)
    input()

scriptpath = tools.scriptpath()
argv.append('')
systema = platform.system()
configs = tools.readconfig()
if configs["wholesome"]:
    txtfile = "cool.txt"
else:
    txtfile = "rude.txt"
frases = open(f"{scriptpath}/{txtfile}", "r").readlines()


def main(args):
    guimode = False

    if args[1] == "-c":
        print("Loading command line...")
    elif args[1] == "-g":
        consoledb("Main", "Iniciando GUI...")
        guimode = True
    else:
        print("It was not specified if you want to run on Command Line or GUI, "
              "please select: ")
        opt = ""
        while opt not in ["c", "g"]:
            opt = input("[c]ommand or [g]ui: ").lower()

        if opt == "g":
            guimode = True
            consoledb("Main", "GUI")
        else:
            consoledb("Main", "CL")

    if guimode:
        root = tk.Tk()
        root.title("Universal Text Editor")
        # Por algum motivo, eu tenho que alterar o geometry de acordo com
        # o sistema...
        if systema == "Linux":
            root.geometry("782x630")
        else:
            root.geometry("686x595")
        root.resizable(False, False)
        root["bg"] = "#cccccc"

        # Menu
        menu = tk.Menu(root, bg="#ffffff", fg="#000000",
                       activebackground="#5156db", activeforeground="#ffffff",
                       disabledforeground="#a1a1a1", relief="flat", border=0)

        root.config(menu=menu)

        # Text
        text = tk.Text(root, bg="#ffffff", fg="#000000",
                       font=("Segoe", 10), wrap="word", undo=True,
                       insertbackground="#000000", selectbackground="#5156db",
                       width=95, height=35)
        text.grid(row=1, column=0, rowspan=1)

        # Scrollbar
        scrollbar = tk.Scrollbar(root, command=text.yview,
                                 bg="#ffffff", activebackground="#5156db",
                                 activerelief="flat")
        scrollbar.grid(row=1, column=1, sticky="nsew")
        text.config(yscrollcommand=scrollbar.set)

        # Label
        phr = tk.Label(root, bg="#cccccc", font=("Segoe", 10),
                       text=f"{choice(frases)}", fg="#000000")
        phr.grid(row=2, column=0, sticky="n")

        tools.configmenu(menu, text, root)

        root.mainloop()
    else:
        text = []
        line = 0
        tools.clear(systema)
        endl = "\n"
        while True:
            line += 1
            tinput = input(f"[{line}] ")
            if tinput not in [":exit:", ":save:", ":delete:", ":open:",
                              ":help:", ":about:", ":cp:"]:
                text.append(tinput)
            else:
                if tinput == ":exit:":
                    exit()
                elif tinput == ":save:":
                    menus.saveas('\n'.join(text), mode="c")
                elif tinput == ":delete:":
                    text = menus.delete(text)
                elif tinput == ":open:":
                    text = menus.cmdopn()
                    endl = ""
                elif tinput == ":help:":
                    menus.documentation()
                elif tinput == ":about:":
                    menus.about(mode="c")
                elif tinput == ":cp:":
                    text = menus.cp(text)
                line = 0
                tools.clear(systema)
                for line in range(len(text)):
                    line += 1
                    print(f"[{line}] {text[line-1]}", end=endl)


if __name__ == "__main__":
    try:
        main(argv)
        consoledb("Global/main.py", "Fechada inesperada")
    except KeyboardInterrupt:
        consoledb("Global/main.py", "Abortado.", tp=3)
