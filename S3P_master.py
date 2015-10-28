import time
import serial
import serial.tools.list_ports
import msvcrt
import struct
import platform
import Queue
import threading

print platform.system() + " system detected"

ports = list(serial.tools.list_ports.comports())
prompt = "Select a port or press 'q' to quit"

for i in xrange(len(ports)):
    print "[" + str(i) + "] " + ports[i][0]

print prompt

def getch() :
	#needs different function for OSX, linux in future
	return msvcrt.getch()

user_input = getch()
user_port = ""

while user_input != 'q':
	try:
		user_port = ports[int(user_input)][0]
		print "Attempting to connect to port " + user_port + "..."
		ser = serial.Serial(
			port 		= user_port,
			baudrate 	= 115200,
			parity 		= serial.PARITY_NONE,
			stopbits 	= serial.STOPBITS_ONE,
			bytesize	= serial.EIGHTBITS,
			timeout 	= 1,
			writeTimeout = 1
		)
	except Exception:
		print "Connection failed"
	finally:
		print prompt
		user_input = getch()

class ClientThread (threading.Thread):

	def run (self):

		while True:

			client = clientPool.get()

			if client != None:
				print "client received: " + str(client)

clientPool = Queue.Queue ( 0 )

ClientThread().start()
for thread in threading.enumerate():
	clientPool.put(thread)

threading.enumerate()[0].join(5.0)

quit()

#below is working towards instantaneous motor contorl

motor_1 = 0
motor_2 = 0

serial_output = ''
special_char = False

input = '0'

while 1:
	input = getch()

	if ord(input) == 224:
		input = getch()

		if ord(input) == 72: # up arrow
			motor_1 += 2
			motor_2 += 2
		elif ord(input) == 80: # down arrow
			motor_1 += -2
			motor_2 += -2
		elif ord(input) == 75: # left arrow
			motor_1 += -2
			motor_2 += +2
		elif ord(input) == 77: # right arrow
			motor_1 += +2
			motor_2 += -2

		print ord(str(input))
		serial_output = '@1' + struct.pack('b', motor_1) + struct.pack('b', motor_2)
		print '@1' + '[' + str(motor_1) + '][' + str(motor_2) + ']'
		ser.write(serial_output)
	#elif input == 's' :
	#	print 'Stopping...'
	#	motor_1 = 0
	#	motor_2 = 0
	#	serial_output = '@1' + struct.pack('b', motor_1) + struct.pack('b', motor_2)
	#	ser.write(serial_output)
	elif input == 'x' :
		ser.close()
		exit()