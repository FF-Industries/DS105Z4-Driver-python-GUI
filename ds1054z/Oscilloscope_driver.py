import vxi11                                                                                 # Import vxi11 library for instrument communication
from tkinter import *                                                                        # Import tkinter library for GUI
from tkinter import ttk, filedialog, messagebox                                              # Import additional tkinter modules
from PIL import Image, ImageTk                                                               # Import modules for working with images
from ds1054z import DS1054Z                                                                  # Import DS1054Z module for interacting with the oscilloscope
import configparser                                                                          # Import configparser module for working with configuration files
import os                                                                                    # Import os module for file and directory operations
from os.path import exists                                                                   # Import exists function from os.path module
from pathlib import Path                                                                     # Import Path class from pathlib module for path operations
import matplotlib.pyplot as plot                                                             # Import matplotlib for plotting
from matplotlib.animation import FuncAnimation                                               # Import FuncAnimation for animation
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)      # Import modules for embedding Matplotlib figures in Tkinter
from matplotlib.backend_bases import key_press_handler                                       # Import module for key press handling in Matplotlib
from matplotlib.figure import Figure                                                         # Import Figure class from Matplotlib for creating figures
import sys                                                                                   # Import sys module for system-related operations
import numpy as np                                                                           # Import numpy for numerical operations

# Get the current working directory
directory = os.getcwd()        

instr = None                                     # Initialize instrument object as None
stop = 1200                                      # Stop frame for animation
animation_obj = None                             # Initialize animation object as None
animation_running = False                        # Flag to track if animation is running or not

top = Tk()                                       # Create the main Tkinter window
top.geometry("800x710")                          # Set the window size
top.configure(bg="pink")                         # Set the background color
top.title("Oscilloscope Interface Software")     # Set the window title

def ConnectCallBack():  # Callback function for the "Connect" button
    
    global instr                             # Use the global instrument object
    e_text = IP_text.get()                   # Get the IP address from the entry field
    print(e_text)
    instr = DS1054Z(e_text)                  # Create an instance of DS1054Z instrument
    devName = instr.ask("*IDN?")             # Get the device name
    print(devName)
    lbl_info.config(text=devName)            # Update the label with the device name

def RunCallBack():                           # Callback function for the "Run" button
     
    global instr
    if instr is None:
        messagebox.showerror("Error", "Instrument Not Connected !!!")
    else:
        instr.run() 
    
def StopCallBack():    # Callback function for the "Stop" button
    
    global instr
    if instr is None:
        messagebox.showerror("Error", "Instrument Not Connected !!!")
    else:
        instr.stop()

def Readpreamble():    # Callback function for the "Position of axis" button
    
    global instr
    if instr is None:
        messagebox.showerror("Error", "Instrument Not Connected !!!")
    else:
        fmt, typ, pnts, cnt, xinc, xorig, xref, yinc, yorig, yref = instr.waveform_preamble
        print("Points = ",pnts)
        print("X-Origin = ",xorig)
        print("Y-Origin = ",yorig)
          
        redirect_console_output("data.txt")
        
        print(devName)
        print()
        print(e_textCh)        
        print()
        print("Points = ",pnts)
        print()
        print("X-Origin = ",xorig)
        print()
        print("Y-Origin = ",yorig)
       
def hex_format(data):   # Convert data to hexadecimal format
    
    formatted_data = []
    for byte in data:
        formatted_data.append(f"0x{byte:02x}")
    return formatted_data

def redirect_console_output(filename):    # This redirects the standard output to the file
    sys.stdout = open(filename, 'w')

