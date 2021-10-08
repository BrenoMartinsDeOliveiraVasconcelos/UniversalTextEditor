import json
from lib import runtime


def loadui():
    dark = runtime.readconfig()["dark"]
    if not dark:
        file = "colorscheme"
    else:
        file = "darkcolors"

    return json.load(open(runtime.scriptpath() + f"/stuffs/{file}.json"))
