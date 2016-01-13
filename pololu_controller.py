import serial_manager
import struct

class PololuController(object):

	#baud_rate = 115200;
	serial_io = None
	position = 0 #centered

	def __init__(self, manager):
		print "Initializing Pololu motor controller"
		self.serial_io = manager

	def move_right(self):
		self.send_command(self.move(5))

	def move_left(self):
		self.send_command(self.move(-5))

	def move(self, adjustment):

		position = self.position

		position += adjustment
		if position < -50:
			position = -50
		if position > 50:
			position = 50

		self.position = position

		pololu_command = None

		print "Moving to " + str(position)

		if position >= 0:
			pololu_command = 0xE1
		else:
			pololu_command = 0xE0
			position = -position
		
		return struct.pack('B', pololu_command) + struct.pack('b', position)

	def send_command(self, command):
		self.serial_io.write(command)

	def add_menu_functions(self, dict):
		dict['a'] = self.move_left
		dict['d'] = self.move_right

