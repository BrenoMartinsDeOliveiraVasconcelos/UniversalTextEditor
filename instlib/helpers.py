from tkinter import messagebox
from lib.utils import windowmaker
import tkinter as tk
import os


def runscript(so, user, pman=""):
    if so == "Linux":
        if user != "root":
            messagebox.showerror("No permission", "Need sudo!")
            exit()

        os.system(f"sh ./__Installer__/scripts/{pman}.sh")
        messagebox.showinfo("Done", "Run 'main'.")
    elif so == "Windows":
        messagebox.showinfo("Windows", "Windows")

    exit()


def installation(so, user):
    messagebox.showinfo("Installation", "This may take a while!")

    if so == "Linux":
        installing = tk.Tk()

        packageman = ["apt", "pacman"]
        windowmaker(installing, "Select your package manager.", bg="#ffffff")

        var = tk.StringVar(installing, packageman[0])
        tk.Label(installing, text="Select your package manager: ", bg="#ffffff").grid(row=0, column=0, sticky="w")
        tk.OptionMenu(installing, var, *packageman).grid(row=0, column=1, sticky="w")
        tk.Button(installing, text="Ok", width=10, height=1,
                  command=lambda: runscript(so, user, var.get())).grid(row=1, column=0, columnspan=2)

        installing.mainloop()
    elif so == "Windows":
        runscript(so, user)
