version = "0.22"

# IMPORTS
# IMPORTS python -m pip install pillow tk image pywin32 pystray requests
import os
import sys

# Add vendor directory to module search path
parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, 'vendor')

sys.path.append(vendor_dir)
import random, string, datetime, time, importlib, threading, zipfile, io, json, subprocess, configparser, uuid, requests, shelve, pystray
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
  import pkg_resources
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