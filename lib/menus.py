import os
from lib import utils, events, colorscheme, scriptinfo
from lib.consoledb import consoledb
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

ui = colorscheme.loadui()
menui = ui["menus"]
labelui = menui["label"]
buttonui = menui["button"]
enui = menui["entry"]
textui = menui["text"]
scrollbarui = menui["scrollbar"]
opui = menui["optionmenu"]


def saveas(text, root=None):
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
            break

    text.delete("1.0", tk.END)
    text.insert("1.0", txt)
    root.title(f"Universal Text Editor - {fn}")


def about():
    cfg = scriptinfo.readconfig()
    abt = tk.Tk()
    utils.windowmaker(abt, "About")
    ix = 0

    for i in [f"Universal Text Editor v{cfg['version']} {cfg['build']}",
              "Made by Breno Martins",
              "This software is distribuited under the GPLv2 license."]:
        ix += 1
        tk.Label(abt, bg=labelui["bg"], text=i, fg=labelui["fg"]).grid(
            row=ix, column=0
        )

    tk.Button(abt, bg=buttonui["bg"], command=abt.destroy,
              text="Ok", width=10, fg=buttonui["fg"]).grid(row=ix + 1, column=0)

    abt.mainloop()


def macromaker():
    mk = tk.Tk()

    utils.windowmaker(root=mk, title="Macro maker")

    indx = -1
    labels = ["Name: ", "Shortcut: ", "Text: "]
    for i in labels:
        indx += 1
        tk.Label(mk, text=i, bg=labelui["bg"], fg=labelui["fg"]).grid(row=indx,
                                                                      column=0, sticky="nw")

    nentry = tk.Entry(mk, bg=enui["bg"], fg=enui["fg"], width=20,
                      font=("Segoe", 10))
    shentry = tk.Entry(mk, bg=enui["bg"], fg=enui["fg"], width=20,
                       font=("Segoe", 10))
    tentry = tk.Text(mk, bg=textui["bg"], fg=textui["fg"], font=("Segoe", 10),
                     width=20, height=5, insertbackground=textui["ibg"], selectbackground=textui["sbg"])

    scrollbar = tk.Scrollbar(mk, command=tentry.yview,
                             bg=scrollbarui["bg"], activebackground=scrollbarui["abg"],
                             activerelief="flat")
    scrollbar.grid(row=2, column=2, sticky="nsew")
    tentry.config(yscrollcommand=scrollbar.set)

    nentry.grid(row=0, column=1, sticky="e")
    shentry.grid(row=1, column=1, sticky="e")
    tentry.grid(row=2, column=1, sticky="e")

    tk.Button(mk, text="Create",
              command=lambda: utils.createmacro([shentry, nentry], tentry),
              bg=buttonui["bg"], fg=buttonui["fg"], width=10,
              font=("Segoe", 10)).grid(row=3, column=1, sticky="e")

    mk.mainloop()


def replacetxt(text):
    consoledb("Replacetxt", "Bruh")

    rep = tk.Tk()
    utils.windowmaker(rep, "Replace")

    labels = ["Target: ", "Result: "]
    index = -1
    for i in labels:
        index += 1
        tk.Label(rep, text=i, font=("Segoe", "10"),
                 bg=labelui["bg"], fg=labelui["fg"]).grid(row=index, column=0,
                                                          sticky="w")

        tentry = tk.Entry(rep, bg=enui["bg"], fg=enui["fg"])
        rentry = tk.Entry(rep, bg=enui["bg"], fg=enui["fg"])

        tentry.grid(row=0, column=1)
        rentry.grid(row=1, column=1)

        tk.Button(rep, text="Replace", bg=buttonui["bg"], fg=buttonui["fg"],
                  command=lambda: utils.subs(text, [tentry, rentry]),
                  width=10).grid(
            row=2, column=1, sticky="e")

    rep.resizable(False, False)

    rep.mainloop()


def editmacro():
    path = scriptinfo.scriptpath() + "/macros"
    macros = os.listdir(path)
    names = []

    for i in macros:
        if i.endswith(".json"):
            names.append(i.replace(".json", ""))

    medit = tk.Tk()
    utils.windowmaker(medit, "Macro editor")

    var = tk.StringVar(medit)
    var.set(names[0])

    tk.Label(medit, text="Macro: ", bg=labelui["bg"], fg=labelui["fg"]
             ).grid(row=0, column=0, sticky="w")
    optmenu = tk.OptionMenu(medit, var, *names)
    optmenu.config(bg=opui)

    optmenu["menu"].config(bg=opui)

    optmenu.grid(row=0, column=1, sticky="e")

    tk.Button(medit, text="Edit", bg=buttonui["bg"], fg=buttonui["fg"],
              command=lambda: utils.madit(medit, var),
              width=10).grid(row=1, column=1, sticky="e")

    medit.mainloop()


def secretmenu():
    # Essa função contém uma tela que é feito apenas para testes
    # de futuras novas features
    # essa função só poderá ser ativada com argumentos específicos

    secret = tk.Tk()

    utils.windowmaker(secret, "MENU SECRETO")
    consoledb("Shhh", "SEGREDO", tp=1, verifydebug=False)

    secret.bind("<Control-c>", events.q)

    secret.mainloop()