def waveforM():          # This fucntion gets the data and converts it to suitable format
    
    global instr
    if instr is None:
        #ascii_data = b'HEFIGKGLIMKPMQOTPUSXV[X_[a_dbgekholqousyw|{\x80~\x84\x82\x88\x84\x8b\x88\x8e\x8c\x91\x90\x95\x93\x98\x96\x9a\x99\x9e\x9c\xa1\x9f\xa4\xa1\xa5\xa4\xa8\xa5\xa9\xa8\xac\xa9\xad\xab\xae\xac\xb0\xad\xb1\xad\xb1\xb1\xae\xaf\xb1\xae\xb2\xb1\xae\xb1\xad\xad\xb0\xb0\xab\xae\xab\xad\xa8\xac\xa7\xa9\xa5\xa8\xa3\xa5\xa0\xa3\x9d\xa0\x9b\x9e\x98\x9b\x95\x98\x92\x95\x8f\x92\x8b\x8f\x88\x8b\x84\x88\x80\x84|\x81x}vyqunrjogkdh_e]a[_W\\UYRWPTNRLPJMILGLFIEIEHCHCDHHCEHEIEKGLHMJOKPLSOTRXSYW]Z_]c_ecifljpntpxt{x\x7f{\x83\x7f\x87\x82\x89\x86\x8d\x8a\x90\x8e\x92\x90\x98\x93\x9a\x97\x9d\x98\xa0\x9c\xa2\x9e\xa5\xa1\xa8\xa3\xaa\xa5\xac\xa7\xad\xa8\xaf\xa9\xb1\xb1\xab\xac\xb2\xb2\xac\xac\xb4\xac\xb4\xb2\xac\xb2\xac\xac\xb2\xb1\xab\xb0\xa9\xaf\xa8\xad\xa7\xac\xa4\xaa\xa3\xa8\xa0\xa6\x9e\xa4\x9b\xa1\x98\x9d\x95\x9a\x93\x98\x8f\x94\x8c\x91\x88\x8d\x86\x8a\x82\x87\x7f\x84{\x80v|tyoulqhpdkbg^d[aX]V[SYPWNTLQJPIGOMFLEKCKCIBIBCICKCKDLELFMGOIQKSMUOWRYT\\W_Zc\\e`hclgpjsnwryv}x\x81|\x85\x80\x89\x83\x8c\x87\x90\x8a\x92\x8e\x96\x91\x99\x94\x9c\x98\x9e\x9b\xa1\x9e\xa2\xa1\xa5\xa3\xa7\xa5\xa9\xa7\xaa\xa9\xad\xab\xae\xac\xae\xad\xb0\xad\xb1\xb1\xad\xaf\xb1\xaf\xb1\xb1\xaf\xaf\xb1\xb0\xad\xaf\xac\xae\xab\xad\xa8\xaa\xa5\xa8\xa4\xa5\xa1\xa4\x9f\xa1\x9c\x9e\x99\x9c\x97\x98\x93\x95\x90\x92\x8c\x8f\x8a\x8b\x86\x88\x82\x84\x7f\x80{}wytupqloikfhbd_a\\_Y\\VXSURTOQMOKMJLHKGIFHFHEEHEHEHEHHFFIFKHLIMKPNQOTRWTYW\\Z_\\a_echfljpnspwtyx}{\x81\x7f\x85\x83\x88\x87\x8c\x8a\x8f\x8e\x92\x90\x95\x94\x99\x97\x9c\x99\x9e\x9d\xa1\xa0\xa4\xa1\xa6\xa4\xa8\xa6\xaa\xa8\xac\xa9\xad\xae\xab\xac\xb0\xb0\xad\xaf\xb1\xaf\xb1\xaf\xb1\xb1\xaf\xb1\xaf\xb1\xae\xb0\xad\xaf\xac\xae\xab\xad\xa9\xac\xa8\xa9\xa5\xa6\xa3\xa5\xa0\xa2\x9d\xa0\x9b\x9d\x98\x99\x95\x96\x91\x94\x8f\x90\x8b\x8d\x87\x89\x84\x87\x80\x83~\x7fz|vxruoqkmhidgbc^`[]X[UXSUPSNPLOJMILHKGIFHEHEHEEHEHEIIEFLLFIOHPKSMUOWQYS\\V_Yc\\e^hblfphslwpys}w\x81z\x84~\x88\x83\x8c\x86\x90\x8a\x92\x8d\x96\x90\x99\x93\x9c\x97\x9f\x99\xa2\x9c\xa5\x9f\xa6\xa1\xa9\xa3\xac\xa5\xad\xa7\xae\xa9\xb0\xa9\xb1\xac\xb2\xb2\xac\xad\xb4\xb4\xad\xb4\xad\xad\xb4\xad\xb3\xb2\xac\xb2\xab\xb1\xa9\xb0\xa8\xae\xa7\xac\xa5\xaa\xa3\xa8\xa0\xa5\x9e\xa3\x9b\xa1\x98\x9d\x96\x9a\x93\x98\x8f\x94\x8c\x91\x88\x8d\x84\x8a\x82\x87~\x83z\x80w}sxoulqhnekbg^d[aX]V[SXQVNTLQKPIOGMFLEKCKBIBIBBJBKCKCLFLMGMIKPMQOTRVSXW\\Z_\\a_dbhfkjolspvsyw}{\x81\x7f\x84\x83\x88\x86\x8b\x8a\x8f\x8c\x92\x90\x95\x93\x98\x97\x9c\x99\x9e\x9c\xa1\x9f\xa4\xa1\xa6\xa4\xa8\xa5\xaa\xa8\xac\xaa\xad\xab\xae\xac\xb0\xad\xb1\xaf\xb1\xaf\xb2\xb1\xb0\xaf\xb2\xb1\xaf\xb1\xad\xb1\xad\xb0\xac\xae\xab\xad\xa9\xac\xa8\xa9\xa5\xa8\xa4\xa5\xa1\xa2\x9f\xa0\x9c\x9d\x99\x9a\x95\x98\x93\x95\x8f\x91\x8c\x8d\x88\x8b\x86\x87\x80\x84~\x80{|wxsuoqlmhkegbd_`[_X[VXSUPSOQLOKMILHKFIFEIIEHEHEEIEIFIKEGLHMJPKQNSOURXS\\V]Z`\\d`gckfmjqmupxt|x\x80{\x83\x7f\x87\x83\x8a\x86\x8e\x8a\x91\x8e\x95\x91\x96\x94\x9a\x97\x9d\x9b\xa0\x9d\xa2\xa0\xa5\xa2\xa8\xa5\xaa\xa6\xac\xa8\xad\xa9\xae\xac\xb0\xac\xb1\xad\xb1\xb2\xae\xaf\xb2\xaf\xb2'
        #ascii_data = b'\x9c\x9c\x9b\x9b\x9a\x9a\x99\x99\x98\x98\x97\x96\x96\x96\x93\x94\x94\x94\x93\x93\x92\x91\x90\x8f\x8f\x8e\x8e\x8d\x8c\x8d\x8c\x8b\x8a\x8a\x89\x8a\x88\x89\x86\x86\x86\x84\x83\x83\x83\x83\x81\x80\x80\x80\x7f~~}||{zyxyywvvvvuttsqqqqpoonmlmkkikhhighgeedccccbaca``___^_]]]]\\\\[[\\ZZ[[ZYZYXYXYXXXXWWXWWWWXWXXYWVXXXWXXXXXXYYZYZZ\\\\[[[\\\\\\]]]]__`_b`aabcccdedfgfgghhjijjjkmllnoopqqqsttttuvvwxyz{z||}~~\x7f\x80\x80\x81\x81\x82\x83\x84\x84\x85\x85\x88\x87\x87\x88\x89\x89\x8a\x8b\x8c\x8c\x8d\x8e\x8d\x8f\x8f\x90\x91\x90\x91\x93\x92\x94\x94\x94\x96\x95\x96\x97\x98\x97\x99\x99\x9a\x98\x99\x9a\x9b\x9c\x9d\x9c\x9e\x9e\x9e\x9e\x9f\xa0\xa0\xa0\xa2\xa1\xa1\xa1\xa1\xa1\xa2\xa3\xa4\xa3\xa3\xa4\xa4\xa5\xa5\xa5\xa6\xa5\xa6\xa6\xa6\xa6\xa6\xa6\xa7\xa6\xa6\xa6\xa7\xa7\xa7\xa6\xa7\xa7\xa7\xa7\xa7\xa7\xa7\xa5\xa7\xa6\xa6\xa6\xa7\xa6\xa6\xa5\xa6\xa5\xa5\xa4\xa4\xa5\xa4\xa4\xa4\xa3\xa2\xa2\xa2\xa2\xa2\xa0\xa1\xa0\x9f\xa0\x9f\x9f\x9f\x9e\x9e\x9d\x9d\x9d\x9c\x9c\x9c\x99\x9a\x98\x99\x97\x97\x98\x97\x96\x97\x95\x94\x93\x93\x94\x93\x92\x91\x91\x8f\x90\x90\x8f\x8e\x8e\x8d\x8c\x8b\x8a\x8b\x89\x89\x88\x88\x87\x86\x86\x85\x84\x84\x83\x83\x82\x81\x81\x80\x80\x7f~~}||{zzyyxwwwvuttssrqqpoomnllklkjjihhhgfeedddddcba``_`__`_]]^\\\\\\[[ZZZZZZ[YXXZYYXXWWWWWWWWWVWWWWWWWWWXXXXYXXYYZ[ZZZZ[[[[[\\\\\\]^^__`_`aabbccdddfegfhhhiijkjlklnoopprqrsstuuuuvxyyzz|||}~~\x7f\x7f\x81\x80\x81\x82\x83\x85\x85\x84\x87\x87\x87\x88\x89\x8a\x89\x8a\x8b\x8c\x8c\x8d\x8d\x8f\x8f\x8e\x91\x90\x91\x91\x93\x93\x94\x93\x96\x95\x96\x97\x97\x98\x99\x98\x99\x99\x99\x9b\x9b\x9b\x9c\x9d\x9d\x9c\x9e\x9e\x9f\xa0\xa0\xa0\xa1\xa0\xa2\xa2\xa1\xa1\xa2\xa3\xa4\xa3\xa4\xa4\xa5\xa5\xa5\xa5\xa6\xa5\xa6\xa6\xa6\xa6\xa6\xa6\xa7\xa6\xa6\xa7\xa7\xa7\xa7\xa7\xa8\xa7\xa7\xa7\xa7\xa7\xa7\xa7\xa7\xa6\xa6\xa6\xa7\xa6\xa7\xa5\xa6\xa4\xa5\xa5\xa5\xa4\xa4\xa2\xa4\xa3\xa2\xa2\xa2\xa2\xa2\xa1\xa2\xa0\xa0\xa0\xa0\x9f\x9f\x9e\x9e\x9d\x9d\x9d\x9c\x9b\x9c\x9b\x9b\x98\x98\x99\x98\x97\x98\x96\x97\x95\x95\x94\x94\x93\x92\x93\x92\x91\x91\x91\x90\x8e\x8e\x8d\x8e\x8c\x8b\x8b\x8a\x8a\x8a\x89\x89\x88\x88\x87\x86\x86\x84\x83\x83\x82\x81\x81\x81\x80\x80~~}}||{zyyxwwvvvtutssrqppponmmlkkkijiihfgfeddeecbbaaaa````_^]]\\\\[[[ZZ[ZZYZYXXYYYWXWXWWWWWWWWWXXWWXWWXXXXXZYXYYYZZZZZZ[[[[\\\\\\]^^__```aabbbcccdefffhhhiijjklllnopoprprsttutuvwxyyzz|{|}~~\x7f\x7f\x81\x80\x81\x82\x83\x84\x84\x85\x86\x85\x86\x87\x89\x88\x89\x8b\x8b\x8c\x8c\x8d\x8d\x8d\x8e\x8e\x90\x8f\x90\x91\x93\x92\x92\x93\x94\x94\x95\x97\x96\x98\x98\x98\x99\x99\x9a\x9a\x9a\x9b\x9b\x9c\x9e\x9d\x9d\x9e\x9f\x9f\xa0\x9f\xa1\xa0\xa1\xa2\xa2\xa1\xa2\xa2\xa4\xa2\xa3\xa4\xa4\xa4\xa5\xa5\xa6\xa5\xa5\xa6\xa6\xa6\xa6\xa6\xa7\xa6\xa6\xa6\xa7\xa7\xa7\xa6\xa7\xa6\xa7\xa7\xa7\xa7\xa7\xa6\xa7\xa6\xa6\xa5\xa5\xa5\xa5\xa5\xa6\xa4\xa5\xa5\xa3\xa3\xa4\xa3\xa4\xa3\xa3\xa2\xa2\xa2\xa2\xa1\xa2\x9f\xa0\xa0\xa0\x9f\x9f\x9e\x9e\x9d\x9d\x9d\x9d\x9c\x9b\x9b\x9a\x99\x9a\x98\x99\x98\x98\x96\x96\x95\x95\x95\x93\x93\x93\x93\x92\x91\x91\x90\x8e\x8f\x8e\x8d\x8e\x8c\x8b\x8b\x8b\x8c\x8a\x88\x8a\x87\x87\x88\x87\x86\x84\x84\x84\x82\x81\x81\x81\x80\x80\x7f\x7f~}||{zzzxxxwwvuusrrrrqpoomnnllllijihhgfgee'
        messagebox.showerror("Error", "Instrument Not Connected !!!")
        return data
    else :    
        e_textCh = cbChList.get()
        print(e_textCh)
        
        if e_textCh == 'Ch1':
           print(instr.get_waveform_bytes(1))
           ascii_data = instr.get_waveform_bytes(1)
        elif e_textCh == 'Ch2':
           print(instr.get_waveform_bytes(2))
           ascii_data = instr.get_waveform_bytes(2) 
        elif e_textCh == 'Ch3':
           print(instr.get_waveform_bytes(3))
           ascii_data = instr.get_waveform_bytes(3) 
        elif e_textCh == 'Ch4':
           print(instr.get_waveform_bytes(4))
           ascii_data = instr.get_waveform_bytes(4) 
        else:
           #  Handle the case when e_textCh doesn't match any of the specified values
           print("Invalid channel selection.")    
           
        formatted_data = hex_format(ascii_data)
        print()
        print("INTEGER DATA = ")
        print()
        data = [int(x, 16) for x in formatted_data]
        print(data)
        print()
        print("HEX DATA = ")
        print()
        print(formatted_data)
        
        # Specify the filename for the text file
        filename = "Output.txt"
        devName  = instr.ask("*IDN?")
        e_textCh = cbChList.get()
        
        # Redirect console output to the file
        redirect_console_output(filename)

        # Print some data to the console                    #open while during testing
        print(devName)
        print()
        print(e_textCh)        
        print()
        print("RAW DATA = ")
        print()
        print(ascii_data)
        print()
        print("INTEGER DATA = ")
        print()
        print(data) 
        print()
        print("HEX DATA = ")
        print()
        print(formatted_data)               
        return data

