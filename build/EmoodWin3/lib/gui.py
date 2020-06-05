# The purpose of this file to hold everything related to creating and showin GUIs
from config import *

# LOCAL GLOBALS
background_color = '#000b35'
#background_color = '#333333'
window_width = 600
window_height = 300
move_up = 100 # movemos la ventana unos pixeles para arriba.

def configure_window(window_type="default",window_width=600,window_height=300):
    """ DEFAULT WINDOW TEMPLATE """
    os.chdir( path  )
    window = tk.Tk()
    window.title("E-Mood v." + version )
    window.configure(background=background_color)
    window.overrideredirect(1) # Remove border
    window.grid_rowconfigure(12, weight=1)
    window.grid_columnconfigure(12, weight=1)
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()  
    window.geometry("%dx%d+%d+%d" % (window_width, window_height,screen_width/2-window_width/2, screen_height/2-window_height/2 - move_up)) 
    window.iconbitmap('src/logo.ico')
    window.resizable(0, 0) # Can't Resize
    window.lift(aboveThis=window) 
    window.wm_attributes("-topmost", 1) # always on top
    window.focus_force() # le da foco a la ventana   
    return window

def clear_grid(window):
    """ Clear everything in Grid"""
    for label in window.grid_slaves():
        # if int(label.grid_info()["row"]) > 6:
        # find grid "hide all"
        #main_title.configure(text='OUCH!')
        #sad_face.grid_remove()
        # grid()
        label.grid_forget()    

def run_action(window,action=False):
    """ Run Custom Action (open website) This could create security issues."""
    if( action ):    
        if windows:
            os.startfile(action)
        else:
            try:
                subprocess.Popen(['open', action])
            except:
                subprocess.Popen(['xdg-open', action])
    window.destroy()


def save_answer(window,score,inputValue,questionId="DefaultId",questionType="Default",questionTime="unknown"):
    """ SAVE DATA TO SHELVE """
    print(score,inputValue,questionId,questionType)

    datos = shelve.open('src/data.db') # Abrimos la base de datos para guardar la respuesta.
    
    answerTime = time.strftime("%Y-%m-%d %H:%M:%S")
    print(inputValue, questionId)
    #datos.setdefault('unsentAnswers', []) # list.append()
    new_data = {
        "answerTime": answerTime,
        "questionTime": questionTime,
        "userId": datos["userId"],
        "questionId": questionId,
        "version": datos["version"],
        "company": datos["company"],
        "feedback": inputValue,
        "answer": score,
        "department": datos["department"],
        "questionType": questionType,
    }
    
    unsentAnswers = datos['unsentAnswers']
    unsentAnswers.append(new_data)
    datos['unsentAnswers'] = unsentAnswers
    for answer in datos['unsentAnswers']:
        print ( answer )

    datos.close() # Cerrando la base
    # Quizas la podemos guardar y meter en el loop siguiente de "envio de respuestas". Pero necesitamos un ID para la pregunta. 
    window.destroy()





# GUI TEMPLATES

# gui_generator(type=0,main_text="¿Cómo te sentís?",questionId="DefaultId",questionType="Default",data=0):
def smiles(main_text="¿CÓMO TE SENTÍS?",questionId="DefaultId"): #questionID,ETC.   
    """ CUSTOM WINDOW CREATION """
    # SET UP WINDOW.

    window = configure_window()
    questionType="Smiles"
    questionTime = time.strftime("%Y-%m-%d %H:%M:%S")

    sad_img = tk.PhotoImage(file="src/sad.gif")
    neutral_img = tk.PhotoImage(file="src/neutral.gif")
    smile_img = tk.PhotoImage(file="src/smile.gif")

    inputValue = ""

    #  First Step
    def show_first():
        #background_color = "#FF00FF"
        main_title = tk.Label(window, text = main_text, fg="#FFFFFF", font='Sans 20', background=background_color) # , anchor="center"
        main_title.grid(row=1,column=1,columnspan=12,pady=30,stick="WENS")

        sad_face = tk.Label(window, text='', width=120,height=120,cursor="hand2",image = sad_img,border=0,background=background_color )
        sad_face.grid(row=2,columnspan=1,column=1,pady=0,padx=15,stick="WENS") # ,padx=20,pady=20

        neutral_face = tk.Label(window, text='', width=120,height=120,cursor="hand2",image = neutral_img,border=0,background=background_color )
        neutral_face.grid(row=2,columnspan=1,column=6,pady=0,padx=80,stick="WENS")

        smile_face = tk.Label(window, text='', width=120,height=120,cursor="hand2",image = smile_img,border=0,background=background_color )
        smile_face.grid(row=2,columnspan=1,column=12,pady=0,padx=0,stick="WENS")

        #ACTIONS
        sad_face.bind('<Button-1>', lambda event, text="¿QUIERES CONTARNOS POR QUE?",score=-1: show_input(text,score) )
        neutral_face.bind('<Button-1>', lambda event, text="¿QUIERES CONTARNOS POR QUE?",score=0: show_input(text,score) )
        smile_face.bind('<Button-1>', lambda event, text="¿QUIERES CONTARNOS POR QUE?",score=1: show_input(text,score) )

    # Second Step
    def show_input(main_text="default text",score=0):
        clear_grid(window)
        # score var

        main_title = tk.Label(window, text = main_text, fg="#FFFFFF", font='Sans 20', background=background_color) # , anchor="center"
        main_title.grid(row=0,column=1,columnspan=12,pady=20,stick="WENS")

        textBox = tk.Text(window, width=50,height=6)
        textBox.grid(row=2,column=1,columnspan=12,padx=0,pady=0,stick="S")

        ok_button = tk.Button(window, text='Cancelar', font='Sans 20', width=10,height=1,cursor="hand2",border=0,
         command=lambda: save_answer(window,score,inputValue,questionId,questionType,questionTime) )
        ok_button.grid(row=12,column=8,pady=20,columnspan=1,padx=70)
        
        no_button = tk.Button(window, text='Enviar', font='Sans 20', width=10,height=1,cursor="hand2",border=0,
         command=lambda: save_answer(window,score,inputValue,questionId,questionType,questionTime) )
        no_button.grid(row=12,column=12,pady=20,columnspan=1,padx=20)

        def input_keyup(data):
            global inputValue
            #print(data.keycode)
            inputValue= textBox.get("1.0","end-1c").strip()
            if(data.keycode == 13): # Enter ahora envia el formulario.
                save_answer(window,score,inputValue,questionId,questionType,questionTime) # inputValue, score
        
        window.bind_all('<KeyRelease>', input_keyup)

        ### send answer and close.

    show_first()
    #window.update()
    window.mainloop()










