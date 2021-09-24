import json
from lib import scriptinfo


def loadui():
    dark = scriptinfo.readconfig()["dark"]
    if not dark:
        file = "colorscheme"
    else:
        file = "darkcolors"

    return json.load(open(scriptinfo.scriptpath()+f"/stuffs/{file}.json"))
