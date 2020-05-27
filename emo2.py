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
  """ STUFF THAT RUNS ONECE ON STARTUP"""
  
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


def gui_tests(type=0,main_text="wolololo",questionId="DefaultId",questionType="Default",data=0):
    window = tk.Tk()
    os.chdir( path  )
    window.title("E-Mood v." )
    window_width = 600
    window_height = 300
    move_up = 100 # movemos la ventana unos pixeles para arriba.
    background_color = '#091337'
    window.configure(background=background_color)
    window.overrideredirect(1) # Remove border
    window.grid_rowconfigure(3, weight=1)
    window.grid_columnconfigure(3, weight=1)
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()  
    window.geometry("%dx%d+%d+%d" % (window_width, window_height,screen_width/2-window_width/2, screen_height/2-window_height/2 - move_up)) 
    try:
      window.iconbitmap('src/logo.ico')
    except:
      print("Icon bitmap error.")
    window.resizable(0, 0) # Can't Resize
    window.lift(aboveThis=window) 
    window.wm_attributes("-topmost", 1) # always on top
    tk.Label(window, text = main_text, fg="#FFFFFF", font='Sans 20', background=background_color).grid(row=0,column=0,columnspan=9,pady=20)   # Helvetica
    print("PNG not working.")
    img1 = tk.PhotoImage(file="src/sad.gif")
    img2 = tk.PhotoImage(file="src/neutral.gif")
    img3 = tk.PhotoImage(file="src/smile.gif")          
    tk.Button(window, text='', width=150,height=120,cursor="hand2",border=0,background=background_color,image = img1, command=window.destroy ).grid(row=2,column=1,pady=20,padx=20)
    tk.Button(window, text='', width=150,height=120,cursor="hand2",border=0,background=background_color,image = img2, command=window.destroy ).grid(row=2,column=3,pady=20)
    tk.Button(window, text='', width=150,height=120,cursor="hand2",border=0,background=background_color,image = img3, command=window.destroy ).grid(row=2,column=6,pady=20,padx=20)
    window.focus_force() # le da foco a la ventana
    window.mainloop()



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




