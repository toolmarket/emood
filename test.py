import tkinter as tk
from PIL import Image
import sys

windows = False
if sys.platform.startswith('win'):
  windows = True


# Tkinter GUI

def gui_generator(type=0,main_text="¿Cómo te sentís?",questionId="DefaultId",questionType="Default",data=0):
    """ Creates the windows """
    window = tk.Tk()
    window.title("E-Mood v. test" )
    window_width = 600
    window_height = 300
    move_up = 100 # movemos la ventana unos pixeles para arriba.
    background_color = '#091337'
    window.configure(background=background_color)
    #window.overrideredirect(1) # Remove border
    window.grid_rowconfigure(3, weight=1)
    window.grid_columnconfigure(3, weight=1)
    window.iconbitmap('src/logo.ico')

    if windows:
        mousecursor = "hand2"
    else:
        mousecursor = "pointinghand"


    # Botones de Acciones dentro del GUI. 
    def btn_next(datos=0):
        print(datos)
        window.destroy()

        if datos == -1:
            gui_generator(1,"¿Por qué estas mal?",questionId,questionType,datos)
        if datos == 0:
            gui_generator(1,"¿Queres dejar un Comentario?,",questionId,questionType,datos)
        if datos == 1:
            gui_generator(1,"¿Queres contar por qué?",questionId,questionType,datos)

    def save_answer(data=0):
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
        tk.Label(window, text = main_text, fg="#FFFFFF", font='Sans 30', background=background_color).grid(row=1, column=0, columnspan=9,pady=25)   # Helvetica
        if windows:
            img1 = tk.PhotoImage(file="src/sad.png")
            img2 = tk.PhotoImage(file="src/neutral.png")
            img3 = tk.PhotoImage(file="src/smile.png")
        else:
            img1 = tk.PhotoImage(file="src/sad.gif")
            img2 = tk.PhotoImage(file="src/neutral.gif")
            img3 = tk.PhotoImage(file="src/smile.gif")            
       
        tk.Button(window, 
            text='', 
            width=120,
            height=120,
            cursor="arrow",
            border=0, 
            highlightbackground="#091337",
            highlightcolor='#091337', 
            background='#091337',
            image = img1, 
            command=lambda: btn_next(-1) ).grid(row=2,column=1,pady=20,padx=50)
        tk.Button(window, text='', width=120,height=120,cursor="arrow",border=0,highlightbackground='#091337', background=background_color,image = img2, command=lambda: btn_next(0) ).grid(row=2,column=3,pady=20)
        tk.Button(window, text='', width=120,height=120,cursor="arrow",border=0,highlightbackground='#091337', background=background_color,image = img3, command=lambda: btn_next(1) ).grid(row=2,column=6,pady=20,padx=50)

    if type == 1: # INPUT TEXT
        tk.Label(window, text = main_text, fg="#FFFFFF", font='Sans 25', background=background_color).grid(row=0,column=0,columnspan=9,pady=15)   # Helvetica
        textBox = tk.Text(window, width=60,height=6)
        textBox.grid(row=2,column=0,columnspan=9,pady=15)
        send_button = tk.Button(window, text='No', font='Sans 20', width=15,height=1,cursor="hand2",border=0, command=lambda: save_answer() )
        send_button.grid(row=3,column=3,pady=10,padx=15)
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
        tk.Label(window, text = main_text, fg="#FFFFFF", font='Sans 26', background=background_color,wraplength=500,justify="center").grid(row=0,column=0,rowspan=2,columnspan=9,pady=50,padx=20)   # Helvetica
        
        tk.Button(window, text='Ok', font='Sans 20', width=10,height=1,bd=0,background=background_color,cursor=mousecursor,border=0,highlightthickness=0,padx=0,pady=0,relief="flat", command=window.destroy ).grid(row=3,column=3,pady=20,padx=20)
       # tk.Button(window, text='Cancelar', font='Sans 20', width=10,height=1,cursor="hand2",border=0, command=window.destroy ).grid(row=3,column=2,pady=20,padx=20)
        window.focus_force() # le da foco a la ventana
        # https://www.google.com/search?q=tk+python+mac+button+border


    window.iconbitmap('src/logo.ico')
    window.resizable(0, 0) # Can't Resize
    window.lift(aboveThis=window) 
    # window.wm_attributes("-alpha",0.3) # -notify https://wiki.tcl-lang.org/page/wm+attributes
    window.wm_attributes("-topmost", 1) # always on top
    window.mainloop() #bloquea la ejecución del script.



def test(texto_largo):
    window = tk.Tk()
    window_width = 600
    window_height = 300
    move_up = 100
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()  
    window.geometry("%dx%d+%d+%d" % (window_width, window_height,screen_width/2-window_width/2, screen_height/2-window_height/2 - move_up)) 

    window.grid_rowconfigure(3, weight=1)
    window.grid_columnconfigure(3, weight=1)
    titulo = tk.Label(window, text = texto_largo)
    titulo.grid(row=0,column=0,rowspan=2,columnspan=9,pady=20,padx=20)

    window.wm_attributes("-topmost", 1)
    window.lift(aboveThis=window)
    window.focus_force()

    window.mainloop()



#test("adfa dfas dfasd fasd fasdf ")

gui_generator(0,"CONTANOS QUÉ ES LO QUE SUCEDE")
