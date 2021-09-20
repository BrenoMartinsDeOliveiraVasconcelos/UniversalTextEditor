from lib import tools


def consoledb(info, text, tp=0, verifydebug=True):
    if tp == 0:
        symb = "=>"
    elif tp == 1:
        symb = "<!>"
    elif tp == 2:
        symb = "[!]"
    elif tp == 3:
        symb = "(!)"
        verifydebug = False
    else:
        symb = "?"

    config = tools.readconfig()

    if config["debug"] or not verifydebug:
        print(f"{info} {symb} {text}")

    if tp == 3:
        exit(3)


def errorprint(text, tp):
    if tp == 0:
        symb = "<!>"
    elif tp == 1:
        symb = "[!]"
    else:
        symb = "\033[0m"

    print(f"{symb} {text}")