# Tkinter GUI
def gui_generator(type=0,main_text="¿Cómo te sentís?",questionId="DefaultId",questionType="Default",data=0):
    """ Creates the windows """
    config = shelve.open('src/data.db') 
    window = tk.Tk()
    window.title("E-Mood v." + str( config["version"] ) )
    window_width = 600
    window_height = 300
    move_up = 100 # movemos la ventana unos pixeles para arriba.
    background_color = '#091337'
    window.configure(background=background_color)
    window.overrideredirect(1) # Remove border
    window.grid_rowconfigure(3, weight=1)
    window.grid_columnconfigure(3, weight=1)
    questionTime = time.strftime("%Y-%m-%d %H:%M:%S")

    config.close()

    # Botones de Acciones dentro del GUI. 
    def btn_next(datos=0):
        print(datos)
        window.destroy()

        with shelve.open('src/data.db') as config: #
            config['questionData'] = datos
            # config['questionId'] = questionId
            # config['questionType'] = questionType

        if datos == -1:
            gui_generator(1,"¿Por qué estas mal?",questionId,questionType,datos)
        if datos == 0:
            gui_generator(1,"¿Queres dejar un Comentario?,",questionId,questionType,datos)
        if datos == 1:
            gui_generator(1,"¿Queres contar por qué?",questionId,questionType,datos)

    def save_answer(data=0):
        config = shelve.open('src/data.db') # Abrimos la base de datos para guardar la respuesta.

        inputValue= textBox.get("1.0","end-1c").strip()
        

        answerTime = time.strftime("%Y-%m-%d %H:%M:%S")

        questionId = config['questionId']
        questionData = config['questionData']
        questionType = config['questionType']

        print(inputValue, questionId)
        #config.setdefault('unsentAnswers', []) # list.append()
        new_data = {
            "answerTime": answerTime,
            "questionTime": questionTime,
            "userId": config["userId"],
            "questionId": questionId,
            "version": config["version"],
            "company": config["company"],
            "feedback": inputValue,
            "answer": questionData,
            "department": config["department"],
            "questionType": questionType,
        }
        try:
            unsentAnswers = config['unsentAnswers'] # Crear un nuevo shelve solo para esto. No utilizar la configuración.
        except:
            config['unsentAnswers'] = []
            unsentAnswers = config['unsentAnswers']
        unsentAnswers.append(new_data)
        config['unsentAnswers'] = unsentAnswers
        for answer in config['unsentAnswers']:
            print ( answer )

        config['questionData'] = ""
        config['questionId'] = ""
        config['questionType'] = ""
        config.close() # Cerrando la base
        # config.sync()
        # Quizas la podemos guardar y meter en el loop siguiente de "envio de respuestas". Pero necesitamos un ID para la pregunta. 
        window.destroy()
    def input_keyup(data):
        print(data.keycode)
        inputValue= textBox.get("1.0","end-1c").strip()
        if len(inputValue) > 1:
            send_button.config(text='Enviar')
        else:
            send_button.config(text='No')
        if(data.keycode == 13): # Enter ahora envia el formulario.
            save_answer()


    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()  
    window.geometry("%dx%d+%d+%d" % (window_width, window_height,screen_width/2-window_width/2, screen_height/2-window_height/2 - move_up)) 
    # https://www.tutorialspoint.com/python/tk_grid.htm  # Tutorial de Grid
    # prog_call = sys.argv[0] # los argumentos
    # prog_location = os.path.split(prog_call)[0]
    # photo_location = os.path.join(prog_location,"src/happy.png")
   
    if type == 0: # SHOW FACES
        tk.Label(window, text = main_text, fg="#FFFFFF", font='Sans 20', background=background_color).grid(row=0,column=0,columnspan=9,pady=20)   # Helvetica
        img1 = tk.PhotoImage(file="src/sad.png")
        img2 = tk.PhotoImage(file="src/neutral.png")
        img3 = tk.PhotoImage(file="src/smile.png")

        tk.Button(window, text='', width=150,height=120,cursor="hand2",border=0,background=background_color,image = img1, command=lambda: btn_next(-1) ).grid(row=2,column=1,pady=20,padx=20)
        tk.Button(window, text='', width=150,height=120,cursor="hand2",border=0,background=background_color,image = img2, command=lambda: btn_next(0) ).grid(row=2,column=3,pady=20)
        tk.Button(window, text='', width=150,height=120,cursor="hand2",border=0,background=background_color,image = img3, command=lambda: btn_next(1) ).grid(row=2,column=6,pady=20,padx=20)

    if type == 1: # INPUT TEXT
        tk.Label(window, text = main_text, fg="#FFFFFF", font='Sans 20', background=background_color).grid(row=0,column=0,columnspan=9,pady=20)   # Helvetica
        textBox = tk.Text(window, width=50,height=6)
        textBox.grid(row=2,column=0,columnspan=9,pady=20)
        send_button = tk.Button(window, text='No', font='Sans 20', width=20,height=6,cursor="hand2",border=0, command=lambda: save_answer() )
        send_button.grid(row=3,column=3,pady=20,padx=20)
        window.bind_all('<KeyRelease>', input_keyup)
        window.focus_force() # le da foco a la ventana
        # window.after(1, lambda: window.focus_force()) 
    # window.wm_attributes("-transparentcolor", 'grey') hace que el gris sea transparente y crea un agujero en la imagen.

    if type == 2: # CUSTOM TEXT YES NO
        tk.Label(window, text = main_text, fg="#FFFFFF", font='Sans 16', background=background_color,wraplength=500,justify="center").grid(row=0,column=0,rowspan=2,columnspan=9,pady=20,padx=20)   # Helvetica
        tk.Button(window, text='Aceptar', font='Sans 20', width=10,height=1,cursor="hand2",border=0, command=window.destroy ).grid(row=3,column=4,pady=20,padx=20)
        tk.Button(window, text='Cancelar', font='Sans 20', width=10,height=1,cursor="hand2",border=0, command=window.destroy ).grid(row=3,column=2,pady=20,padx=20)
        window.focus_force() # le da foco a la ventana
    if type == 3: # CUSTOM CLOSE
        tk.Label(window, text = main_text, fg="#FFFFFF", font='Sans 16', background=background_color,wraplength=500,justify="center").grid(row=0,column=0,rowspan=2,columnspan=9,pady=20,padx=20)   # Helvetica
        tk.Button(window, text='Ok', font='Sans 20', width=10,height=1,cursor="hand2",border=0, command=window.destroy ).grid(row=3,column=3,pady=20,padx=20)
       # tk.Button(window, text='Cancelar', font='Sans 20', width=10,height=1,cursor="hand2",border=0, command=window.destroy ).grid(row=3,column=2,pady=20,padx=20)
        window.focus_force() # le da foco a la ventana



    window.iconbitmap('src/logo.ico')
    window.resizable(0, 0) # Can't Resize
    window.lift(aboveThis=window) 
    # window.wm_attributes("-alpha",0.3) # -notify https://wiki.tcl-lang.org/page/wm+attributes
    window.wm_attributes("-topmost", 1) # always on top
    
    window.mainloop() #bloquea la ejecución del script.






