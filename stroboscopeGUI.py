import tkinter as tk
from tkinter import messagebox as tkm
import serial
from tkinter import *
from tkinter.ttk import *
import tempfile

class ResizingCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event):
        wscale = float(event.width) / self.width
        hscale = float(event.height) / self.height
        self.width = event.width
        self.height = event.height 
        self.config(width=self.width, height=self.height)
        self.scale("all", 0, 0, wscale, hscale)

class MainApplication:

    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=450, height=600)

        self.frame = tk.Frame(master, bg='white')
        self.frame_gen_inf = tk.Frame(self.frame, bd='10', padx=3, pady=3)                                 

        # Pulse Width 
        self.label_PulseWidth = tk.Label(self.frame_gen_inf, text='Pulse width',
                                       bd='3', font='Helvetica 12 bold')

        PulseWidth_def = tk.StringVar(self.frame, value='1.00')   

        self.PulseWidth = tk.Entry(self.frame_gen_inf, bd='3',      
                                       justify="center", textvariable=PulseWidth_def)

        self.label_PulseWidth.place(relx=0.055, rely=0.05,  relwidth=0.3,
                                  relheight=0.1)
        self.PulseWidth.place(relx=0.355, rely=0.05, relwidth=0.15,
                                  relheight=0.1)
    
        self.label_warning = tk.Label(self.frame_gen_inf, text='Maximum 3 digits and 2 decimal places',
                                       bd='3', font='Helvetica 8')
        self.label_warning.place(relx=0.075, rely=0.15,  relwidth=0.5,
                                  relheight=0.05)

        self.label_units = tk.Label(self.frame_gen_inf, text='μs',
                                       bd='3', font='Helvetica 10')
        self.label_units.place(relx=0.53, rely=0.07,  relwidth=0.05,
                                  relheight=0.05)

        # Inter Pulse Width
        self.label_InterPulseWidth = tk.Label(self.frame_gen_inf, text='Inter pulse width',
                                       bd='3', font='Helvetica 12 bold')

        InterPulseWidth_def = tk.StringVar(self.frame, value='1.00')

        self.InterPulseWidth = tk.Entry(self.frame_gen_inf, bd='3',
                                       justify="center", textvariable=InterPulseWidth_def)

        self.label_InterPulseWidth.place(relx=0.095, rely=0.3,  relwidth=0.3,
                                  relheight=0.1)
        self.InterPulseWidth.place(relx=0.445, rely=0.3,  relwidth=0.15,
                                  relheight=0.1)

        self.label_warning2 = tk.Label(self.frame_gen_inf, text='Maximum 3 digits and 2 decimal places',
                                       bd='3', font='Helvetica 8')
        self.label_warning2.place(relx=0.075, rely=0.4,  relwidth=0.5,
                                  relheight=0.05)
        
        self.label_units2 = tk.Label(self.frame_gen_inf, text='μs',
                                       bd='3', font='Helvetica 10')
        self.label_units2.place(relx=0.62, rely=0.32,  relwidth=0.05,
                                  relheight=0.05)

        #N Pulses
        self.label_nPulses= tk.Label(self.frame_gen_inf, text='Number of pulses',
                                       bd='3', font='Helvetica 12 bold')

        nPulses_def = tk.StringVar(self.frame, value='1')
        self.nPulses = tk.Entry(self.frame_gen_inf, bd='3',
                                       justify="center", textvariable=nPulses_def)

        self.label_nPulses.place(relx=0.025, rely=0.54,  relwidth=0.3,
                                  relheight=0.1)
        self.nPulses.place(relx=0.325, rely=0.54,  relwidth=0.15,
                                  relheight=0.1)

        self.label_warning3 = tk.Label(self.frame_gen_inf, text='Maximum 2 digits',
                                       bd='3', font='Helvetica 8')
        self.label_warning3.place(relx=0.095, rely=0.64,  relwidth=0.2,
                                  relheight=0.05)
    
        # Initial pulse shift 
        self.label_InitShift= tk.Label(self.frame_gen_inf, text='Initial pulse shift',
                                       bd='3', font='Helvetica 12 bold')

        InitShift_def = tk.StringVar(self.frame, value='1.00')
        self.InitShift = tk.Entry(self.frame_gen_inf, bd='3',
                                       justify="center", textvariable=InitShift_def)

        self.label_InitShift.place(relx=0.085, rely=0.75,  relwidth=0.5,
                                  relheight=0.1)
        self.InitShift.place(relx=0.65, rely=0.75,  relwidth=0.15,
                                  relheight=0.1)

        self.label_warning4 = tk.Label(self.frame_gen_inf, text='Maximum 2 digits and 2 decimal places',
                                       bd='3', font='Helvetica 8')
        self.label_warning4.place(relx=0.075, rely=0.85,  relwidth=0.5,
                                  relheight=0.05)

        ############################################################################################

        self.frame_button = tk.Frame(self.frame, bd='3', padx=3, pady=3)

        self.button_start = tk.Button(self.frame_button, text='Start',
                                      command=self.start_clicked)

        self.button_start.place(relx=0.7, rely=0, relheight=1,
                                 relwidth=0.25)

        ##############################################################################################

        self.frame_gen_inf.place(relx=0.005, rely=0.005, relwidth=0.99,
                                 relheight=0.96)

        self.frame_button.place(relx=0.005, rely=0.915, relwidth=0.99,
                                relheight=0.08)

        self.frame.place(relx=0.02, rely=0, relwidth=0.96, relheight=0.96)
        self.canvas.pack()
        ##############################################################################################

    # this function is called when the start button is clicked
    def start_clicked(self):
        # check if any values are missing
        if not self.PulseWidth.get():
            tkm.showerror('Error', 'PulseWidth value is missing!')
            return
        if not self.InterPulseWidth.get():
            tkm.showerror('Error', 'InterPulseWidth value is missing!')
            return
        if not self.nPulses.get():
            tkm.showerror('Error', 'nPulses value is missing!')
            return
        print(self.nPulses.get())
        nPulses = "{0:0=2d}".format(int(self.nPulses.get()))

        PulseWidth = round(float(self.PulseWidth.get()), 2)
        if PulseWidth >= 1000:
            PulseWidth = 99999
        else:
            PulseWidth *= 100
        PulseWidthMicro = "{0:0=3d}".format(int(PulseWidth//100))
        PulseWidthNano = "{0:0=2d}".format(int(PulseWidth%100))

        InterPulseWidth = round(float(self.InterPulseWidth.get()), 2)
        if InterPulseWidth >= 1000:     
            InterPulseWidth = 99999     
        else:
            InterPulseWidth *= 100
        InterPulseWidthMicro = "{0:0=3d}".format(int(InterPulseWidth//100))
        InterPulseWidthNano = "{0:0=2d}".format(int(InterPulseWidth%100))

        InitShift = round(float(self.InitShift.get()), 2)
        if InitShift >= 1000:     
            InitShift = 99999     
        else:
            InitShift *= 100

        InitShiftWidthMicro = "{0:0=3d}".format(int(InterPulseWidth//100))
        c = "{0:0=2d}".format(int(InterPulseWidth%100))

        # Arduino gets 16 digit number
        dataToSend = nPulses + PulseWidthMicro + PulseWidthNano + InterPulseWidthMicro + InterPulseWidthNano + InitShiftWidthMicro + InitShiftWidthMicro
        arduino.write(dataToSend.encode())
        

# window for COM port selection
select = tk.Tk()
select.geometry('400x200')
select.resizable(0, 0)
select.title('Port selection')

# blank title bar icon
#ICON = (b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
#        b'\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00'
#        b'\x08\x00\x00\x00\x00\x00@\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#        b'\x00\x01\x00\x00\x00\x01') + b'\x00'*1282 + b'\xff'*64
#
#_, ICON_PATH = tempfile.mkstemp()
#with open(ICON_PATH, 'wb') as icon_file:
#    icon_file.write(ICON)

#select.iconbitmap(default=ICON_PATH)

# function for connecting with arduino 
def connect(port_number):
    select.destroy()
    global arduino
    arduino = serial.Serial('COM{}'.format(port_number), baudrate = 115200, timeout = 0)

# make opening window for COM port selection
#label_COM = tk.Label(select, text='COM', bd='3', font='Helvetica 14 bold') 
#var = tk.IntVar()     
#COM = tk.Entry(select, textvariable = var, bd='3', justify="center")
#label_COM.place(relx=0.05, rely=0.4,  relwidth=0.3, relheight=0.2)
#COM.place(relx=0.3, rely=0.4, relwidth=0.15, relheight=0.2)
#warning = tk.Label(select, text='Select your Teensy port!', bd='3', font='Helvetica 12')
#warning.place(relx=0.1, rely=0.2,  relwidth=0.5, relheight=0.1)
#frame_button = tk.Frame(select, bd='3', padx=3, pady=3)
#button_start = tk.Button(select, text='Start', command=lambda: [connect(var.get())])
#button_start.place(relx=0.6, rely=0.4, relheight=0.2, relwidth=0.25)
#button_start.wait_variable(var)
select.mainloop()

# main application window
window = tk.Tk() 
window.resizable(0,0) 
window.title("Stroboscope")
#window.iconbitmap(default=ICON_PATH)
c = MainApplication(window)
window.mainloop()