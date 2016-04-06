# max.prokopenko@gmail.com
# written for openrobotics.ca
import sys
from os import path
sys.path.append(path.dirname(__file__) + 'lib/') #for generic functionality
sys.path.append(path.dirname(__file__) + 'modules/') #specific to various hardware

from threading import Thread
from time import clock
from time import sleep
from utilities import Utility
from serial_manager import SerialManager
from pololu_controller import PololuController
from Servo import *
from data_structures import mini_arm as marm

utils = Utility()
alive = True

def quit():
	global alive
	alive = False

manager1 = SerialManager()
print 'Ports available'
manager1.list_ports()

#print_function_dict()
print 'Select servo port'
user_input = utils.getch()

if manager1.open_port(user_input, 57600):

	e_rot = PololuController(manager1, 1)
	print 'Setting up Pololu 1'
	e_elev = PololuController(manager1, 2)
	print 'Setting up Pololu 2'

	e_rot.move_to(0);
	#e_elev.move_to(-10);
	time.sleep(1)
	
	serv_2 = Robotis_Servo(manager1, 2)
	print 'Setting up Dynamixel 2'
	serv_5 = Robotis_Servo(manager1, 5)
	print 'Setting up Dynamixel 5'
	
	serv_2.set_angvel(0.5)
	serv_2.set_cw_limit(1)
	serv_2.set_ccw_limit(4095)	
	serv_2.move_angle(2.5, 0.5, blocking=True)
	print 'Dynamixel 2 at ' + str(serv_2.read_angle())

	serv_5.set_angvel(0.5)
	serv_5.set_cw_limit(1)
	serv_5.set_ccw_limit(4095)	
	serv_5.move_angle(2, 0.5, blocking=True)
	print 'Dynamixel 5 at ' + str(serv_5.read_angle())
	
	while(alive):
		manager1.write("@MARM?")
		if marm.pack_into_received(manager1.serial_io.read(17)):
			s5_angle = (marm.voltages[5] - 2640) / 800.0 + 2
			s2_angle = (2350 - marm.voltages[6]) / 300.0 + 2.5
			e_rot_angle = (marm.voltages[4] - 2500) / 30
			print marm.voltages
			print e_rot_angle
			e_rot.move_to(e_rot_angle)
			#serv_5.move_angle(s5_angle, 0.5, blocking=False)
			#serv_2.move_angle(s2_angle, 0.5, blocking=False)
		time.sleep(0.05)

manager1.close()