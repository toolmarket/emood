#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import *


# LOCAL GLOBALS
background_color = '#091337'
#background_color = '#333333'
window_width = 600
window_height = 300
move_up = 100 # movemos la ventana unos pixeles para arriba.

def configure_window(window_type="default"):
    """ DEFAULT WINDOW TEMPLATE """
    os.chdir( path  )
    window = tk.Tk()
    window.title("E-Mood v." + version )
    window.configure(background=background_color)
    #window.overrideredirect(1) # Remove border
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

def save_answer(window,score,inputValue,questionId="DefaultId",questionType="Default"):
    print(score,inputValue,questionId,questionType)
    window.destroy()
    pass


# gui_generator(type=0,main_text="¿Cómo te sentís?",questionId="DefaultId",questionType="Default",data=0):
def smiles(main_text="¿Cómo te sentís?",questionId="DefaultId"): #questionID,ETC.   
    """ CUSTOM WINDOW CREATION """
    # SET UP WINDOW.
    window = configure_window()
    questionType="Smiles"

    try:
        sad_img = tk.PhotoImage(file="src/sad.png")
        neutral_img = tk.PhotoImage(file="src/neutral.png")
        smile_img = tk.PhotoImage(file="src/smile.png")      
    except:
        sad_img = tk.PhotoImage(file="src/happy.gif")
        neutral_img = tk.PhotoImage(file="src/neutral.gif")
        smile_img = tk.PhotoImage(file="src/smile.gif")

    inputValue = ""

    #  First Step
    def show_first():
        #background_color = "#FF00FF"
        main_title = tk.Label(window, text = main_text, fg="#FFFFFF", font='Sans 20', background=background_color) # , anchor="center"
        main_title.grid(row=1,column=1,columnspan=12,pady=30,stick="WENS")

        sad_face = tk.Button(window, text='', width=120,height=120,cursor="hand2",border=0,background=background_color,image = sad_img,
         highlightbackground=background_color,
         highlightcolor=background_color,
         borderwidth=0,
         bd=0,
         padx=0,
         pady=0,
         bg="#FF00FF",
         fg="#FF0000",
         relief="flat",
         highlightthickness=0,
         
         command=lambda: show_input("¿Quieres contarnos por que?",-1) )
        sad_face.grid(row=2,columnspan=1,column=4,pady=0,padx=5,stick="WENS") # ,padx=20,pady=20

        neutral_face = tk.Button(window, text='', width=120,height=120,cursor="hand2",border=0,background=background_color,image = neutral_img,
         command=lambda: show_input("¿Queres contarnos algo?",0) )
        neutral_face.grid(row=2,columnspan=1,column=8,pady=0,padx=60,stick="WENS")

        smile_face = tk.Button(window, text='', width=120,height=120,cursor="hand2",border=0,background=background_color,image = smile_img,
         command=lambda: show_input("¿Queres contarnos por que?",1) )
        smile_face.grid(row=2,columnspan=1,column=9,pady=0,padx=0,stick="WENS")

    # Second Step
    def show_input(main_text="default text",score=0):
        clear_grid(window)
        # score var

        main_title = tk.Label(window, text = main_text, fg="#FFFFFF", font='Sans 20', background=background_color) # , anchor="center"
        main_title.grid(row=0,column=1,columnspan=12,pady=20,stick="WENS")

        textBox = tk.Text(window, width=50,height=6)
        textBox.grid(row=2,column=1,columnspan=12,padx=0,pady=0,stick="S")

        ok_button = tk.Button(window, text='Cancelar', font='Sans 20', width=10,height=1,cursor="hand2",border=0,
         command=lambda: save_answer(window,score,inputValue) )
        ok_button.grid(row=12,column=8,pady=20,columnspan=1,padx=70)
        
        no_button = tk.Button(window, text='Enviar 😄', font='Sans 20', width=10,height=1,cursor="hand2",border=0,
         highlightbackground=background_color,
         highlightcolor=background_color,
         borderwidth=0,
         bd=0,
         padx=0,
         pady=0,
         bg="#FF00FF",
         fg="#FF0000",
         relief="flat",
         highlightthickness=0,
         command=lambda: save_answer(window,score,inputValue) )
        no_button.grid(row=12,column=12,pady=20,columnspan=1,padx=20)


        def input_keyup(data):
            global inputValue
            print(data.keycode)
            inputValue= textBox.get("1.0","end-1c").strip()
            if len(inputValue) > 1:
                # send_button.config(text='Enviar')
                pass
            else:
                # send_button.config(text='No')
                pass
            if(data.keycode == 13): # Enter ahora envia el formulario.
                save_answer(window,score,inputValue) # inputValue, score
        window.bind_all('<KeyRelease>', input_keyup)

        ### send answer and close.

    show_first()
    #window.update()
    window.mainloop()







smiles()


exit()