def start_stop():           # This function starts or stops the animation based on the current state
    
    global animation_obj, animation_running
    if but_waveforms['text'] == 'Start':
        but_waveforms.config(text="Halt")
        if not animation_running:
            go()
            animation_running = True    
    else:
        but_waveforms.config(text="Start")  
        if animation_obj is not None:
            animation_obj.event_source.stop()
            animation_running = False
        
def test(frame):             # This function updates the plot with new data for each frame
    
    global wavedata
    if frame == 0:
        wavedata = waveforM()
    x = np.arange(frame + 1)
    y = wavedata[:frame + 1]
    line.set_data(x, y)
    return line,
    
def animation():             # This function creates and displays the animation
     
    global animation_obj
    animation_obj = FuncAnimation(fig, test, frames=stop, interval=10, blit=True)
    plot.show()

def go():                     # This function starts the animation if it is not already running
    
    global animation_obj, animation_running
    if animation_obj is None or not animation_running:
        animation_running = True
        if animation_obj is None:
            animation_obj = FuncAnimation(fig, test, frames=stop, interval=10, blit=True)
        else:
            animation_obj.event_source.start() 
        
# Create a label for displaying instrument Connection
lbl_info = Label(top, text="NOT CONNECTED", font='Helvetica 11 bold', width=83, height=3, bg="#B2EBF2", relief="solid", highlightthickness=4, highlightbackground="#37d3ff")
lbl_info.place(x=20, y=5)

