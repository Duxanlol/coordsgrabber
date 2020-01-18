from tkinter import *
from PIL import ImageGrab, ImageTk, Image
import sys
import pyperclip

TEXT_OFFSET_X = 50
TEXT_OFFSET_X += 15
TEXT_OFFSET_Y = 50

if len(sys.argv)==2:
    img = Image.open(str(sys.argv[1]))    
else:
    img = ImageGrab.grabclipboard()
    
width, height = img.size
retval = str()
root = Tk()
root.title('coordsGrabber')
root.overrideredirect(True)
root.config(cursor="none")

saved = None
renew = False
die = False
mod_alt = False
mod_ctrl = False
mod_shift = False

img = ImageTk.PhotoImage(img)

def on_left_click(event):
    global retval
    print(event.x,event.y)
    retval = retval + str(event.x)+" "+str(event.y) + '\n'
    
def on_right_click(event):
    pyperclip.copy(retval)
    global die
    die = True
    
def on_middle_click(event):
    global mod_alt,mod_ctrl,mod_shift
    global saved
    global renew
    saved = dict()
    saved['x'] = event.x
    saved['y'] = event.y
    renew = True
    if mod_alt:
        saved = None
        renew = False

def on_mousewheel(event):
    global TEXT_OFFSET_X
    global TEXT_OFFSET_Y
    global mod_alt,mod_ctrl,mod_shift
    change = (event.delta/120) * (10 if mod_shift else 1)
    if mod_ctrl:
        TEXT_OFFSET_Y+= change
    elif mod_alt:
        TEXT_OFFSET_X+= change
    else:
        TEXT_OFFSET_X+= change
        TEXT_OFFSET_Y+= change
    
def key_up(event):
#    print(event.char, event.keysym + " UP " )
    global mod_alt, mod_ctrl, mod_shift
    if event.keysym == "Alt_L":
        mod_alt = False
    elif event.keysym == "Control_L":
        mod_ctrl = False
    elif event.keysym == "Shift_L":
        mod_shift = False
def key_down(event):
#    print(event.char, event.keysym + " DOWN " )
    global mod_alt, mod_ctrl, mod_shift
    if event.keysym == "Alt_L":
        mod_alt = True
    elif event.keysym == "Control_L":
        mod_ctrl = True
    elif event.keysym == "Shift_L":
        mod_shift = True

canvas = Canvas(root, width=width, height=height,highlightthickness=0)
canvas.bind("<Button-1>",on_left_click)
canvas.bind("<Button-2>",on_middle_click)
canvas.bind("<Button-3>",on_right_click)
canvas.bind("<MouseWheel>",on_mousewheel)
root.bind("<KeyPress>",key_down)
root.bind("<KeyRelease>",key_up)
canvas.pack(fill='both', expand=1)
canvas.create_image(0,0,anchor=NW,image=img)

x = root.winfo_pointerx()
y = root.winfo_pointery()
saved_line = None
current_line = dict()
current_line['x_line'] = canvas.create_line(0,0,0,0,fill='red')
current_line['y_line'] = canvas.create_line(0,0,0,0,fill='red')
current_line['text']   = canvas.create_text(0, 0,fill='red', text='')
saved_line = dict()
saved_line['x_line'] = canvas.create_line(0,0,0,0,fill='blue')
saved_line['y_line'] = canvas.create_line(0,0,0,0,fill='blue')

while(not die):
    x = root.winfo_pointerx()
    y = root.winfo_pointery()
    canvas.coords(current_line['x_line'] ,x,0,x,height)
    canvas.coords(current_line['y_line'] ,0,y,width,y)
    canvas.coords(current_line['text'], x+TEXT_OFFSET_X, y-TEXT_OFFSET_Y)
    if renew:
        if saved_line is None:
            saved_line = dict()
        canvas.coords(saved_line['x_line'] ,saved['x'],0,saved['x'],height)
        canvas.coords(saved_line['y_line'] ,0,saved['y'],width,saved['y'])
        renew = False
    if saved is None:
        canvas.itemconfig(current_line['text'], text=str(x)+" "+str(y))
        canvas.coords(saved_line['x_line'] ,0,0,0,0)
        canvas.coords(saved_line['y_line'] ,0,0,0,0)
    else:
        canvas.itemconfig(current_line['text'], text=str(x)+" "+str(y)+'\n'+str(x-saved['x'])+" "+str(y-saved['y'])) 
        
    root.update_idletasks()
    root.update()        

