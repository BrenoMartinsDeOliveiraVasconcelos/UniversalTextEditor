import os
import json


def scriptpath():
    script = os.path.dirname(os.path.realpath(__file__))
    return '/'.join(script.replace("\\", "/").split("/")[:-1])


def readconfig():
    path = scriptpath() + "/stuffs/config.json"

    with open(path) as json_file:
        data = json.load(json_file)
        return data
