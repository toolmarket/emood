#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SETTINGS
version = "0.22"

# IMPORTS y Functions 
import random, string
import os, sys, datetime, time
import shelve # Config/Database
import uuid # para el uniquid
import importlib
from PIL import Image  # python -m pip install image pywin32 
import tkinter as tk
import threading
import requests
from pathlib import Path
import zipfile, io, json # Para updates
import pystray # Para trayIcon
from pystray import MenuItem as item #pip install pystray
import pystray
import subprocess

if sys.platform.startswith('win'):
  import win32event
  import win32api
  from winerror import ERROR_ALREADY_EXISTS
else:
  # import fcntl  # MAC and UNIX
  pass

import configparser # config.ini

__file__ = os.path.abspath( sys.argv[0]) 
path = os.path.dirname( os.path.abspath(sys.argv[0])) 
# startup_path = os.path.join('C:\\Users\\',os.getlogin(),'\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\')

frozen = False
if getattr(sys, 'frozen', False): 
  frozen = True


# Functions
def first_run():
  """ Checks if frist run. Does the stuff it should do on first run """
  first_run = False
  config = shelve.open('src/data.db') #.clear() borra el contenido del shelve.
  config["version"] = version
  
  # Gets or Creates machine Id
  try:
      machineId = config["machineId"]
  except:
      first_run = True
      machineId = create_machineId()
      config["machineId"] = machineId

  ini = configparser.ConfigParser()
  ini.read('config.ini')
  for key in ini['defaults']:  
    print(key, ini['defaults'][key])

  if ini['defaults']['Startup'] == "1":
    print("Add to startup")
    add_to_startup()
      
  if( first_run ):
      # Add script to startup. write config.ini
      # Read Config and Print Keys
      config["userId"] = config["machineId"]
      config["company"] = ini['defaults']['CompanyName']
      config["department"] = "default"
      config["show_smiles"] = ini['defaults']['SurveyTimes']
      config["questions_answered"] = ""
      config['unsentAnswers'] = []

  print ( list( config.keys() ) ) # ['machineId', 'uuId', 'userId', 'version', 'company', 'department', 'unsentAnswers']
  config.close()

def add_to_startup():
  if sys.platform.startswith('win') and getattr(sys, 'frozen', False): #if Frozen
    subprocess.call("powershell \"$s=(New-Object -COM WScript.Shell).CreateShortcut('%userprofile%\Start Menu\Programs\Startup\emood.lnk');$s.TargetPath='{}';$s.Save()\"".format(__file__), shell=True)



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



def show_smiles(testingTime=False):
    """ Validate if there is any smile to show """
    config = shelve.open('src/data.db')
    nowHours = time.strftime("%H")
    nowMinutes = time.strftime("%M")
    nowDate = time.strftime("%m-%d")

    if testingTime:
        config["show_smiles"] = testingTime  # "10:10;16:10"  ########### TESTING VAR
    test = config["questions_answered"]

    print("-Checking Smiles...")

    smile_times = config["show_smiles"].split(";")
    for times in smile_times:
        checking = times.split(":")
        if( nowHours == checking[0] and nowMinutes >= checking[1] and (times+nowDate not in test) ): ## && not in array QUESTIONS_ANSWERED.
            print("---- Showing Smiles!")
            config["questions_answered"] = config["questions_answered"]+times+nowDate+";"[-300:] # limita la cantidad de respuestas guardadas.
            config.close()
            return True

      #timePassed = datetime.datetime.strptime(nowTime, "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S") # 0:17:05
      # timePassed.total_seconds() # Float. 


    config.close()

    return False



def send_ping():
    """  Sends Machine Id, Local Time, and any extra data. """
    config = shelve.open('src/data.db')
    machineTime = time.strftime("%Y-%m-%d %H:%M:%S")
    machineId = config["machineId"] # == USERID
    version = config["version"]
    company = config["company"]
    config.close()
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
    }
    data = {
        "action" : "ping",
        "machineTime" : machineTime,
        "version" : version,
        "machineId": machineId,
        "company": company  
    }
    target_url = "http://emood.com.ar/api.php"
    r = requests.post(target_url, json=data, headers=headers)
    try:
        response = json.loads(r.text)
    except:
        print( r.text )
        return( {"action":"ok"} )
    return( response )

def download_update(update_url="https://emood.com.ar/update.zip",update_dir="./"):
    ''' Download update. Restart. '''
    headers = { # Hay que poner un U.A.  o Bluehost lo bloquea.
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
    }
    r = requests.get(update_url,headers=headers)
    try:
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(update_dir)
    except Exception as e:
      print( "type error: " + str(e) )
      return False
    return True

