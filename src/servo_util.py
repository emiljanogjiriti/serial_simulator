#!/usr/bin/python
'''
@author: Max Prokopenko
@email : max@embeddedprofessional.com
@github: https://github.com/maxlazarus
'''
from __future__ import print_function
from __future__ import unicode_literals
if 'raw_input' not in dir(__builtins__): raw_input = input
import os
from os import path
from os import sep
import time
import sys
from opbots import *

ser = SerialManager()

current_baudrate = 115200
start_id = 0
end_id = 10
servo_list = []

def select_baudrate():
	baudrates = [1000000, 500000, 400000, 250000, 200000, 115200, 57600, 19200, 9600]
	print("Select a baudrate")
	for baudrate in baudrates :
		print(str(baudrate) + ' bps')	
	current_baudrate = raw_input()
	print(str(current_baudrate)+' selected as baudrate')
	if int(current_baudrate) not in baudrates:
		print('Incorrect baudrate selected')

def open_port():
	print('Select a port to open')
	ser.list_ports()
	selected_port = raw_input();
	try:
		ser.open_port(int(selected_port),current_baudrate)
	except KeyError:
		print('"'+str(selected_port)+'" is not a valid port')

def find_servos():
	global servo_list
	servo_list = []
	for i in range(start_id, end_id+1):
		print('scanning servo at id ' + str(i))
		try:
			r = RobotisServo(ser, i);
			ang = r.read_angle()
			servo_list.append(r)
			print('Servo found at id ' + str(i) + ' at angle %.3f' % ang)
		except RuntimeError as e:
			print(e)
			pass

def exit(): quit()

def move_servo_to():
	print('Choose servo')
	for i,servo in enumerate(servo_list):
		print('['+str(i)+']'+str(servo_list[i]))
	servo_num = raw_input()
	print('Enter angle')
	servo_angle = raw_input()
	try:
		servo_list[int(servo_num)].move_to_encoder(int(servo_angle))
	except IndexError:
		print('Servo index out of range in servo_list')
	except ValueError:
		print('"'+str(servo_num)+'" is not a valid index')

def read_servo_encoder():
	print('Choose servo')
	for i,servo in enumerate(servo_list):
		print('['+str(i)+']'+str(servo_list[i]))
	servo_num = raw_input()
	try:
		print('Servo at '+str(servo_list[int(servo_num)].read_encoder()))
	except IndexError:
		print('Servo index out of range in servo_list')
	except ValueError:
		print('"'+str(servo_num)+'" is not a valid index')

user_input = ''
function_dict = {}
function_dict['f'] = find_servos
function_dict['q'] = exit
function_dict['re'] = read_servo_encoder
function_dict['m'] = move_servo_to
function_dict['s'] = select_baudrate
function_dict['o'] = open_port

while user_input not in ['q','Q','quit','exit']:
	print('Select option')
	for k in function_dict.keys():
		print('['+str(k)+']:'+str(function_dict[k].__name__	))
	user_input = raw_input()
	try:
		function_dict[user_input]()
	except KeyError:
		print('"'+str(user_input)+'" is an invalid selection')