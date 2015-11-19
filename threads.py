
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
				incoming = self.serial_rx.read(5)
				if incoming is not '':
					packet_formatting = 'BBBBB'
					if len(incoming) == struct.calcsize(packet_formatting):
						print "Packet received: " + incoming
						packet = struct.unpack(packet_formatting, incoming)
						print packet
						print "%.3f" %((packet[4] * 256 + packet[3]) * 5.0/1024)

	def stop(self):
		self.thread_alive = False

	def listen(self):
		self.awaiting = True

class Auto_timer(Thread):

	thread_alive = True
	period = 1
	
	def __init__(self, event, period=1):

		Thread.__init__(self)
		self.period = period
		self.event = event
		self.start()

	def run(self):

		clock_start = clock()
		clock_last = clock()

		while (self.thread_alive):
			if (clock_last - clock_start) > self.period:
				self.event()
				clock_start = clock_last
			else:
				clock_last = clock()

	def stop(self):

		self.thread_alive = False
