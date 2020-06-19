#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
    if windows:
        window.overrideredirect(1) # Remove border
    window.grid_rowconfigure(12, weight=1)
    window.grid_columnconfigure(12, weight=1)
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()  
    window.geometry("%dx%d+%d+%d" % (window_width, window_height,screen_width/2-window_width/2, screen_height/2-window_height/2 - move_up)) 
    try:
        window.iconbitmap('src/logo.ico') # TODO #2 hacer que se vea en mac
    except:
        pass #Error en linux
    window.resizable(0, 0) # Can't Resize
    window.lift(aboveThis=window) 
    window.wm_attributes("-topmost", -1) # always on top
    window.focus_force() # le da foco a la ventana   
    #window.after(4, lambda: window.focus_force())
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
    print(new_data)
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

    sad_img2 = tk.PhotoImage(file="src/sad2.gif")
    neutral_img2 = tk.PhotoImage(file="src/neutral2.gif")
    smile_img2 = tk.PhotoImage(file="src/smile2.gif")

    inputValue = ""
    if windows:
        mouse_pointer = "hand2"
    else:
        mouse_pointer = "pointinghand"

    #  First Step
    def show_first():
        #background_color = "#FF00FF"
        main_title = tk.Label(window, text = main_text, fg="#FFFFFF", font=('Sans', 28, 'bold'), background=background_color) # , anchor="center"
        main_title.grid(row=1,column=1,columnspan=12,pady=30,stick="WENS") #cambie tipografia

        sad_face = tk.Label(window, text='', width=120,height=120,cursor=mouse_pointer,image = sad_img,border=0,background=background_color )
        sad_face.grid(row=2,columnspan=1,column=1,pady=0,padx=15,stick="WENS") # ,padx=20,pady=20 cursor="hand2" (anterior)

        neutral_face = tk.Label(window, text='', width=120,height=120,cursor=mouse_pointer,image = neutral_img,border=0,background=background_color )
        neutral_face.grid(row=2,columnspan=1,column=6,pady=0,padx=80,stick="WENS")

        smile_face = tk.Label(window, text='', width=120,height=120,cursor=mouse_pointer,image = smile_img,border=0,background=background_color )
        smile_face.grid(row=2,columnspan=1,column=12,pady=0,padx=0,stick="WENS")

        #ACTIONS
        sad_face.bind('<Button-1>', lambda event, text="¿QUERÉS CONTARNOS POR QUÉ?",score=-1: show_input(text,score) )
        sad_face.bind("<Enter>", lambda e, y=sad_img2: e.widget.config(image=y) )
        sad_face.bind("<Leave>", lambda e, y=sad_img: e.widget.config(image=y) )
        # https://stackoverflow.com/questions/16665155/python-tkinter-label-widget-mouse-over
        #sad_face.bind("<Enter>", lambda e, x=x: e.widget.config(text=x))
        #sad_face.bind("<Leave>", lambda e, i=i: e.widget.config(text="Label "+str(i)))
       
        neutral_face.bind('<Button-1>', lambda event, text="¿QUERÉS CONTARNOS POR QUÉ?",score=0: show_input(text,score) )
        neutral_face.bind("<Enter>", lambda e, y=neutral_img2: e.widget.config(image=y) )
        neutral_face.bind("<Leave>", lambda e, y=neutral_img: e.widget.config(image=y) )
        
        smile_face.bind('<Button-1>', lambda event, text="¿QUERÉS CONTARNOS POR QUÉ?",score=1: show_input(text,score) )
        smile_face.bind("<Enter>", lambda e, y=smile_img2: e.widget.config(image=y) )
        smile_face.bind("<Leave>", lambda e, y=smile_img: e.widget.config(image=y) )  #puse imagen de sustitucion


    # Second Step
    def show_input(main_text="default text",score=0):
        global inputValue
        clear_grid(window)
        # score var

        try:
            inputValue
        except:
            inputValue = ""

        main_title = tk.Label(window, text = main_text, fg="#FFFFFF", font=('Sans', 25, 'bold'), background=background_color) # , anchor="center"
        main_title.grid(row=0,column=1,columnspan=12,pady=20,stick="WENS")  #cambie tipografia

        textBox = tk.Text(window, width=50,height=8)        
        textBox.grid(row=2,column=1,columnspan=12,padx=0,pady=2,stick="S")

        ok_button = tk.Button(window, text='CANCELAR', font=('Sans', 15, 'bold'), width=10,height=1,cursor=mouse_pointer,border=0, highlightbackground="#000b35",
         command=lambda: save_answer(window,score,inputValue,questionId,questionType,questionTime) )
        ok_button.grid(row=12,column=6,pady=20,columnspan=1,padx=100) #cambie botones y cursor
        
        no_button = tk.Button(window, text='ENVIAR', font=('Sans', 15, 'bold'), width=10,height=1,cursor=mouse_pointer,border=0, highlightbackground="#000b35",
         command=lambda: save_answer(window,score,inputValue,questionId,questionType,questionTime) )
        no_button.grid(row=12,column=10,pady=20,columnspan=1,padx=42)

        def input_keyup(data):
            global inputValue
            #print(data.keycode)
            inputValue= textBox.get("1.0","end-1c").strip()
            print(inputValue)
            if(data.keycode == 13): # Enter ahora envia el formulario.
                save_answer(window,score,inputValue,questionId,questionType,questionTime) # inputValue, score
        
        window.bind_all('<KeyRelease>', input_keyup)

        ### send answer and close.

    show_first()
    #window.after(1000, lambda: window.focus_force())
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




































