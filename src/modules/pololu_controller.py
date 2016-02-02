import serial_manager
import struct

class PololuController(object):

	#baud_rate = 115200;

	def __init__(self, manager, device_number, cw_key, ccw_key):
		print "Initializing Pololu motor controller"
		self.manager = manager
		self.device_number = device_number
		self.position = 0
		self.cw_key = cw_key
		self.ccw_key = ccw_key

	def move_right(self):
		self.send_command(self.move(2))

	def move_left(self):
		self.send_command(self.move(-2))

	def move(self, adjustment):

		position = self.position

		position += adjustment
		if position < -50:
			position = -50
		if position > 50:
			position = 50

		self.position = position

		print "Moving to " + str(position)

		if position >= 0:
			pololu_command = 0x61
		else:
			pololu_command = 0x60
			position = -position
		
		return struct.pack('BBBb', 0xAA, self.device_number, pololu_command, position)

	def send_command(self, command):
		print command
		#self.manager.acquire_mutex()
		self.manager.serial_io.write(command)
		#self.manager.release_mutex()

	def add_menu_functions(self, dict):
		dict[self.cw_key] = self.move_left
		dict[self.ccw_key] = self.move_right

