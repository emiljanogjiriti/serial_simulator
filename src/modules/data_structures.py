import struct
from collections import OrderedDict
from os import linesep as sep

class CVariable:
	def __init__(self, name, formatting, length=1):
		self.name = name
		self.string_type = True if formatting == 's' else False
		array_qualifier = str(length) if length > 1 else ''
		self.formatting = array_qualifier + formatting
		self.data = None
		self._length = length

	def __len__(self):
		return self._length

class DataStructure(object):
	'''Preliminary structure to hold C struct data for microcontroller network
	'''
	_PADDING = 5

	def __init__(self, delimiter):
		self.delimiter = delimiter
		self.to_dict = OrderedDict()
		self.from_dict = OrderedDict()

	def __getattr__(self, name):
		if name not in ['delimiter', 'to_dict', 'from_dict', 'to_struct', 'from_struct']:
			return self.from_dict[name].data

	def __setattr__(self, name, value):
		if name not in ['delimiter', 'to_dict', 'from_dict', 'to_struct', 'from_struct']:
			self.to_dict[name].data = value
		else:
			self.__dict__[name] = value

	def __repr__(self):
		#[str(self.delimiter), 
		outputs = sep.join([str(key) 
				+ ': ' + str(self.to_dict[key][DataStructure._INDEX_VALUE]) 
				for key in self.to_dict])
		inputs = sep.join([str(key) 
				+ ': ' + str(self.from_dict[key][DataStructure._INDEX_VALUE]) 
				for key in self.from_dict])
		return sep.join([self.delimiter, 
				'--Outputs--', outputs, '--Inputs--', inputs])

	def pack_into_received(self, data):
		'''
		returns true and packs data into struct if packet was large enough
		'''
		if(len(data) == self.from_struct.size):
			unpacked = self.from_struct.unpack(data)
			lslice = 0
			for c_var in self.from_dict.values():
				rslice = lslice + len(c_var)
				data_tuple = unpacked[lslice:rslice]
				c_var.data = data_tuple[0] if len(c_var) == 1 or c_var.string_type else data_tuple
				lslice = rslice
			return True
		return False

	def get_outgoing_struct(self):
		outgoing = (c_var.data for c_var in self.to_dict.values())
		return ''.join([self.delimiter, self.to_struct.pack(*outgoing)])

	def calculate_timeout(self, baudrate):
		return (self.to_struct.size + self.from_struct.size + DataStructure._PADDING) * 10.0 / baudrate

	def calc_structs(self):
		'''
		sets structs for outgoing and incoming data from external bus
		'''
		to_formatting = ''.join([c_var.formatting for c_var in self.to_dict.values()])
		self.to_struct = struct.Struct(to_formatting)
		from_formatting = ''.join([c_var.formatting for c_var in self.from_dict.values()])
		self.from_struct = struct.Struct(from_formatting)

	def set_inputs(self, *args):
		for c_var in args:
			self.to_dict[c_var.name] = c_var

	def set_outputs(self, *args):
		for c_var in args:
			self.from_dict[c_var.name] = c_var

def get_packing(x):
	type_dict = {}
	type_dict['uint8_t'] = 'B'
	return type_dict[x]

import re

def parse_into_dict(pair_list, c_struct):
	'''parses struct literals into dict type
	returns format of struct'''
	array_re = re.compile(r'\[([0-9]+)\]')
	for i in enumerate(pair_list[1::2]):
		print i[1]
		m = array_re.search(i[1])
		if m is not None: print m.group(0)
		#if array_re.match(t) is not None: print '!'
	return 'b'

	#print ''.join(map(get_packing, to_list[1]))
'''
with open('V2DT.h', 'r') as content_file:
	to_dict = {}
	from_dict = {}
	content = content_file.read()
	matches = re.findall(r'{([^{}]*)}', content)
	#print parse_into_dict(matches[0].split(), to_dict)
	#print parse_into_dict(matches[1].split(), from_dict)
'''
uint8_t = 'B'
uint16_t = 'H'
string_t = 's'

v2_drivetrain = DataStructure('@V2DT')
v2_drivetrain.set_inputs(
		CVariable('speed1', uint8_t),
		CVariable('speed2', uint8_t),
		CVariable('status', uint8_t))
v2_drivetrain.set_outputs(
		CVariable('output', string_t, 16))
v2_drivetrain.calc_structs()

mini_arm = DataStructure('@MARM')
mini_arm.set_inputs(
		CVariable('status', uint8_t))
mini_arm.set_outputs(
		CVariable('voltages', uint16_t, 8), 
		CVariable('test', uint8_t))
mini_arm.calc_structs()

if __name__ == '__main__':
	print 'unit testing...'

	#correct at first, input to be packed is too short
	v2_drivetrain.pack_into_received('thisis16char!!!!')
	v2_drivetrain.pack_into_received('isthis16char???')
	assert v2_drivetrain.output == 'thisis16char!!!!'
	
	#input to be packed is too long
	v2_drivetrain.pack_into_received('isthis16char?????')
	assert v2_drivetrain.output == 'thisis16char!!!!'

	#default output
	v2_drivetrain.speed1 = 1
	v2_drivetrain.speed2 = 255
	v2_drivetrain.status = ord('k')
	assert v2_drivetrain.get_outgoing_struct() == '@V2DT\x01\xFFk'

	#multiple values
	mini_arm.pack_into_received('\x01\x00\x02\x00\x03\x00\x04\x00\x05\x00\x06\x00\x07\x00\x08\x00y')
	assert mini_arm.voltages == (1, 2, 3, 4, 5, 6, 7, 8)
	assert mini_arm.test == ord('y')

	print 'all tests passed!'