def gui_tests2(type=0,main_text="wolololo",questionId="DefaultId",questionType="Default",data=0):
    window = tk.Tk()
    os.chdir( path  )
    window.title("E-Mood v." + str( version ) )
    window_width = 600
    window_height = 300
    move_up = 100 # movemos la ventana unos pixeles para arriba.
    background_color = '#091337'
    window.configure(background=background_color)
    window.overrideredirect(1) # Remove border
    window.grid_rowconfigure(3, weight=1)
    window.grid_columnconfigure(3, weight=1)
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()  
    window.geometry("%dx%d+%d+%d" % (window_width, window_height,screen_width/2-window_width/2, screen_height/2-window_height/2 - move_up)) 
    try:
      window.iconbitmap('src/logo.ico')
    except:
      print("Icon bitmap error.")
    window.resizable(0, 0) # Can't Resize
    window.lift(aboveThis=window) 
    window.wm_attributes("-topmost", 1) # always on top
    

    if type == 0: # SHOW FACES
        tk.Label(window, text = main_text, fg="#FFFFFF", font='Sans 20', background=background_color).grid(row=0,column=0,columnspan=9,pady=20)   # Helvetica
        try:
          img1 = tk.PhotoImage(file="src/sad.png")
          img2 = tk.PhotoImage(file="src/neutral.png")
          img3 = tk.PhotoImage(file="src/smile.png")
        except:
          print("PNG not working.")
          img1 = tk.PhotoImage(file="src/sad.gif")
          img2 = tk.PhotoImage(file="src/neutral.gif")
          img3 = tk.PhotoImage(file="src/smile.gif")          

        tk.Button(window, text='', width=150,height=120,cursor="hand2",border=0,background=background_color,image = img1, command=window.destroy ).grid(row=2,column=1,pady=20,padx=20)
        tk.Button(window, text='', width=150,height=120,cursor="hand2",border=0,background=background_color,image = img2, command=window.destroy ).grid(row=2,column=3,pady=20)
        tk.Button(window, text='', width=150,height=120,cursor="hand2",border=0,background=background_color,image = img3, command=window.destroy ).grid(row=2,column=6,pady=20,padx=20)

    if type == 4: # SHOW jpg
        tk.Label(window, text = main_text, fg="#FFFFFF", font='Sans 20', background=background_color).grid(row=0,column=0,columnspan=9,pady=20)   # Helvetica
        try:
          img1 = tk.PhotoImage(file="src/sad.jpg")
          img2 = tk.PhotoImage(file="src/neutral.jpg")
          img3 = tk.PhotoImage(file="src/smile.jpg")  
        except:
          print("JPG not working.")
          img1 = tk.PhotoImage(file="src/sad.gif")
          img2 = tk.PhotoImage(file="src/neutral.gif")
          img3 = tk.PhotoImage(file="src/smile.gif")                
        tk.Button(window, text='', width=150,height=120,cursor="hand2",border=0,background=background_color,image = img1, command=window.destroy ).grid(row=2,column=1,pady=20,padx=20)
        tk.Button(window, text='', width=150,height=120,cursor="hand2",border=0,background=background_color,image = img2, command=window.destroy ).grid(row=2,column=3,pady=20)
        tk.Button(window, text='', width=150,height=120,cursor="hand2",border=0,background=background_color,image = img3, command=window.destroy ).grid(row=2,column=6,pady=20,padx=20)



    if type == 1: # INPUT TEXT
        tk.Label(window, text = main_text, fg="#FFFFFF", font='Sans 20', background=background_color).grid(row=0,column=0,columnspan=9,pady=20)   # Helvetica
        textBox = tk.Text(window, width=50,height=6)
        textBox.grid(row=2,column=0,columnspan=9,pady=20)
        send_button = tk.Button(window, text='No', font='Sans 20', width=20,height=6,cursor="hand2",border=0, command=window.destroy )
        send_button.grid(row=3,column=3,pady=20,padx=20)
        window.focus_force() # le da foco a la ventana
        # window.after(1, lambda: window.focus_force()) 
    # window.wm_attributes("-transparentcolor", 'grey') hace que el gris sea transparente y crea un agujero en la imagen.

    if type == 2: # CUSTOM TEXT YES NO
        tk.Label(window, text = main_text, fg="#FFFFFF", font='Sans 16', background=background_color,wraplength=500,justify="center").grid(row=0,column=0,rowspan=2,columnspan=9,pady=20,padx=20)   # Helvetica
        tk.Button(window, text='Aceptar', font='Sans 20', width=10,height=1,cursor="hand2",border=0, command=window.destroy ).grid(row=3,column=4,pady=20,padx=20)
        tk.Button(window, text='Cancelar', font='Sans 20', width=10,height=1,cursor="hand2",border=0, command=window.destroy ).grid(row=3,column=2,pady=20,padx=20)
        window.focus_force() # le da foco a la ventana
    if type == 3: # CUSTOM CLOSE
        tk.Label(window, text = main_text, fg="#FFFFFF", font='Sans 16', background=background_color,wraplength=500,justify="center").grid(row=0,column=0,rowspan=2,columnspan=9,pady=20,padx=20)   # Helvetica
        tk.Button(window, text='Ok', font='Sans 20', width=10,height=1,cursor="hand2",border=0, command=window.destroy ).grid(row=3,column=3,pady=20,padx=20)
       # tk.Button(window, text='Cancelar', font='Sans 20', width=10,height=1,cursor="hand2",border=0, command=window.destroy ).grid(row=3,column=2,pady=20,padx=20)
        window.focus_force() # le da foco a la ventana
    
    window.mainloop()






