# Create a frame for IP address entry
ip_frame = Frame(top, bd=2, relief="groove", bg="#54FA9B")
ip_frame.place(x=20, y=80, width=290, height=50)

# Create the label
ip_label = Label(ip_frame, text=" IP address :", font='Helvetica 14 bold', bg="#54FA9B")
ip_label.pack(side=LEFT, padx=10)

# Create the entry field
IP_text = Entry(ip_frame, justify="center", bg="white",width=19,font='Helvetica 14')
IP_text.pack(side=LEFT, padx=5, pady=5)
IP_text.insert(END, '169.254.1.5')


# Create a frame for channel selection
ch_frame = Frame(top, bd=2, relief="groove", bg="#54FA9B")
ch_frame.place(x=330, y=80, width=270, height=50)

chs = ['Ch1', 'Ch2', 'Ch3', 'Ch4']  # options

# Create a label for channel selection
lbl_channel = Label(ch_frame, text="Channel  :", font='Helvetica 14 bold', bg="#54FA9B")
lbl_channel.pack(side=LEFT, padx=20, pady=5)

# Create a combobox for channel selection
cbChList = ttk.Combobox(ch_frame, values=chs, width=22,font='Helvetica 14')
cbChList.pack(side=LEFT, padx=5, pady=5)
cbChList.set('Ch1')  # default selected option

