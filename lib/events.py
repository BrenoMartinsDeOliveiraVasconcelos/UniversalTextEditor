from lib.consoledb import consoledb
import tkinter as tk
from lib import menus
from tkinter import  messagebox


def close(root: tk.Tk, text: tk.Text):
    confirma = messagebox.askyesnocancel("Exit", "Do you want to save "
                                                 "before exiting?")
    if confirma is True:
        menus.saveas(text, root)
        exit(0)
    elif confirma is False:
        exit(0)
    elif confirma is None:
        return
