import tkinter as tk
from lib import menus
from lib.consoledb import consoledb
from tkinter import messagebox
from sys import exit


def close(root: tk.Tk, text: tk.Text):
    confirma = messagebox.askyesnocancel("Exit", "Do you want to exit "
                                                 "without saving?")
    consoledb("Close", confirma)
    if confirma is False:
        menus.saveas(text, root)
        exit(0)
    elif confirma is True:
        exit(0)
    elif confirma is None:
        return
