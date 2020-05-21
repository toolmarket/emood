import tkinter as tk
from PIL import Image


# Tkinter GUI
def gui_generator(type=0,main_text="¿Cómo te sentís?",questionId="DefaultId",questionType="Default",data=0):
    """ Creates the windows """
    window = tk.Tk()
    window.title("E-Mood v.Test" )
    window_width = 600
    window_height = 300
    move_up = 100 # movemos la ventana unos pixeles para arriba.
    background_color = '#091337'
    background_color = '#091337'
    window.configure(background=background_color)
    window.overrideredirect(1) # Remove border
    window.grid_rowconfigure(3, weight=1)
    window.grid_columnconfigure(3, weight=1)

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()  
    window.geometry("%dx%d+%d+%d" % (window_width, window_height,screen_width/2-window_width/2, screen_height/2-window_height/2 - move_up)) 

    tk.Label(window, text = main_text, fg="#FFFFFF", font='Sans 20', background=background_color).grid(row=0,column=0,columnspan=9,pady=20)   # Helvetica
    img1 = tk.PhotoImage(file="src/sad.png")
    img2 = tk.PhotoImage(file="src/neutral.png")
    img3 = tk.PhotoImage(file="src/smile.png")
    tk.Button(window, text='', width=150,height=120,cursor="hand2",border=0,background=background_color,image = img1, command=window.destroy ).grid(row=2,column=1,pady=20,padx=20)
    tk.Button(window, text='', width=150,height=120,cursor="hand2",border=0,background=background_color,image = img2, command=window.destroy ).grid(row=2,column=3,pady=20)
    tk.Button(window, text='', width=150,height=120,cursor="hand2",border=0,background=background_color,image = img3, command=window.destroy ).grid(row=2,column=6,pady=20,padx=20)

    window.iconbitmap('src/logo.ico')
    window.resizable(0, 0) # Can't Resize
    window.lift(aboveThis=window) 
    # window.wm_attributes("-alpha",0.3) # -notify https://wiki.tcl-lang.org/page/wm+attributes
    window.wm_attributes("-topmost", 1) # always on top
    window.mainloop() #bloquea la ejecución del script.


gui_generator()