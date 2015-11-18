# max.prokopenko@gmail.com
# written for openrobotics.ca

import random
import struct
import io_utils
import serial_manager

utils = io_utils.Utility()
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

manager = serial_manager.SerialManager()
print "Select a port to connect to or a menu option below"
manager.list_ports()

print_function_dict()

while alive:

	user_input = utils.getch()

	if manager.open_port(user_input, 250000):
		manager.add_menu_functions(function_dict)
	else:
		try:
			function_dict[user_input]()
			print "'" + user_input + "' pressed"
		except KeyError:
			print 'No command for that key'

manager.close()