# MENU ITEMS

def open_config(icon, item):
  os.system("config.ini")

def quit_window(icon, item):
  icon.visible = False
  icon.stop()
  return

def show_window(icon, item):
  #window.after(0,window.deiconify)
  x = threading.Thread(target=gui_generator, args=(3,"E-Mood V.{}".format(version) ), daemon=False)
  x.start()
  x.join()

def mac_trials(icon, item):
  print("NO THREADS T1")
  try:
    gui_tests(0,"No thread 0.")
  except Exception as e:
    print( "type error: " + str(e) )
  print("NO THREADS T2")
  try:
    gui_tests(1,"No thread 1.")
  except Exception as e:
    print( "type error: " + str(e) )
  print("NO THREADS T3")
  try:
    gui_tests(2,"No thread 2.")
  except Exception as e:
    print( "type error: " + str(e) ) 
  print("NO THREADS T4")
  try:
    gui_tests(3,"No thread 3.")
  except Exception as e:
    print( "type error: " + str(e) )
  print("NO THREADS T5")
  try:
      gui_tests(4,"No thread 4. JPG")
  except Exception as e:
    print( "type error: " + str(e) )  



def mac_trials2(icon, item):
  print("THREADS T1")
  try:
    x = threading.Thread(target=gui_tests, args=(0,"Thread test. Daemon False" ), daemon=False)
    x.start()
    x.join()
  except Exception as e:
    print( "type error: " + str(e) )  

  print("THREADS T2")
  try:
    x = threading.Thread(target=gui_tests, args=(1,"Thread test. Daemon False" ), daemon=False)
    x.start()
    x.join()
  except Exception as e:
    print( "type error: " + str(e) )  

  print("THREADS T3")
  try:
    x = threading.Thread(target=gui_tests, args=(4,"Thread test. Daemon False JPG" ), daemon=False)
    x.start()
    x.join()
  except Exception as e:
    print( "type error: " + str(e) )  
  print("THREADS T4")
  try:
    x = threading.Thread(target=gui_tests, args=(4,"Thread test. Daemon JPG True" ), daemon=True)
    x.start()
    x.join()
  except Exception as e:
    print( "type error: " + str(e) )  

  print("THREADS T4")
  try:
    x = threading.Thread(target=gui_tests, args=(0,"Last Thread test. Daemon True" ), daemon=True)
    x.start()
    x.join()
  except Exception as e:
    print( "type error: " + str(e) )  



# ACTIONS




check_single_instance() # If not single instance exit.
initialization() # on startup.


image = Image.open("src/logo.ico")
menu = pystray.Menu(pystray.MenuItem(text="Version", action=show_window, default=True),
                       pystray.MenuItem(text="Config", action=open_config),
                       pystray.MenuItem(text="Mac-Tests", action=mac_trials),
                       pystray.MenuItem(text="Mac-Tests Threads", action=mac_trials2),
                       pystray.MenuItem(text="Quit", action=quit_window)
                    )

icon = pystray.Icon("E-Mood", image, "E-Mood Demo", menu)
icon.run(main_loop)

print("Exit on Main")
sys.exit()






