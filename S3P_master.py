import time
import serial
import msvcrt
import struct

ser = serial.Serial(
	port 		= 'COM10',
	#port='/dev/tty.usbserial-AL0151UO',
	baudrate 	= 57600,
	parity 		= serial.PARITY_NONE,
	stopbits 	= serial.STOPBITS_ONE,
	bytesize	= serial.EIGHTBITS,
	timeout 	= 1
)

motor_1 = 0
motor_2 = 0

serial_output = ''
special_char = False

def getch() :
	#needs different function for OSX, linux in future
	return msvcrt.getch()

input = 'A'

while 1 :
	input = getch()

	if ord(input) == 224 :
		input = getch()

		if ord(input) == 72 :
			motor_1 += 1
			motor_2 += 1
		elif ord(input) == 80 :
			motor_1 += -1
			motor_2 += -1
		elif ord(input) == 75 :
			motor_1 += +1
			motor_2 += -1
		elif ord(input) == 77 :
			motor_1 += -1
			motor_2 += +1

		print ord(str(input))
		serial_output = '@1' + struct.pack('b', motor_1) + struct.pack('b', motor_2)
		print '@1' + '[' + str(motor_1) + '][' + str(motor_2) + ']'
		ser.write(serial_output)

	elif input == 'x':
		ser.close()
		exit()