from lib import tools, menus
from lib.consoledb import consoledb
from sys import argv
from sys import version
import platform
import tkinter as tk

scriptpath = tools.scriptpath()
argv.append('')
systema = platform.system()
configs = tools.readconfig()


def main(args):
    guimode = False

    if args[1] == "-c":
        print("Loading command line...")
    elif args[1] == "-g":
        consoledb("Main", "Iniciando GUI...")
        guimode = True
    elif args[1] == "-macromaker":
        menus.macromaker()
        exit()
    else:
        print("It was not specified if you want to run on Command Line or GUI, "
              "please select: ")
        opt = ""
        while opt not in ["c", "g"]:
            # opt = input("[c]ommand or [g]ui: ").lower()
            opt = "g"

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
        root["bg"] = "#d6d6d6"

        # Menu
        menu = tk.Menu(root, bg="#ffffff", fg="#000000",
                       activebackground="#e0e0e0", activeforeground="#000000",
                       disabledforeground="#a1a1a1", relief="flat", border=0)

        root.config(menu=menu)

        # Text
        text = tk.Text(root, bg="#ffffff", fg="#000000",
                       font=("Segoe", 10), wrap="word", undo=True,
                       insertbackground="#000000", selectbackground="#e0e0e0",
                       selectforeground="#000000",
                       width=95, height=35)
        text.grid(row=1, column=0, rowspan=1)

        # Scrollbar
        scrollbar = tk.Scrollbar(root, command=text.yview,
                                 bg="#ffffff", activebackground="#e0e0e0",
                                 activerelief="flat")
        scrollbar.grid(row=1, column=1, sticky="nsew")
        text.config(yscrollcommand=scrollbar.set)

        # Label
        ver = version.split("\n")[0]
        ver = "".join(ver).split(" ")[0]
        if configs["debug"]:
            string = f"DEBUG - v{configs['version']} {configs['releasebuild']} {configs['build']} - " \
                     f"OS: {platform.system()} - Python: {ver}"
        else:
            string = f"v{configs['version']}"
        tk.Label(root, bg="#d6d6d6", text=string, fg="#000000").grid(
                row=2, column=0, sticky="w", columnspan=1, rowspan=1)

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
                              ":help:", ":about:", ":cp:", ":macro:", ":macromaker:"]:
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
                elif tinput == ":macro:":
                    text = tools.macro(text, "c")
                elif tinput == ":macromaker:":
                    menus.macromaker("c")
                line = 0
                tools.clear(systema)
                for line in range(len(text)):
                    line += 1
                    print(f"[{line}] {text[line - 1]}", end=endl)


if __name__ == "__main__":
    try:
        main(argv)
        consoledb("Global/main.py", "Fechada inesperada!")
    except KeyboardInterrupt:
        consoledb("Global/main.py", "Abortado.", tp=3)
