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
from pololu_controller import PololuController
from Servo import *

utils = Utility()
alive = True

def quit():
	global alive
	alive = False

function_dict = {'q':quit }

def print_function_dict():
	global function_dict
	for key in function_dict.keys():
		print "[" + key + "] " + function_dict[key].__name__

function_dict['m'] = print_function_dict

manager = SerialManager()
print ""
print "Select a port to connect to or a menu option below"
manager.list_ports()

print_function_dict()

while alive:

	user_input = utils.getch()

	if manager.open_port(user_input, 57600):
		manager.add_menu_functions(function_dict)

		elbow_rotation = PololuController(manager, 1, 'a', 'd')
		elbow_elevation = PololuController(manager, 2, 's', 'w')
		elbow_rotation.add_menu_functions(function_dict)
		elbow_elevation.add_menu_functions(function_dict)

		serv_2 = Robotis_Servo(manager, 2, 'i', 'k')
		print 'Setting up Dynamixel 2'
		serv_5 = Robotis_Servo(manager, 5, 'l', 'j')
		print 'Setting up Dynamixel 5'
		
		serv_2.set_angvel(0.5)
		serv_2.set_cw_limit(1)
		serv_2.set_ccw_limit(4095)
		serv_2.add_menu_functions(function_dict)

		serv_5.set_angvel(0.5)
		serv_5.set_cw_limit(800)
		serv_5.set_ccw_limit(2800)
		serv_5.add_menu_functions(function_dict)

	else:
		try:
			function_dict[user_input]()
			print "'" + user_input + "' pressed"
		except KeyError:
			print 'No command for that key'

manager.close()