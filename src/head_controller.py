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
	
	serv = Robotis_Servo(manager1,5)
	print('Setting up Dynamixel')
	
	print('Dynamixel angle at ' + str(serv.read_angle()))
	print('Dynamixel encoder at ' + str(serv.read_encoder()))

	while(alive):
		#serv.move_angle(1, 1.5, blocking=False)
		serv.move_to_encoder(650)
		time.sleep(1)
		serv.move_to_encoder(700)
		time.sleep(1)

manager1.close()