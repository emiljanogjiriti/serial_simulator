# max.prokopenko@gmail.com
# written for openrobotics.ca
from __future__ import print_function
from __future__ import unicode_literals
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
print('Ports available')
manager1.list_ports()
print('Select Dynamixel port')
user_input = utils.getch()

if manager1.open_port(user_input, 115200):
	
	serv2 = Robotis_Servo(manager1,2)
	print('Setting up Dynamixel')
	print('Dynamixel angle at ' + str(serv2.read_angle()))
	print('Dynamixel encoder at ' + str(serv2.read_encoder()))

	serv5 = Robotis_Servo(manager1,5)
	print('Setting up Dynamixel')
	print('Dynamixel angle at ' + str(serv5.read_angle()))
	print('Dynamixel encoder at ' + str(serv5.read_encoder()))

	while(alive):
		#serv.move_angle(1, 1.5, blocking=False)
		serv2.move_angle(0.5,blocking=False)
		serv5.move_angle(0.1,blocking=False)
		time.sleep(2)
		serv2.move_angle(0.1,blocking=False)
		serv5.move_angle(0.5,blocking=False)
		time.sleep(2)

manager1.close()