# Tkinter GUI
def gui_generator(type=0,main_text="¿Cómo te sentís?",questionId="DefaultId",questionType="Default",data=0):
    """ Creates the windows """
    #path = os.path.dirname( os.path.abspath(__file__) )
    #os.chdir( path ) # Cambiar el workingdir a dode esta este script(los threads se pierden un poco si no)
    config = shelve.open('src/data.db') 
    window = tk.Tk()
    window.title("E-Mood v." + str( config["version"] ) )
    window_width = 600
    window_height = 300
    move_up = 100 # movemos la ventana unos pixeles para arriba.
    background_color = '#091337'
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













































# PRINT SOME DATA
print ( str(sys.argv) )

# Check if its the only one running


# if getattr(sys, 'frozen', False): ### NO ESTOY SUPER SEGURO DE ESTO.
#     # frozen
#     path = os.path.realpath(sys.executable)
# else:
#     # unfrozen
#     path = os.path.dirname( os.path.realpath(__file__) )



os.chdir( path  )
cwd = os.getcwd()
print("- CWD:      ",cwd)
print("- PATH:     ", path )
print("- __file__: ", __file__)

check_single_instance()
first_run()



print( sys.version )
total_timer = time.time() # Iniciamos un timer
print("Started At: "+str( time.strftime('%Y-%m-%d %H:%M:%S') ) )

# Path("src/").mkdir(parents=True, exist_ok=True) # Creamos la carpeta SRC si no existe.


# x = threading.Thread(target=thread_function, args=(1,), daemon=True) # daemon significa que el main script no espera a que termine de ejecutarse para cerrarse. 
#gui_generator(type=0,main_text="¿Cómo te sentís?",questionId="DefaultId",questionType="Default")
# gui_generator(type=2,main_text="Te gustaría saber más sobre las promociones para empleados? Llamá a RRHH para recibir tu cupón! tel: 0800-33444 https://rrhh.com")

# send_hello()

# After Update something like this.
# os.execvp("python.exe",["main.py"]) # https://docs.python.org/3/library/os.html#os.execlp
# exit()


#download_update()
#exit()


# Main loop. Que despues tiene que estar dentro del wrapper del icono de pysystray.
last_update = ""
start_time = time.strftime("%Y-%m-%d %H:%M:%S")

def main_loop(icon):
  icon.visible = True

  while icon.visible: #O while true si queremos que sea invisible.
    """ 
    - Check for commands and updates and Send Keep Alive. 
      Que mandamos? La hora local + id de la maquina y analizamos la respuesta para ver si hay acciones para realizar. 

    - Send Answers.
    - Check if survey faces are configured to start. 
    """
    nowTime = time.strftime("%Y-%m-%d %H:%M:%S")

    timePassed = datetime.datetime.strptime(nowTime, "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S") # 0:17:05
    # timePassed.total_seconds() # Float. 
    
    # PING SERVER with data. 
    try:
      reply = send_ping()
      if (reply["action"] == "update"): # IF REPLY UPDATE
        print("update with: "+reply["url"])
        updated = download_update( reply["url"], update_dir="./")

        if updated:
          print(__file__)
          icon.visible = False
          icon.stop()
          if getattr(sys, 'frozen', False):
            os.execv(__file__, sys.argv)
          else:
            print("NOT FROZEN")
            os.execvp("python",["python", "start.py --reload"])

          exit()

      print(reply)
    except Exception as e:
      print("type error: " + str(e))
      print("Ping Error. :( ")

    config = shelve.open('src/data.db')
    #config['unsentAnswers'] = []
    try:
      if len( config['unsentAnswers']  ) > 0:
        headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
        }
        target_url = "http://emood.com.ar/api.php"

        reply = requests.post(target_url, json=config['unsentAnswers'], headers=headers)

        print(reply.reason,reply.request, reply.text)
        if( reply.text == "ok"):
          config['unsentAnswers'] = []
          print("DATA SENT!!!!!!!!!!!!")

    except:
      # config['unsentAnswers'] = []
      time.sleep(30) # Algun problema de envio o recepcion
      print("- Nothing to send or error sending. Who knows.")
    config.close()

    
    # SHOULD WE SHOW SMILES
    smiles = show_smiles()

    if smiles:
      questionId = time.strftime("%Y-%m-%d %H:00:00")+"Smiles"
      questionType = "Smiles"
      
      with shelve.open('src/data.db') as config: #Guardamos en el Shelve la data para mandar
        config['questionId'] = questionId
        config['questionType'] = questionType

      x = threading.Thread(target=gui_generator, args=(0,"¿Cómo te sentís?",questionId,"Smiles"), daemon=False)
      x.start()
      x.join(1800) # Va a mostrar 30 min el gui y morir. 
    
    # x = threading.Thread(target=gui_generator, args=(2,"Mensaje 1"), daemon=False).start() # Blocking. 
    print( "Sleeping ", nowTime," Running_For: ", timePassed.total_seconds() ) #
    
    time.sleep(5)
  
  #icon.visible = False
  # Breaking Icon Loop
  return



