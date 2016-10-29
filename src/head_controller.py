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
	
	serv_2 = Robotis_Servo(manager1, 1)
	print 'Setting up Dynamixel 2'
	
	print 'Dynamixel 2 at ' + str(serv_2.read_angle())

	while(alive):
		serv_2.move_angle(1, 1.5, blocking=False)
		time.sleep(1)
		serv_2.move_angle(2, 1.5, blocking=False)
		time.sleep(1)

manager1.close()