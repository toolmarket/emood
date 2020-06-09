version = "0.22"

# IMPORTS
# IMPORTS python -m pip install pillow tk image pywin32 pystray requests

import random, string, os, sys, datetime, time, importlib, threading, zipfile, io, json, subprocess, configparser, uuid, requests, shelve, pystray
import multiprocessing
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
# __file__, path, frozen, windows, python_path
__file__ = os.path.abspath( sys.argv[0])
filename = os.path.abspath( sys.argv[0])
path = os.path.dirname( os.path.abspath(sys.argv[0])) 
frozen = False
if getattr(sys, 'frozen', False): 
  frozen = True
try:
  python_path = sys.executable
except:
  python_path = False
os.chdir( path  )
cwd = os.getcwd()
#/GLOBALS
