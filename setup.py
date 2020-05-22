import sys
from cx_Freeze import setup, Executable

# python setup.py build

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": 
["os","tkinter","sys","winerror","uuid","subprocess","importlib","configparser","threading","pathlib","dbm","shelve","zipfile","io","json","requests","certifi","chardet","idna","pystray","six","urllib3","multiprocessing","image","win32event","win32api"], 
    "excludes": ["django"],
    "include_files": ["emood.py","src","config.ini"]
}
#build_exe_options = {}





# GUI applications require a different base on Windows (the default is for a
# console application).
base = None

if sys.platform == "win32":
    base = "Win32GUI" # hides the console
    #base = None



setup(  name = "emood",
        version = "0.22",
        
        description = "Making RRHH great again!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("start.py", base=base,icon="src/logo.ico")])

