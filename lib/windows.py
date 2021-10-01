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
        fileinfo = open(f"{path}/{i}", "r").readlines()[0].split(";")
        column += 1
        if column % 10 == 0:
            row += 1
            column = 0

        text = tk.Text(nm, bg=fileinfo[0], fg=fileinfo[1],
                       font=("Segoe", 10), wrap="word", undo=True,
                       width=20, height=10, insertbackground=textui["ibg"],
                       selectbackground=textui["sbg"])
        text.grid(row=row, column=column, rowspan=1, columnspan=1)
        index = 0
        while True:
            codecs = ["latin1", "utf-8", "utf8", "iso-88691-1",
                      "mac_cyrilic", "mac_greek", "mac_iceland",
                      "mac_latin2", "mac_roman", "mac_turkish"]
            index += 1
            try:
                file = "".join(open(f"{path}/{i}", "r",
                                    encoding=codecs[index]).readlines()[1:])
                print(file)
                text.insert("1.0", file)
                break
            except UnicodeError:
                pass
        text.config(state=tk.DISABLED)

    nm.mainloop()
