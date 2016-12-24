#!/usr/bin/python
from __future__ import print_function
from __future__ import unicode_literals
import time
from opbots import*

ser = serial_manager.SerialManager()
ser.list_ports()
ser.open_port(0,9600)
while True:
	ser.write(str('Hello'))
	time.sleep(0.01)
