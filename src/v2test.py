# max.prokopenko@gmail.com
# written for openrobotics.ca
from __future__ import print_function
from __future__ import unicode_literals
import sys
from os import path
sys.path.append(path.dirname(__file__) + 'lib/') #for generic functionality
sys.path.append(path.dirname(__file__) + 'modules/') #specific to various hardware

from data_structures import v2_drivetrain as v2dt 
from data_structures import mini_arm as marm
from serial_manager import SerialManager as ser
import time
from Tkinter import *
import tkFont
import tk_monitor
from threading import Thread
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s  %(levelname)s: %(message)s")
logging.info('Start of P')

s = ser()
s.list_ports()
s.open_port(1, 115200)

marm.status = ord('U')

class AppThing():
	def __init__(self, app):
		self.app = app
	def serial_stuff(self):
		while(True):
			s.write(marm.get_outgoing_struct())
			time.sleep(0.02)
			if(s.receive_into(marm)):
				scaled = [ v / 1000.0 for v in marm.voltages]
				logging.info(scaled)
				self.app.set_displayed(scaled)




'''
class TkThread(Thread):
	def __init__(self, app):
		super(TkThread, self).__init__()
		self.app = app

	def run(self):
		print('huh?')
		app.mainloop()
'''
root = Tk()
app = tk_monitor.Application(master=root, screen_size=(1080, 720))
app.master.minsize(500, 500)
appThing = AppThing(app)
serial_thread = Thread(target=appThing.serial_stuff);
serial_thread.start()
app.mainloop()
'''
appThreaded = TkThread(app)
appThreaded.run()
'''


while(True):
	pass
#appThreaded.join()
root.destroy()
serial_thread.join()