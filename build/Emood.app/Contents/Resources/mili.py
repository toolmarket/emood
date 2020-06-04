#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import *


# LOCAL GLOBALS
background_color = '#000b35'
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
def smiles(main_text="¿CÓMO TE SENTÍS?",questionId="DefaultId"): #questionID,ETC.   
    """ CUSTOM WINDOW CREATION """
    # SET UP WINDOW.
    window = configure_window()
    questionType="Smiles"

    sad_img = tk.PhotoImage(file="src/sad.gif")
    neutral_img = tk.PhotoImage(file="src/neutral.gif")
    smile_img = tk.PhotoImage(file="src/smile.gif")

    inputValue = ""

    #  First Step
    def show_first():
        #background_color = "#FF00FF"
        main_title = tk.Label(window, text = main_text, height=1, fg="#FFFFFF", font=('Sans', 28, 'bold'), background=background_color) # , anchor="center"
        main_title.grid(row=1,column=1,columnspan=12,pady=40,stick="WENS")

        sad_face = tk.Label(window, text='', width=120,height=120,cursor="hand2",image = sad_img,border=0,background=background_color )
        sad_face.grid(row=2,columnspan=1,column=1,pady=0,padx=15,stick="WENS") # ,padx=20,pady=20

        neutral_face = tk.Label(window, text='', width=120,height=120,cursor="hand2",image = neutral_img,border=0,background=background_color )
        neutral_face.grid(row=2,columnspan=1,column=6,pady=0,padx=80,stick="WENS")

        smile_face = tk.Label(window, text='', width=120,height=120,cursor="hand2",image = smile_img,border=0,background=background_color )
        smile_face.grid(row=2,columnspan=1,column=12,pady=0,padx=0,stick="WENS")

        #ACTIONS
        sad_face.bind('<Button-1>', lambda event, text="¿QUERÉS CONTARNOS POR QUÉ?",score=-1: show_input(text,score) )
        neutral_face.bind('<Button-1>', lambda event, text="¿QUERÉS CONTARNOS POR QUÉ?",score=0: show_input(text,score) )
        smile_face.bind('<Button-1>', lambda event, text="¿QUERÉS CONTARNOS POR QUÉ?",score=1: show_input(text,score) )

    # Second Step
    def show_input(main_text="default text",score=0):
        clear_grid(window)
        # score var

        main_title = tk.Label(window, text = main_text, fg="#FFFFFF", font=('Sans', 25, 'bold'), background=background_color) # , anchor="center"
        main_title.grid(row=0,column=1,columnspan=12,pady=20,stick="WENS")

        textBox = tk.Text(window, width=50,height=6,)
        textBox.grid(row=2,column=1,columnspan=12,padx=0,pady=0,stick="S")

        ok_button = tk.Button(window, text='CANCELAR', font='Sans 15 bold', width=10,height=1, cursor="hand", border=0, highlightbackground="#000b35",
         command=lambda: save_answer(window,score,inputValue) )
        ok_button.grid(row=12,column=8,pady=20,columnspan=1,padx=70)
        
        no_button = tk.Button(window, text='ENVIAR', font='Sans 15 bold', width=10,height=1,cursor="hand",border=0,
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
