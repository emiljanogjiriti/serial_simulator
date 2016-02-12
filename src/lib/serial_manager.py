import thread
import threads
import serial
import serial.tools.list_ports
import sys
import data_structures
import struct

class SerialManager(object):

	user_input = None
	user_port = None
	user_baud = None
	serial_io = None
	watchdog = None
	auto_timer = None
	serial_printer = None
	ports = None

	def __init__(self):
		print ""
		print "Initializing serial manager..."
		self.counter = 0

	def open_port(self, user_input, baud):

		self.mutex = thread.allocate_lock()
		self.acquire_mutex()

		try:
			self.user_port = self.ports[int(user_input)][0]
			print ""
			print "Attempting to connect to port " + self.user_port + "..."
			self.serial_io = serial.Serial(
				port 		= self.user_port,
				baudrate 	= baud,
				parity 		= serial.PARITY_NONE,
				stopbits 	= serial.STOPBITS_ONE,
				bytesize	= serial.EIGHTBITS,
				xonxoff 	= False,
				timeout 	= 0.1,
				writeTimeout = 0.1
			)
			print ""
			print "Connected"
			return True

		except serial.serialutil.SerialException:
			print ""
			print "Connection failed"	
			return False	

		except Exception as e:
			sys.exc_clear()
			return False
		self.release_mutex()

	def acquire_mutex(self):
		self.mutex.acquire()

	def release_mutex(self):
		self.mutex.release()

	def receive_into(self, data_structure):
		if self.serial_io is not None:
				incoming = self.serial_io.read(data_structure.get_output_packet_size())
				if incoming is not '':
					return data_structure.pack_into_received(incoming)
		return False

	def write(self, message):
		self.counter += 1
		self.counter = self.counter % 128
		if self.serial_io is not None:
			self.serial_io.write(message)

	def toggle_watchdog(self):
		if self.watchdog is None:
			print "Starting watchdog..."
			self.watchdog = threads.Watchdog()
		else:
			print "Stopping watchdog..."
			self.watchdog.stop()
			self.watchdog = None

	def start_serial_printer(self):
		DataStructure = data_structures.v2_drivetrain
		print "Starting serial printer listening to " + DataStructure.delimiter + " on " + self.user_port
		self.serial_printer = threads.SerialPrinter(self.serial_io, DataStructure)

	def list_ports(self):
		self.ports = list(serial.tools.list_ports.comports())
		dead_ports = list()
		'''following 5 lines are to prevent Linux machines from showing non-USB ports'''
		for port in self.ports:
			if "ttyS" in port[1]:
				dead_ports.append(port)
		for port in dead_ports:
			self.ports.remove(port)
		for i in xrange(len(self.ports)):
			print "[" + str(i) + "] " + self.ports[i][0]

	def close(self):
		if self.watchdog is not None:
			self.watchdog.stop()
		if self.serial_printer is not None:
			self.serial_printer.stop()
		if self.auto_timer is not None:
			self.auto_timer.stop()

	def add_menu_functions(self, dict):
		if self.serial_io is not None:
			dict['p'] = self.start_serial_printer
			#dict['w'] = self.toggle_watchdog
			dict[' '] = self.write
			#dict['a'] = self.start_auto_timer