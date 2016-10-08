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
print 'Select Dynamixel port'
user_input = utils.getch()

if manager1.open_port(user_input, 57600):
	
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

manager2 = SerialManager()
print 'Ports available'
manager2.list_ports()
print 'Select Torxis(red servo) port'
user_input = utils.getch()

def controlled(old_voltages, new_voltages):
	for i, v in enumerate(old_voltages):
		if abs(old_voltages[i] - new_voltages[i]) > 150:
			return True
	return False

if manager2.open_port(user_input, 57600):

	e_rot = PololuController(manager2, 1)
	print 'Setting up Pololu 1'
	e_elev = PololuController(manager2, 2)
	print 'Setting up Pololu 2'

	e_elev.move_to(0)
	time.sleep(1)

	last_voltages = []
	hold_counter = 0
	s2_array = [2.5, 0.8, 2.5, 4]
	s5_array = [2.0, 1, 2.0, 3]
	e_rot_array = [0, 30, 0, -30]
	e_elev_array = [0, 20, 0, -20]

	while(alive):
		manager1.write("@MARM?")
		if marm.pack_into_received(manager1.serial_io.read(17)):
			if not controlled(last_voltages, marm.voltages):
				hold_counter += 1
			else:
				hold_counter = 0
			if hold_counter < 50:
				s5_angle = (marm.voltages[5] - 2550) / 900.0 + 2
				s2_angle = (2350 - marm.voltages[6]) / 300.0 + 2.5
				e_rot_angle = (marm.voltages[4] - 2600) / 20
				e_elev_angle = (marm.voltages[1] - 2400) / 25
			'''else:
				if hold_counter >= 250: hold_counter = 50
				print 'Starting auto routine'
				arr_i = (hold_counter / 50) % 4
				print arr_i
				e_rot_angle = e_rot_array[arr_i]
				e_elev_angle = e_elev_array[arr_i]
				s5_angle = s5_array[arr_i]
				s2_angle = s2_array[arr_i]
				print e_rot_angle
				print e_elev_angle'''
			e_rot.move_to(e_rot_angle)
			e_elev.move_to(e_elev_angle)
			serv_5.move_angle(s5_angle, 0.8, blocking=False)
			serv_2.move_angle(s2_angle, 1.5, blocking=False)
			last_voltages = marm.voltages
		time.sleep(0.05)

manager1.close()