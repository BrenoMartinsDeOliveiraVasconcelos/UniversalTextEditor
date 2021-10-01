import tkinter as tk
from lib import utils, colorscheme

ui = colorscheme.loadui()
mainui = ui["main"]
textui = mainui["text"]


def notemanager(path: str, nots: list):
    nm = tk.Tk()
    utils.windowmaker(nm, "Note Manager")

    for i in nots:
        text = tk.Text(nm, bg=textui["bg"], fg=textui["fg"],
                       font=("Segoe", 10), wrap="word", undo=True,
                       width=20, height=10, insertbackground=textui["ibg"],
                       selectbackground=textui["sbg"])
        text.grid(row=1, column=0, rowspan=1, columnspan=1)

    nm.mainloop()
