#!/bin/sh

apt install python3-pip
apt install python3-tk

python3 -m pip install -r ./requeriments.txt
sh ./__Installer__/scripts/pyinstaller.sh
