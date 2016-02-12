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

from threads import AutoTimer, OneShotTimer

from data_structures import v2_drivetrain as v2dt 
from data_structures import mini_arm as marm

def e0():
	manager.write(v2dt.get_outgoing_struct())

def e1():
	print manager.receive_into(v2dt)
	manager.write(marm.get_outgoing_struct())

def e2():
	print manager.receive_into(marm)

event_list = list()

def schedule(time, *args):
	global event_list
	for event in args:
		event_timer = OneShotTimer(event, time)
		event_list.append(event_timer)

schedule(v2dt.calculate_timeout(115200), e0)
schedule(marm.calculate_timeout(115200) + v2dt.calculate_timeout(115200), e1)
schedule(0.5, e0)

def timer_function(): 
	print 'Scheduler'
	for event in event_list:
		event.run()
sertest = AutoTimer(1, timer_function)

while True:

	user_input = raw_input()

	if manager.open_port(user_input, 57600):
		print 'yay'

	else:
		if user_input == 'q' or user_input == 'quit':
			sertest.stop()
			manager.close()
			quit()