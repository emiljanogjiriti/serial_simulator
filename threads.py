
from time import clock
from threading import Thread
import struct
 
class Watchdog(Thread):

	thread_alive = True
	
	def __init__(self):

		Thread.__init__(self)
		self.start()

	def run(self):

		clock_start = clock()
		clock_last = clock()

		while (self.thread_alive):
			if (clock_last - clock_start) > 1:
				print 'TICK'
				clock_start = clock_last
			else:
				clock_last = clock()

	def stop(self):

		self.thread_alive = False

class Serial_printer(Thread):

	thread_alive = True
	serial_rx = None
	awaiting = False
	
	def __init__(self, serial):

		Thread.__init__(self)
		self.start()
		self.serial_rx = serial

	def run(self):

		while (self.thread_alive):
			if self.serial_rx is not None:
				incoming = self.serial_rx.read()
				if incoming is not '':
					packet = struct.unpack('B', incoming)
					print packet[0]

	def stop(self):
		self.thread_alive = False

	def listen(self):
		self.awaiting = True