# """ THREADS GUI """
# x = threading.Thread(target=gui_generator, args=(2,"Mensaje 1"), daemon=False).start()
# time.sleep(1) # Entre generacion de GUIs para evitar errores (por algún motivo)
# y = threading.Thread(target=gui_generator, args=(2,"Mensaje 2"), daemon=False).start()

# threads.append( x )
# x.start()
#gui_generator()

# print("Press any key...")
# pause = input()




image = Image.open("src/logo.ico")


def open_config(icon, item):
  #subprocess.run(['open', "config.ini"], check=True)
  os.system("config.ini")



def quit_window(icon, item):
  icon.visible = False
  icon.stop()
  sys.exit(1) # Exit solo no mataba los threads.  sys.exit(1)
  exit()

def show_window(icon, item):
  #window.after(0,window.deiconify)
  x = threading.Thread(target=gui_generator, args=(3,"E-Mood V.{}".format(version) ), daemon=False)
  x.start()
  x.join(1800)
  print("Show_window")
  pass

menu = pystray.Menu(pystray.MenuItem(text="Version", action=show_window, default=True),
                       pystray.MenuItem(text="Config", action=open_config),
                       pystray.MenuItem(text="Quit", action=quit_window)
                    )

icon = pystray.Icon("E-Mood", image, "E-Mood Demo", menu)
icon.run(main_loop)


print("ended")

sys.exit()


















# image = Image.open("src/icon.ico")




# import pystray

# icon = pystray.Icon('test name')

# from PIL import Image, ImageDraw

# def create_image():
#     # Generate an image and draw a pattern
#     image = Image.new('RGB', (width, height), color1)
#     dc = ImageDraw.Draw(image)
#     dc.rectangle(
#         (width // 2, 0, width, height // 2),
#         fill=color2)
#     dc.rectangle(
#         (0, height // 2, width // 2, height),
#         fill=color2)

#     return image

# icon.icon = create_image()





# class FakeDatabase:
#     def __init__(self):
#         self.value = 0
#         self._lock = threading.Lock()

#     def locked_update(self, name):
#         logging.info("Thread %s: starting update", name)
#         logging.debug("Thread %s about to lock", name)
#         with self._lock:
#             logging.debug("Thread %s has lock", name)
#             local_copy = self.value
#             local_copy += 1
#             time.sleep(0.1)
#             self.value = local_copy
#             logging.debug("Thread %s about to release lock", name)
#         logging.debug("Thread %s after release", name)
#         logging.info("Thread %s: finishing update", name)







total_timer = str( datetime.timedelta( seconds=round( time.time() - total_timer,2 ) ) ) #total_timer = time.time() - total_timer 
print("[Completed in {}s]\n".format(total_timer))








"""








configuration.js

const nodemachine = require('node-machine-id');

global.this_version = "0.1";

global.developer_mode_window = false;
global.machineId = nodemachine.machineIdSync(true);
global.minute_time = 60000;

// Tenemos mensajes pendientes?
global.answer_config = global.store.get( 'answer_config' ) || [];

//===> COSAS PARA TEST.
global.answer_config = []; // BORRAMOS EL config PARA TEST.
// global.store.set('last_answer_time',"//BORRAMOS LAST ANSWER");
// global.minute_time = 10000;
global.this_company = "Custom";
global.this_department = "Everyone";

//===> COSAS PARA TEST. END



global.configuration = global.store.get('config');
if( !global.configuration ) {
  console.log("App missing configuration file.");
  // (login and) GET REMOTE CONFIG.
  global.configuration = {
    // 'question_times': [9,10,11,12,13,14,15,16,17],
    // 'question_days': [0,1,2,3,4,5,6],
    'question_times': [10,16],
    'question_days': [1,2,3,4,5],    
    'company_name':"E-mood Inc."
  }


"""


















