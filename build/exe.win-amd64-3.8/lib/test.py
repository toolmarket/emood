import tkinter as tk
from PIL import Image


# Tkinter GUI
def gui_generator(type=0,main_text="¿Cómo te sentís?",questionId="DefaultId",questionType="Default",data=0):
    """ Creates the windows """
    #path = os.path.dirname( os.path.abspath(__file__) )
    #os.chdir( path ) # Cambiar el workingdir a dode esta este script(los threads se pierden un poco si no)

    window = tk.Tk()
    window.title("E-Mood v. test" ) )
    window_width = 600
    window_height = 300
    move_up = 100 # movemos la ventana unos pixeles para arriba.
    background_color = '#091337'
    background_color = '#091337'
    window.configure(background=background_color)
    window.overrideredirect(1) # Remove border
    window.grid_rowconfigure(3, weight=1)
    window.grid_columnconfigure(3, weight=1)


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

gui_generator(3,"emood test")