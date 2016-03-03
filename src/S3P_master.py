# max.prokopenko@gmail.com
# written for openrobotics.ca
from __future__ import print_function
from __future__ import unicode_literals
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
print('\nSelect a port to connect to or a menu option below')
manager.list_ports()

from threads import AutoTimer, EventWrapper

from data_structures import v2_drivetrain as v2dt 
from data_structures import mini_arm as marm

marm.status = ord('k')
v2dt.speed1 = 1
v2dt.speed2 = 255
v2dt.status = ord('k')

def e0():
	manager.write(marm.get_outgoing_struct())

dataflag = False

def e1():
	global dataflag
	dataflag = manager.receive_into(marm)
	manager.write(v2dt.get_outgoing_struct())

def e2():
	manager.receive_into(v2dt)
	pass

ev0 = EventWrapper(e0, 0)
ev1 = EventWrapper(e1, marm.calculate_timeout(115200))
ev2 = EventWrapper(e2, marm.calculate_timeout(115200) + v2dt.calculate_timeout(115200))

sertest = AutoTimer(period=1, events=[ev0,ev1,ev2])

if manager.open_port('0', 115200):
	sertest.start()

try:
	while True:

		if dataflag:
			print(marm.voltages)
			print(marm.test)
			dataflag = False

		#user_input = raw_input()

			'''
		if manager.open_port(user_input, 115200):
			sertest.start()
		else:
			if user_input == 'q' or user_input == 'quit':
				sertest.stop()
				manager.close()
				quit()'''
except KeyboardInterrupt:
	print('Closing threads, serial port, and quitting...')
	sertest.kill()
	manager.close()
	quit(0)