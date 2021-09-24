import os

def scriptpath():
    script = os.path.dirname(os.path.realpath(__file__))
    return '/'.join(script.replace("\\", "/").split("/")[:-1])