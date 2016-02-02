# max.prokopenko@gmail.com
# written for openrobotics.ca
import sys
from os import path
sys.path.append(path.dirname(__file__) + 'lib/') #for generic functionality
sys.path.append(path.dirname(__file__) + 'modules/') #specific to various hardware

import random
import struct
from utilities import Utility
from serial_manager import SerialManager

utils = Utility()

manager = SerialManager()
print ""
print "Select a port to connect to or a menu option below"
manager.list_ports()

from threads import AutoTimer

def timer_function(): 
	print 'lammm'
sertest = AutoTimer(timer_function)

while True:

	user_input = raw_input()

	if manager.open_port(user_input, 57600):
		print 'yay'

	else:
		if user_input == 'q' or user_input == 'quit':
			sertest.stop()
			manager.close()
			quit()