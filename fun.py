# The purpose of this file is to have long complex or bothersome functions.
from config import *

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
      config["questions_answered"] = ""
      config['unsentAnswers'] = []
  config["department"] = "default"
  config["company"] = ini['defaults']['CompanyName']
  config["show_smiles"] = ini['defaults']['SurveyTimes']

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