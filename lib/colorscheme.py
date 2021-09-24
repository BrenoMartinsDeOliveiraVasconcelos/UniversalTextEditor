import json
from lib import scriptinfo


def loadui():
    return json.load(open(scriptinfo.scriptpath()+"/stuffs/colorscheme.json"))
