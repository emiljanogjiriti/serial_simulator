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
	manager.write(marm.get_outgoing_struct())

dataflag = False

def e1():
	global dataflag
	dataflag = manager.receive_into(marm)
	#manager.write(v2dt.get_outgoing_struct())

def e2():
	#print manager.receive_into(v2dt)
	pass

event_list = list()

def schedule(time, *args):
	global event_list
	for event in args:
		event_timer = OneShotTimer(event, time)
		event_list.append(event_timer)

schedule(marm.calculate_timeout(115200), e1)
print "Mini-arm read timeout: " + str(marm.calculate_timeout(115200))
#schedule(marm.calculate_timeout(115200) + v2dt.calculate_timeout(115200), e1)
#schedule(0.5, e2)

def timer_function(): 
	#print 'Scheduler'
	e0()
	for event in event_list:
		event.run()
sertest = AutoTimer(0.020, timer_function)


if manager.open_port('0', 115200):
	sertest.start()

try:
	while True:

		if dataflag:
			print marm.dataOut
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
	print "Closing threads, serial port, and quitting..."
	sertest.stop()
	manager.close()
	quit()