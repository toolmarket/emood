#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import *
import fun, gui


# fun.first_run() # Setea lo basico. 

# gui.smiles()


# gui.show_text(main_text="E-Mood Demo v.{}".format(version),
#   secondary_text="Aqui puede ir mucho texto.")

# exit()



# CRONJOB LOOP
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



    smiles = fun.show_smiles()
    if smiles:
      questionId = time.strftime("%Y-%m-%d %H:00:00")+"Smiles"
      p = multiprocessing.Process(target=gui.smiles, args=("¿CÓMO TE SIENTES?",questionId ) )
      p.start()
      p.join(3400) # WAITS ALMOST ONE HOUR BEFORE CLOSING SMILES.
      p.terminate() # Lo cierra despues del join.



    lastTick = time.time()

  pass
























# ICON LOOP
def main_loop(icon):
  """ ICON LOOP """
  icon.visible = True
  while icon.visible: #O while true si queremos que sea invisible.
    main_process() # All functions that go on loop.
    time.sleep(1)
    #print("Main loop...")
  return



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
  p = multiprocessing.Process(target=gui.show_text, args=("E-Mood Demo v.{}".format(version),
  "Todo funciona correctamente.\n Windows={}\n Frozen={}\nFile_path={}\nPath={}\nPython={}".format(windows,frozen,__file__,path,python_path ),
  "Ir a la Web",
  "https://emood.com.ar",
  "Cerrar"  ) )
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

  fun.check_single_instance() # If not single instance exit.

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





