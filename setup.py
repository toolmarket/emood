#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from cx_Freeze import setup, Executable

# python setup.py build

# Dependencies are automatically detected, but it might need fine tuning.

#build_exe_options = {}





# GUI applications require a different base on Windows (the default is for a
# console application).


if sys.platform == "win32":
    base = "Win32GUI" # hides the console
    build_exe_options = {
        "packages": 
    ["os","tkinter","sys","winerror","uuid","subprocess","importlib",
    "configparser","threading","pathlib","dbm","shelve","zipfile","io","json","requests",
    "certifi","chardet","idna","pystray","six","urllib3","multiprocessing","image",
    "win32event","win32api"], 
        "excludes": ["django","scipy","numpy","PyQt5","llvmlite","notebook","babel","matplotlib","mkl","jupyter"],
        "include_files": ["config.py","gui.py","fun.py","src","config.ini"],
        'build_exe': './/build/EmoodWin/'
    }

    build_exe_options = {
        "packages": 
    ["os","tkinter","sys","uuid","subprocess","importlib",
    "configparser","threading","pathlib","dbm","shelve","zipfile","io","json","multiprocessing"], 
        "excludes": ["django","scipy","numpy","PyQt5","llvmlite","notebook","babel","matplotlib","mkl","jupyter"],
        "include_files": ["config.py","gui.py","fun.py","src","vendor","config.ini"],
        'build_exe': './/build/EmoodWin3/',
        "optimize": 2
    }

else:
    build_exe_options = {
        "packages": 
    ["os","tkinter","sys","uuid","subprocess","importlib",
    "configparser","threading","pathlib","dbm","shelve","zipfile","io","json","requests",
    "certifi","chardet","idna","pystray","six","urllib3","multiprocessing","PIL","fcntl","pkg_resources","sysconfig"], 
        "excludes": ["django","scipy","numpy","PyQt5","llvmlite","notebook","babel","matplotlib","mkl","jupyter"],
        "include_files": ["config.py","gui.py","fun.py","src","vendor","config.ini"],
        'build_exe': './/build/EmoodMac3/'
    }
    base = None    


setup(  name = "emood",
        version = "0.5",
        
        description = "Share your E-Mood!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("emood.py", base=base,icon="src/logo.ico")])