"""
  index.js



  const { remote, app, BrowserWindow, Tray, Menu } = require('electron');
const fetch = require("node-fetch");

const { autoUpdater } = require("electron-updater")

// https://github.com/sindresorhus/electron-is-dev
const isDev = require('electron-is-dev');
if (isDev) {
	console.log('Running in development');
} else {
	console.log('Running in production');
}


// https://hackernoon.com/electron-the-bad-parts-2b710c491547



// to-do // 
// npm install
// electron-forge run make --platform=win32
// npm run make --platform=win32
// https://www.electronforge.io/config/makers/dmg

const path = require('path');
var url = require('url');

const Store = require('electron-store');
const store = new Store();
global.store = store;
// PRUEBAS DE DATOS DE LA PC.
var os = require('os');
//var prettyBytes = require('pretty-bytes');
var prettyBytes = "";
console.log('Number of cpu cores: ' + os.cpus().length);

var iconpath = path.join(__dirname, 'logo.ico');

// Handle creating/removing shortcuts on Windows when installing/uninstalling.
if ( require('electron-squirrel-startup') ) { // eslint-disable-line global-require
  app.quit();
}



// autoupdate
// https://www.electronjs.org/docs/api/auto-updater#event-checking-for-update
// require('update-electron-app')()

//  ---CHEQUEAMOS SI ESTA CONFIGURADO
require('./configuration.js');


// Chequear Single Instance
// https://stackoverflow.com/questions/35916158/how-to-prevent-multiple-instances-in-electron
const gotTheLock = app.requestSingleInstanceLock();

if (!gotTheLock) {
  app.quit();
} 





// TESTING

function everyMinute() {

  var now = new Date();
  global.now_minutes = now.getMinutes();
  global.now_hour = now.getHours();
  global.weekday = now.getDay();
  global.now_day = now.getDate();
  global.now_month = now.getMonth();
  global.now_year = now.getFullYear();
  global.day_hour = now_hour.toString()+now_day.toString();
  global.hourstamp = now.getFullYear()+"-"+("00" + (now.getMonth() + 1)).slice(-2) + "-" +("00" + now.getDate()).slice(-2) + " " +("00" + now.getHours()).slice(-2) + ":00:00";
  global.timestamp = now.getFullYear()+"-"+("00" + (now.getMonth() + 1)).slice(-2) + "-" +("00" + now.getDate()).slice(-2) + " " +("00" + now.getHours()).slice(-2) + ":" +("00" + now.getMinutes()).slice(-2) + ":" +("00");

  console.log('Tick: '+ global.timestamp +': '+ global.machineId);
  console.log( JSON.stringify( global.answer_config ) );

  // find if we need to send answers. [answer_config]
  // find if configuration changed or new custom messages. ( LATTER MAKE THIS EVERY HOUR );

  //find if there is a new MSG or Question from RRHH.

  // Chequear si hay una pregunta abierta, y si la hay ignorar el resto.

  ShowSmiles();



} // everyMinute

setInterval(everyMinute, global.minute_time);


// # Guardar respuesta en memoria. Sumarla al config y llamar al envio de este.
//exports.StoreAnswer() = StoreAnswer();


// IPC LISTENER
const {ipcMain} = require('electron');

ipcMain.on('StoreAnswer', (event, data) => {
    var now = new Date();
    data["answerTime"] = now.getFullYear()+"-"+("00" + (now.getMonth() + 1)).slice(-2) + "-" +("00" + now.getDate()).slice(-2) + " " +("00" + now.getHours()).slice(-2) + ":" +("00" + now.getMinutes()).slice(-2) + ":" +("00" + now.getSeconds()).slice(-2);
    data["questionTime"] = global.timestamp;
    data["userId"] = global.machineId;
    data["questionId"] = global.questionId;
    data["version"] = global.this_version;
    data["company"] = global.this_company;
    data["department"] = global.this_department;
    data["questionType"] = global.this_questionType;
    data["version"] = global.this_version;
    console.log(data);
    StoreAnswer(data);
    global.question_visible = false;
});


// FUNCTIONS
// #Guarda y trata de enviar la respuesta. 
function StoreAnswer(data) {

  global.answer_config.push ( data );
 // console.log( JSON.stringify(global.answer_config ) );
  store.set( 'answer_config', global.answer_config  );
  for (let i = 0; i < global.answer_config.length; i++) {
    // console.log( global.answer_config[i] );
    // copy.push(answer_config[i]) agrega un item al array.
    
  }

  // try to send all answers.
// [{"answer":"1","feedback":"soy gay","questionTime":"2020-04-06 12:51:37","answerTime":"2020-04-06 12:51:00","userId":"c336f4a7-9263-446d-8fe5-77285260f19a","questionId":"2020-04-06 12:00:00 Smiles","version":"0.1","company":"Custom","department":"Everyone","questionType":"Smiles"}]

  fetch('http://emood.com.ar/api.php', {
    method: 'post',
    headers: {
      //'Accept': 'application/json, text/plain, */*',
      'Content-Type':'application/x-www-form-urlencoded'
    },
    // body: 'json=' + encodeURIComponent( JSON.stringify(global.answer_config) )
    body: 'json=' + encodeURIComponent( JSON.stringify(global.answer_config) 
    )
  }).then(function(response) {
        response.text().then(function( text ) {
          console.log("################################################################################");
        //  console.log(post_data);
          if ( text != "ok") {
            console.log("ERROR. Reply was not ok.")
          } else {
            store.set( 'answer_config', []  );
            global.answer_config = [];
          }
          console.log( text );
          console.log("################################################################################");
        });
      }).catch(err => {
      console.log("Connection Error... Sending Latter.");
    });



}



function ShowSmiles() {
    //console.log( global.now_hour +" - "+global.now_day+" / "+global.now_month +" / "+global.now_year  );
    //console.log(configuration["question_times"]);
    // question_days : [0,1,2,3,4,5,6],   [ global.weekday ]

    if ( global.configuration["question_times"].includes(global.now_hour) && global.configuration["question_days"].includes(global.weekday) ) {
      
      var last_answer_time = store.get('last_answer_time'); // CAMBIAR A TODAY ANSWERS
      if( last_answer_time == global.hourstamp || global.question_visible == true ) {
        console.log("You answered or are answering something else...");
        return;
      } else {
        console.log(" Hit Show Smiles!!! ");
        global.question_visible = true;
        // currentWindow = require('electron').remote.getCurrentWindow();
        global.questionId = global.hourstamp + " Smiles";
        global.this_questionType = "Smiles";
        store.set('last_answer_time', global.hourstamp  );
        global.mainWindow.show();
      }
    }
}


















const createWindow = () => {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 900,
    height: 400,
    frame: false,
    title: "E-Mood",
    icon: iconpath,
    show: false,
    transparent: true,
    resizable: false,
    webPreferences: {
         nodeIntegration: true //access node globals in browser windows
     }
  });

  global.mainWindow = mainWindow;

  if( global.developer_mode_window ) {
    mainWindow.webContents.openDevTools();
  }
  // Always on top
  mainWindow.setAlwaysOnTop(true);
  // and load the index.html of the app.
  mainWindow.loadFile( path.join(__dirname, 'index.html') );


// Autosatart
// https://www.electronjs.org/docs/api/app#appsetloginitemsettingssettings-macos-windows
const appFolder = path.dirname(process.execPath)
const updateExe = path.resolve(appFolder, '..', 'Update.exe')
const exeName = path.basename(process.execPath)

app.setLoginItemSettings({
  openAtLogin: true,
  path: updateExe,
  allowRendererProcessReuse: true,
  args: [
    '--processStart', `"${exeName}"`,
    '--process-start-args', `"--hidden"`
  ]
})




// JQUERY https://ourcodeworld.com/articles/read/202/how-to-include-and-use-jquery-in-electron-framework

// Tratando de que se cierre a un icono en el tray.
// var appIcon = new Tray(iconpath);
// var contextMenu = Menu.buildFromTemplate([
//     {
//         label: 'Show App', click: function () {
//             mainWindow.show();
//         }
//     },
//     {
//         label: 'Quit', click: function () {
//             app.isQuiting = true;
//             app.quit();
//         }
//     }
// ])
//
// appIcon.setContextMenu(contextMenu)

let tray = null
tray = new Tray(iconpath)
const contextMenu = Menu.buildFromTemplate([
      {
          label: 'Show App', click: function () {
              mainWindow.show();
          }
      },
      {
          label: 'Quit', click: function () {
              app.isQuiting = true;
              app.quit();
          }
      }
])
tray.setToolTip('This is my application.');
tray.setContextMenu(contextMenu);

//


  mainWindow.on('minimize',function(event){
      event.preventDefault();
      mainWindow.hide();
      global.question_visible = false;
  });

  mainWindow.on('close', function (event) {
      if( !app.isQuiting){
          event.preventDefault();
          mainWindow.hide();
          global.question_visible = false;
      }
      return false;
  });





// FIN de tratando






}; // fin createWindow










// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow);

// Quit when all windows are closed.
app.on('window-all-closed', () => {
  // On OS X it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  // On OS X it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }

});

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and import them here.
"""