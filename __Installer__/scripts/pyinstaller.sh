#!/bin/sh

python3 -m PyInstaller ./main.py
mv ./dist/main/* ./
