#!/usr/bin/env python3
import sys, os

python_path = sys.executable
path = os.path.dirname( os.path.abspath(sys.argv[0])) 

# Instalamos PIP si no existe. 
try:
    import pip
except:
    os.system(python_path + " get-pip.py" )


if sys.platform == "darwin":
    print("- Mac Detected.")
    
    # Instalamos los paquetes que podemos.

    packages = ["os","tkinter","sys","uuid","subprocess","importlib",
    "configparser","threading","pathlib","dbm","shelve","zipfile","io","json","requests",
    "certifi","chardet","idna","pystray","six","urllib3","multiprocessing","PIL","fcntl","mac-login-items"]
    
    for package in packages:
        try:
            os.system(python_path + " -m pip install "+package )
        except Exception as e:
            print( "Error: " + str(e) )

    # Agregamos a AUTOINICIO SI NO EXISTE
    os.system("cp emood.py emood.command")
    os.system("chmod +x emood.command")
    os.system("login-items rm emood.command")
    os.system("login-items add {}/emood.command".format(path) ) # path
    os.system("emood.command")









if sys.platform == "win32":
    print("- Windows Detected")
    
    packages = ["os","tkinter","sys","uuid","subprocess","importlib",
    "configparser","threading","pathlib","dbm","shelve","zipfile","io","json","requests",
    "certifi","chardet","idna","pystray","six","urllib3","multiprocessing","PIL","fcntl"]
    
    for package in packages:
        try:
            #pipmain( ['install', package] )
            #os.execv(python_path, ['python.exe -m pip install',package])
            os.system(python_path + " -m pip install "+package )
        except Exception as e:
            print( "Error: " + str(e) )


# python_path