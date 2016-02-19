import struct
from collections import OrderedDict
from os import linesep as sep

class DataStructure:
	'''Preliminary structure to hold C struct data for microcontroller network
	'''
	#indices for location of values in to_dict and from_dict lists
	#_INDEX_NAME = 0 
	_INDEX_PACKING = 0
	_INDEX_VALUE = 1
	_PADDING = 5

	def __init__(self, delimiter):
		self.delimiter = delimiter
		self.to_dict = OrderedDict()
		self.from_dict = OrderedDict()

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
		'''returns true and packs data into struct if packet was large enough'''
		if(len(data) == self.from_struct.size):
			for dict_val, c_var in zip(self.from_dict.values(), self.from_struct.unpack(data)):
				dict_val[DataStructure._INDEX_VALUE] = c_var
			return True
		return False

	def get_outgoing_struct(self):
		return ''.join([self.delimiter, self.to_struct.pack(*map(lambda x: x[DataStructure._INDEX_VALUE], self.to_dict.values()))])

	def calculate_timeout(self, baudrate):
		return (self.to_struct.size + self.from_struct.size + DataStructure._PADDING) * 10.0 / baudrate

	def calc_structs(self):
		self.to_struct = struct.Struct(''.join([self.to_dict[key][0] for key in self.to_dict]))
		self.from_struct = struct.Struct(''.join([self.from_dict[key][0] for key in self.from_dict]))

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

with open('V2DT.h', 'r') as content_file:
	to_dict = {}
	from_dict = {}
	content = content_file.read()
	matches = re.findall(r'{([^{}]*)}', content)
	#print parse_into_dict(matches[0].split(), to_dict)
	#print parse_into_dict(matches[1].split(), from_dict)

v2_drivetrain = DataStructure('@V2DT')
v2_drivetrain.to_dict['speed1'] = ['B', ord('a')]
v2_drivetrain.to_dict['speed2'] = ['B', ord('b')]
v2_drivetrain.to_dict['status'] = ['B', ord('c')]
v2_drivetrain.from_dict['output'] = ['16s', "abcdefghijklmnop"]
v2_drivetrain.calc_structs()

mini_arm = DataStructure('@MARM')
mini_arm.to_dict['status'] = ['B', ord('d')]
mini_arm.from_dict['analogRead[8]'] = ['HHHHHHHH', 0] 
mini_arm.calc_structs()

if __name__ == '__main__':
	print 'unit testing...'

	#input to be packed is too short
	v2_drivetrain.pack_into_received('isthis16char???')
	assert v2_drivetrain.from_dict['output'][1] is 'abcdefghijklmnop'
	
	#input to be packed is too long
	v2_drivetrain.pack_into_received('isthis16char?????')
	assert v2_drivetrain.from_dict['output'][1] is 'abcdefghijklmnop'

	#input just right
	v2_drivetrain.pack_into_received('isthis16char????')
	assert v2_drivetrain.from_dict['output'][1] == 'isthis16char????'

	#default output
	assert v2_drivetrain.get_outgoing_struct() == '@V2DTabc'

	print 'all tests passed!'