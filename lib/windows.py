import tkinter as tk
from lib import utils, colorscheme

ui = colorscheme.loadui()
mainui = ui["main"]
textui = mainui["text"]


def notemanager(path: str, nots: list):
    nm = tk.Tk()
    utils.windowmaker(nm, "Note Manager")
    row = 0
    column = -1

    for i in nots:
        column += 1
        if column % 10 == 0:
            row += 1
            column = 0

        text = tk.Text(nm, bg=textui["bg"], fg=textui["fg"],
                       font=("Segoe", 10), wrap="word", undo=True,
                       width=20, height=10, insertbackground=textui["ibg"],
                       selectbackground=textui["sbg"])
        text.grid(row=row, column=column, rowspan=1, columnspan=1)
        text.insert("1.0", "".join(open(f"{path}/{i}", "r")))

    nm.mainloop()
