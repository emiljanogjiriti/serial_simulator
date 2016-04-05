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

ser.list_ports()

for i, port in enumerate(ser.ports):
	if ser.open_port(i, 1000000):
		print('Scanning at 1 Mbps')
		for i in range(1, 10):
			try:
				r = Robotis_Servo(ser, i);
				ang = r.read_angle()
				print('Servo found at id ' + str(i) + ' at angle %.3f' % ang)
			except RuntimeError, e:
				pass
		ser.serial_io.close()
time.sleep(1)

servo_list = []

for i, port in enumerate(ser.ports):
	if ser.open_port(i, 115200):
		print('Scanning at 115.2 Kbps')
		for i in range(1, 10):
			try:
				r = Robotis_Servo(ser, i);
				servo_list.append(r)
				ang = r.read_angle()
				print('Servo found at id ' + str(i) + ' at angle %.3f' % ang)
			except RuntimeError, e:
				pass
		ser.serial_io.close()