# Create a button to connect to the instrument
but_connect = Button(top, text="Connect", bg='#FFD700', fg='black', font='Helvetica 13 bold', command=ConnectCallBack)
but_connect.place(x=620, y=80, width=160, height=50)

# Create a separator line
separator = ttk.Separator(top, orient='horizontal')
separator.place(x=0, y=140, relwidth=1)

# Create a button to run the instrument
but_run = Button(top, text="Run", bg='#FFD700', fg='black', font='Helvetica 13 bold', command=RunCallBack)
but_run.place(x=20, y=155, width=160, height=50)

# Create a button to stop the instrument
but_stop = Button(top, text="Stop", bg='#FFD700', fg='black', font='Helvetica 13 bold', command=StopCallBack)
but_stop.place(x=220, y=155, width=160, height=50)

# Create a button to retrieve waveform data
but_waveforms = Button(top, text="Waveform", bg='#FFD700', fg='black', font='Helvetica 13 bold', command=start_stop)
but_waveforms.place(x=420, y=155, width=160, height=50)

# Create a button to read waveform preamble
but_preamble = Button(top, text="Position of axis", bg='#FFD700', fg='black', font='Helvetica 13 bold', command=Readpreamble)
but_preamble.place(x=620, y=155, width=160, height=50)

# Add a separator line
separator = ttk.Separator(top, orient='horizontal')
separator.place(x=0, y=215, relwidth=1)

# Create an empty line object
fig, ax = plot.subplots(figsize=(8, 6))
ax.set_xlim(0, stop)
ax.set_ylim(0, 255)
line, = ax.plot([], [], lw=2)
ax.set_xlabel('Time', fontsize=12, fontweight='bold')
ax.set_ylabel('Amplitude', fontsize=12, fontweight='bold')
ax.set_title('Oscilloscope Graph', fontsize=14, fontweight='bold')
canvas = FigureCanvasTkAgg(fig, master=top)
canvas.draw()
canvas.get_tk_widget().place(x=20, y=230, width=750, height=460)

# Run the main event loop
top.mainloop()
