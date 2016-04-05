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

from data_structures import mini_arm as marm

manager1 = SerialManager()
print 'Ports available'
manager1.list_ports()

#print_function_dict()
print 'Select servo port'
user_input = utils.getch()

if manager1.open_port(user_input, 115200):
	'''
	elbow_rotation = PololuController(manager, 1, 'a', 'd')
	elbow_elevation = PololuController(manager, 2, 's', 'w')
	elbow_rotation.add_menu_functions(function_dict)
	elbow_elevation.add_menu_functions(function_dict)
	'''

	serv_2 = Robotis_Servo(manager1, 2)
	print 'Setting up Dynamixel 2'
	serv_5 = Robotis_Servo(manager1, 5)
	print 'Setting up Dynamixel 5'
	
	serv_2.set_angvel(10)
	serv_2.set_cw_limit(1)
	serv_2.set_ccw_limit(1023)
	'''

	serv_5.set_angvel(0.5)
	serv_5.set_cw_limit(800)
	serv_5.set_ccw_limit(2800)
	'''

manager2 = SerialManager()
print 'Ports available'
manager2.list_ports()	
print 'Select controller port'
user_input = utils.getch()
if manager2.open_port(user_input, 115200):
	while(alive):
		manager2.write('@MARM!')
		manager2.acq_mutex()
		marm.pack_into_received(manager2.serial_io.read(17));
		manager2.rel_mutex()
		if marm.voltages:
			try:
				serv_2.move_to_encoder(marm.voltages[0] / 5 + 1)
			except RuntimeError, e:
				print e

manager1.close()
manager2.close()