#Mostrar titulo con un subtexto.
def show_text(main_text="Titulo",secondary_text="Esto es más texto.",button_1="Cerrar",button_action=False,close_option=False): #questionID,ETC.   
    window = configure_window(window_type="default",window_width=600,window_height=400)
    main_title = tk.Label(window, text = main_text, fg="#FFFFFF", font='Sans 16', background=background_color,wraplength=600) # , anchor="center"
    main_title.grid(row=1,column=1,columnspan=12,pady=30,stick="WENS")

    main_text = tk.Label(window, text = secondary_text, fg="#FFFFFF", font='Sans 12', background=background_color,wraplength=600) # , anchor="center"
    main_text.grid(row=2,column=1,columnspan=12,rowspan=5,pady=30,stick="WENS")

    ok_button = tk.Button(window, text=button_1, font='Sans 16', width=10,height=1,cursor="hand2",border=0,
        command=lambda: run_action(window,button_action) )
    no_button = tk.Button(window, text=close_option, font='Sans 16', width=10,height=1,cursor="hand2",border=0,
        command=window.destroy )


    if close_option:
        no_button.grid(row=12,column=8,pady=20,columnspan=1,padx=70)
        ok_button.grid(row=12,column=12,pady=20,columnspan=1,padx=20)
    else:
        ok_button.grid(row=12,column=1,pady=20,columnspan=12,padx=0)

    # no_button = tk.Button(window, text='Enviar', font='Sans 20', width=10,height=1,cursor="hand2",border=0,
    #     command=lambda: save_answer(window,score,inputValue,questionId,questionType,questionTime) )
    # no_button.grid(row=12,column=12,pady=20,columnspan=1,padx=20)



    window.mainloop()






















































































def test():
    win = tk.Tk()
    max_amount = 0
    label1 = None #just so it is defined

    def fun():
        global max_amount, label1
        max_amount +=100
        label1.configure(text='Balance :$' + str(max_amount))

    btn = tk.Button(win,text = 'Change', command = fun)
    btn.grid()
    t1 =str(max_amount)
    label1 = tk.Label(win,text = 'Balance :$' + t1)
    label1.grid()

    win.mainloop()

def test2():
    def toggle():
        if mylabel.visible:
            btnToggle["text"] = "Show Example"
            print ("Now you don't")
            mylabel.place_forget()
        else:
            mylabel.place(mylabel.pi)
            print ("Now you see it")
            btnToggle["text"] = "Hide Example"
        mylabel.visible = not mylabel.visible

    root = tk.Tk()

    print ("TkVersion", tk.TkVersion)
    print ("TclVersion", tk.TclVersion)
    print ("Python version", sys.version_info)

    mylabel = tk.Label(text="Example")
    mylabel.visible = True
    mylabel.place(x=20, y=50)
    mylabel.pi = mylabel.place_info()

    btnToggle = tk.Button(text="Hide Example", command=toggle)
    btnToggle.place(x=70, y=150)
    root.mainloop()






































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
        pass # Error en linux.
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




# Tkinter GUI
def gui_generator(type=0,main_text="¿Cómo te sentís?",questionId="DefaultId",questionType="Default",data=0):
    """ Creates the windows """
    config = shelve.open('src/data.db') 
    window = tk.Tk()
    window.title("E-Mood v." + str( version ) )
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

        try:
          img1 = tk.PhotoImage(file="src/sad.png")
          img2 = tk.PhotoImage(file="src/neutral.png")
          img3 = tk.PhotoImage(file="src/smile.png")
        except: # Quizas para MAC o algo
          img1 = tk.PhotoImage(file="src/sad.gif")
          img2 = tk.PhotoImage(file="src/neutral.gif")
          img3 = tk.PhotoImage(file="src/smile.gif")

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



