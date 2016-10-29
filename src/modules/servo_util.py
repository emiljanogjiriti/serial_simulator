#!/usr/bin/python
'''
@author: Max Prokopenko
@email : max@embeddedprofessional.com
@github: https://github.com/maxlazarus
'''
from __future__ import print_function
from __future__ import unicode_literals
import os
from os import path
from os import sep
import time
import sys
sys.path.append(path.dirname(__file__) + '/../lib/') 
sys.path.append(path.dirname(__file__) + '../lib/') 
from serial_manager import SerialManager
from Servo import Robotis_Servo

ser = SerialManager()

baudrates = [1000000, 500000, 400000, 250000, 200000, 115200, 57600, 19200, 9600]
print("Select a baudrate:")

for baudrate in baudrates :
	print(str(baudrate) + ' bps')

	
current_baudrate = raw_input()
print (str(current_baudrate))


if int(current_baudrate) not in baudrates:
	print('incorrect baudrate selected')
	quit()


ser.list_ports()

for i, port in enumerate(ser.ports):
	if ser.open_port(i, current_baudrate):
		print('Scanning at ' + str(current_baudrate))
		for i in range(0, 10):
			print('scanning servo at id ' + str(i))
			try:
				r = Robotis_Servo(ser, i);
				ang = r.read_angle()
				print('Servo found at id ' + str(i) + ' at angle %.3f' % ang)
			except RuntimeError, e:
				pass
		ser.serial_io.close()
time.sleep(1)

servo_list = []