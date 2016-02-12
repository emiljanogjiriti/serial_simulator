import struct
'''		while (self.thread_alive):
			if self.serial_rx is not None:
				incoming = self.serial_rx.read(5)
				if incoming is not '':
					packet_formatting = 'BBBBB'
					if len(incoming) == struct.calcsize(packet_formatting):
						print "Packet received: " + incoming
						packet = struct.unpack(packet_formatting, incoming)
						print packet
						print "%.3f" %((packet[4] * 256 + packet[3]) * 5.0/1024)
'''

class DataStructure:
	'''Preliminary structure to hold C struct data for microcontroller network
	'''
	#indices for location of values in dataIn and dataOut lists
	name = 0 
	packing_type = 1
	current_value = 2
	PADDING = 5

	def __init__(self, delimiter):
		self.delimiter = delimiter
		self.dataIn = []
		self.dataOut = []

	def get_input_packet_formatting(self):
		packet_formatting = ''
		for variable in self.dataIn:
			packet_formatting += variable[DataStructure.packing_type]
		return packet_formatting

	def get_input_packet_size(self):
		return struct.calcsize(self.get_input_packet_formatting())

	def get_output_packet_formatting(self):
		packet_formatting = ''
		for variable in self.dataOut:
			packet_formatting += variable[DataStructure.packing_type]
		return packet_formatting

	def get_output_packet_size(self):
		return struct.calcsize(self.get_output_packet_formatting())

	def pack_into_received(self, data):
		packet_formatting = self.get_output_packet_formatting()
		if len(data) == self.get_output_packet_size():
			print "Length of packet good"
			return True
		print "Length of packet bad"
		return False

	def print_received_struct(self):
		for variable in self.dataOut:
			print variable

	def get_outgoing_struct(self):
		output = self.delimiter
		for variable in self.dataIn:
			output += struct.pack(variable[DataStructure.packing_type], variable[DataStructure.current_value])
		return output

	def calculate_timeout(self, baudrate):
		return (self.get_input_packet_size() + self.get_output_packet_size() + DataStructure.PADDING) * 10 / baudrate

'''
volatile struct dataIn
{
	uint8_t speed1;
	uint8_t speed2;
	uint8_t status;
} dataIn;

volatile struct dataOut
{
	char output[16];
} dataOut;

'''

v2_drivetrain = DataStructure('@V2DT')
v2_drivetrain.dataIn.append(['speed1', 'B', ord('a')])
v2_drivetrain.dataIn.append(['speed2', 'B', ord('b')])
v2_drivetrain.dataIn.append(['status', 'B', ord('c')])
v2_drivetrain.dataOut.append(['output', '16s', "abcdefghijklmnop"])

mini_arm = DataStructure('@MARM')
mini_arm.dataIn.append(['status', 'B', ord('d')])
mini_arm.dataOut.append(['analogReadings', 'H', 0])