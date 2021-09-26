import platform
from instlib import helpers
from lib.consoledb import consoledb
from lib.utils import windowmaker
import tkinter as tk
import getpass

user = getpass.getuser()
so = platform.system()
consoledb("Global/fastinstall.py", f"{so}, {user}")


def install():
    inst = tk.Tk()
    windowmaker(inst, "Install", bg="#ffffff")

    tk.Label(inst, font=("TKDefault", 10), bg="#ffffff",
             text="""Please read before continuing""").grid(row=0, column=0,
                                                            sticky="nsew", columnspan=2)
    text = tk.Text(inst)
    text.insert("1.0", ''.join(open("./__Installer__/tos.txt", "r").readlines()))
    text.grid(row=1, column=0, columnspan=2)
    tk.Button(inst, text="Agree and install", width=20,
              command=lambda: helpers.installation(so, user, inst)).grid(row=2,
                                                                         column=0, sticky="w")
    tk.Button(inst, text="Exit", width=20, command=inst.destroy).grid(row=2,
                                                                      column=1, sticky="e")

    inst.mainloop()


if __name__ == '__main__':
    install()
