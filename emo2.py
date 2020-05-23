#!/usr/bin/env python3
# -*- coding: utf-8 -*-
version = "0.22"

# IMPORTS python -m pip install pillow tk image pywin32 pystray requests
import random, string, os, sys, datetime, time, importlib, threading, zipfile, io, json, subprocess, configparser, uuid, requests, shelve, pystray
from PIL import Image  
import tkinter as tk
from pathlib import Path
if sys.platform.startswith('win'):
  windows = True
  import win32event
  import win32api
  from winerror import ERROR_ALREADY_EXISTS
else:
  import fcntl  # MAC and UNIX
  windows = False

# GLOBALS
# __file__, path, frozen, windows, 
__file__ = os.path.abspath( sys.argv[0]) 
path = os.path.dirname( os.path.abspath(sys.argv[0])) 
frozen = False
if getattr(sys, 'frozen', False): 
  frozen = True

print ( str(sys.argv) )
os.chdir( path  )
cwd = os.getcwd()
print("- CWD:      ",cwd)
print("- PATH:     ", path )
print("- __file__: ", __file__)


def initialization():
  """ STUFF THAT RUNS ONECE """
  pass



def main_process():
  """ STUFF THAT RUNS INSIDE A LOOP """
  pass




def main_loop(icon):
  """ ICON LOOP """
  icon.visible = True
  while icon.visible: #O while true si queremos que sea invisible.
    main_process() # All functions that go on loop.
    time.sleep(1)
    print("Main loop...")
  return




def open_config(icon, item):
  os.system("config.ini")

def quit_window(icon, item):
  icon.visible = False
  icon.stop()
  return

def show_window(icon, item):
  #window.after(0,window.deiconify)
  # x = threading.Thread(target=gui_generator, args=(3,"E-Mood V.{}".format(version) ), daemon=False)
  # x.start()
  # x.join(1800)
  # print("Show_window")
  pass	

















image = Image.open("src/logo.ico")
menu = pystray.Menu(pystray.MenuItem(text="Version", action=show_window, default=True),
                       pystray.MenuItem(text="Config", action=open_config),
                       pystray.MenuItem(text="Quit", action=quit_window)
                    )

icon = pystray.Icon("E-Mood", image, "E-Mood Demo", menu)
icon.run(main_loop)

print("Exit on Main")
sys.exit()






