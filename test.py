
import matplotlib
import matplotlib.dates as mdates
import datetime
import numpy as np

matplotlib.use('TkAgg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure




import sys
if sys.version_info[0] < 3:	
    import Tkinter as Tk
else:
    import tkinter as Tk

from tkinter import ttk
import logging
from lib.dataproc import dataproc
from lib.mywidget import StatusFrame

from lib.mywidget import Calendar
import calendar

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.info('Start App')



root = Tk.Tk()
root.wm_title("TkPlot")


f = Figure(figsize=(5, 4), dpi=100)
a = f.add_subplot(111)
t = arange(0.0, 3.0, 0.01)
s = sin(2*pi*t)

a.plot(t, s)


# a tk.DrawingArea
canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=2)

toolbar = NavigationToolbar2TkAgg(canvas, root)
toolbar.update()
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)




def on_key_event(event):
	print('you pressed %s' % event.key)
	key_press_handler(event, canvas, toolbar)

canvas.mpl_connect('key_press_event', on_key_event)


def _quit():
	logger.info('Finish App')
	root.quit()     # stops mainloop
	root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate
	

#bQuit = Tk.Button(master=root, text='Quit', command=_quit)
#bQuit.pack(side=Tk.LEFT)
#bLoad = Tk.Button(master=root, text='Quit', command=_quit)
#bLoad.pack(side=Tk.LEFT)


def load():
	
	filename = Tk.filedialog.askopenfilename(filetypes = (("Data files", "*.txt"),("All files", "*.*")), initialdir = "~/home/pablo/Dropbox/python/tkinter")
	dp = dataproc(filename)
		
	if filename is not '':
		
		dp.load()
		#pb = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
		#pb.pack()
		filemenu.entryconfig("Load", state="disabled")
		#w = Tk.Label(root, text="Progress")
		#w.pack(side = Tk.LEFT)
		mystatusframe = StatusFrame(root)
		mystatusframe.pack(side = Tk.BOTTOM)
		pre = 0
		for load in dp:
			
			_total  = int(dp.read / dp.size * 100)
			mystatusframe.label.config(text=str(_total) + " %")
			mystatusframe.pb["value"] = _total
			
			if pre < _total:
				prev = _total 
				mystatusframe.pb.update_idletasks()
				root.update()
		mystatusframe.destroy()
		filemenu.entryconfig("Load", state="normal")
		
	else:
		logger.info('No file slected')
	
	dp = None

def __plot():
	
	
	logger.info('Call Plot')
	
	
	dp = dataproc('')
	
	tupla = np.array(dp.get_data(1))
	x1 = tupla[:,0]
	s1 = tupla[:,1]
	
	tupla = np.array(dp.get_data(2))
	
	x2 = tupla[:,0]
	s2 = tupla[:,1]
	
	a.clear()
	a.plot(x1,s1,x2,s2)
	
	_day = mdates.DayLocator()
	_month = mdates.MonthLocator()
	_week = mdates.WeekdayLocator()
	a.xaxis.set_minor_locator(_day)
	a.xaxis.set_major_locator(_week)
	

	#a.format_xdata = mdates.DateFormatter('%Y-%m-%d')
	#a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
	a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
	a.set_xlim(x1.min(), x1.max())
	a.set_ylim(-2, 80)
	a.grid(True)
	#f.autofmt_xdate()
	
	canvas.show()
	pass

def __data_info():
	data = dataproc('')
	for s in data.getSensorAll(): 
		print (s.id)

def __showCalendar():
	return 0
	ttkcal = Calendar(firstweekday=calendar.SUNDAY)
	ttkcal.pack(expand=1,fill='both')

	if 'win' not in sys.platform:
		style = ttk.Style()
		style.theme_use('clam')
	pass

menubar = Tk.Menu(root)

filemenu = Tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Load", command=load)
filemenu.add_command(label="Plot", command=__plot)

filemenu.add_separator()
filemenu.add_command(label="Exit", command=_quit)

filemenut = Tk.Menu(menubar, tearoff=0)
filemenut.add_command(label="Data info", command=__data_info)
filemenut.add_command(label="Calendar", command=__showCalendar)


menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="Tools", menu=filemenut)

#menubar.add_command(label="Hello!", command=hello)
#menubar.add_command(label="Quit!", command=_quit)



root.config(menu = menubar)




Tk.mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.


	
	
