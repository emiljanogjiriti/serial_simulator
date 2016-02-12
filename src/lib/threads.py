
from time import clock
from threading import Thread
from data_structures import DataStructure
 
class Watchdog(Thread):
	
	def __init__(self):
		Thread.__init__(self)
		self.start()
		self.thread_alive = True

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

class SerialPrinter(Thread):
	
	def __init__(self, serial, DataStructure):
		Thread.__init__(self)
		self.thread_alive = True
		self.awaiting = False
		self.serial = serial
		self.data_structure = DataStructure
		self.start()

	def run(self):
		i = 0
		while (self.thread_alive and i < 2000):
			i += 1
			if self.serial is not None:
				incoming = self.serial.read(self.data_structure.get_output_packet_size())
				if incoming is not '':
					packet_formatting = self.data_structure.get_output_packet_formatting()
					if len(incoming) == self.data_structure.get_output_packet_size():
						print "Packet received: " + incoming
						#data_structure.printOutputPacket()

	def stop(self):
		self.thread_alive = False

	def listen(self):
		self.awaiting = True

class AutoTimer(Thread):
	
	def __init__(self, period=1, *events):
		Thread.__init__(self)
		self.thread_alive = True
		self.period = period
		self.event = events[0]
		self.start()

	def run(self):
		clock_start = clock()
		last_event = clock_start

		while (self.thread_alive):
			tick = clock()
			if (tick - last_event) > self.period:
				self.event()
				last_event += self.period
				print "event error = " + str(last_event - tick)

	def stop(self):
		self.thread_alive = False


class OneShotTimer(Thread):

	def __init__(self, event, timeout=1):
		Thread.__init__(self)
		self.timeout = timeout
		self.event = event
		self.start()

	def run(self):
		self.thread_alive = True
		clock_start = clock()
		last_event = clock_start

		while (self.thread_alive):
			if (clock() - last_event) > self.timeout:
				self.event()
				self.thread_alive = False

	def stop(self):
		self.thread_alive = False
