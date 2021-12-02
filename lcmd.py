import os
import shutil


def main():
    content = open("./main.py", "r").readlines()
    content.insert(0, "#!/usr/bin/env python3\n")
    open("utelinux.py", "w+").writelines(content)

    for i in os.listdir("./"):
        if os.path.isdir(f"./{i}"):
            shutil.copytree(f"./{i}", f"/usr/bin/{i}")


if __name__ == '__main__':
    main()