#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import *
import fun, gui


gui.smiles()


exit()







def initialization():
  """ STUFF THAT RUNS ONECE ON STARTUP"""
  # QUIZAS PODRIA PONER TODO ESTO EN CONFIG.PY
  
  pass


lastTick = 0
tickTime = 10 # Secconds
def main_process():
  """ STUFF THAT RUNS INSIDE A LOOP """
  global nowTick
  global lastTick
  nowTick = time.time()

  if(nowTick > lastTick + tickTime ):
    print( "Do something every tickTime ") # aca va lo que quiero analizar cada X catnidad de segundos. 
    #reply = send_ping() # Hay que mandar un ping cada X cantidad de segundos. 

    lastTick = time.time()

  pass



def send_ping():
    """  Sends Machine Id, Local Time, and any extra data. """
    config = shelve.open('src/data.db')
    machineTime = time.strftime("%Y-%m-%d %H:%M:%S")
    machineId = config["machineId"] # == USERID
    version = config["version"]
    company = config["company"]
    updated = config["updated"] # agregando la idea es que mande el ultimo update que recibio de esa empresa. asi si hay uno nuevo se los muestra. Si el update es mas viejo que x dias no lo mostraria.
    config.close()

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
    }
    data = {
        "action" : "ping",
        "machineTime" : machineTime,
        "version" : version,
        "machineId": machineId,
        "company": company,  
        "updated": updated
    }
    target_url = "http://emood.com.ar/api.php"
    r = requests.post(target_url, json=data, headers=headers)
    try:
        response = json.loads(r.text)
    except:
        print( r.text )
        return( {"action":"ok"} )
    return( response )

def main_loop(icon):
  """ ICON LOOP """
  icon.visible = True
  while icon.visible: #O while true si queremos que sea invisible.
    main_process() # All functions that go on loop.
    time.sleep(1)
    #print("Main loop...")
  return

def check_single_instance():
  if "--reload" not in sys.argv:
      if sys.platform.startswith('win'): #seria win32 siempre igual
          mutex = win32event.CreateMutex(None, False, "gTAvwfsTAvwf52rTAvwfg")
          last_error = win32api.GetLastError()
          if last_error == ERROR_ALREADY_EXISTS:
              print("App already running")
              os._exit(0)
      else:
          print("Not windows") # usar fctl ( Quizas no anda.)
          fh=open(os.path.realpath(__file__),'r')
          try:
              fcntl.flock(fh,fcntl.LOCK_EX|fcntl.LOCK_NB)
          except:
              print("App already running")
              os._exit(0)
  else:
      print("Reloaded!")

def randmom_string(stringlength=20, extra_characters="-/_?*=+()&$%#@<>.,;:[]\{\}/^!~"):
    '''Generates a random string'''
    return ''.join([random.choice(string.ascii_letters + string.digits + extra_characters  ) for n in range(stringlength)])

def create_machineId():
    '''Creates uuid'''
    uuid_hardware = str( uuid.getnode() )
    uuid_random = randmom_string(40)
    machine_id = uuid_hardware +"-"+ uuid_random
    return machine_id





























# MENU ITEMS

def open_config(icon, item):
  if windows:
    os.system("config.ini")
    # os.startfile("https://google.com.ar/") # si quiero abrir una URL
  else:
    try:
      subprocess.Popen(['open', "config.ini"])
    except:
      subprocess.Popen(['xdg-open', "config.ini"])

def open_website( icon, item ):
  url = "https://emood.com.ar/"
  if windows:
    os.startfile(url)
  else:
    try:
      subprocess.Popen(['open', url])
    except:
      subprocess.Popen(['xdg-open', url])

def quit_window(icon, item):
  icon.visible = False
  icon.stop()
  return

def show_window(icon, item):
  #window.after(0,window.deiconify)
  p = multiprocessing.Process(target=gui_generator, args=(3,"E-Mood V.{}".format(version) ) )
  p.start()
  p.join(20)
  p.terminate() # Lo cierra despues del join.

def mac_trials(icon, item):
  p = multiprocessing.Process(target=gui_generator, args=(0,"¿Te sentis bien Steve?" ) )
  p.start()
  p.join(10)
  p.terminate() # Lo cierra despues del join.




# ACTIONS
if __name__ == '__main__':
  # PRINT SOME DATA
  print(python_path)
  print ( str(sys.argv) )
  print("- CWD:      ",cwd)
  print("- PATH:     ", path )
  print("- __file__: ", __file__)


  multiprocessing.freeze_support() # Para multiprocesing
  multiprocessing.set_start_method('spawn') # fork crea una copia de memoria(?aprox)

  check_single_instance() # If not single instance exit.
  initialization() # on startup.

  image = Image.open("src/logo.ico")
  menu = pystray.Menu(pystray.MenuItem(text="Version", action=show_window, default=True),
                        pystray.MenuItem(text="Config", action=open_config),
                        pystray.MenuItem(text="Website", action=open_website),
                        pystray.MenuItem(text="Quit", action=quit_window)
                      )

  icon = pystray.Icon("E-Mood", image, "E-Mood Demo", menu)
  icon.run( main_loop )

  print("Exit on Main")
  sys.exit()


# from multiprocessing import Process, freeze_support, set_start_method

# def foo():
#     print('hello')

# if __name__ == '__main__':
#     multiprocessing.freeze_support()
#     multiprocessing.set_start_method('spawn')
#     p = multiprocessing.Process(target=foo)
#     p.start()





