import serial_manager
import struct

class PololuController(object):

	#baud_rate = 115200;

	def __init__(self, manager, device_number):
		print "Initializing Pololu motor controller"
		self.manager = manager
		self.device_number = device_number
		self.position = 0

	def move_to(self, position):

		if position < -50:
			position = -50
		if position > 50:
			position = 50

		print "Moving to " + str(position)

		if position >= 0:
			pololu_command = 0x61
		else:
			pololu_command = 0x60
			position = -position
		
		self.send_command(struct.pack('BBBb', 0xAA, self.device_number, pololu_command, position))

	def send_command(self, command):
		self.manager.acq_mutex()
		self.manager.serial_io.write(command)
		self.manager.rel_mutex()

