from lib import util


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

    config = util.readconfig()

    if config["debug"] or not verifydebug:
        print(f"{info} {symb} {text}")

    if tp == 3:
        exit(3)
