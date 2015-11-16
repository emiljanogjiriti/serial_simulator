import threads
import setup
import serial.tools.list_ports
import serial
import random
import struct
io = setup.IO()

ports = list(serial.tools.list_ports.comports())
prompt = "Select a port, press '?' to test or press 'q' to quit"

for i in xrange(len(ports)):
    print "[" + str(i) + "] " + ports[i][0]

print prompt

user_input = None
user_port = None

alive = True
ser = None

watchdog = None
serial_printer = None

while alive:

	user_input = io.getch()

	try:
		user_port = ports[int(user_input)][0]
		print "Attempting to connect to port " + user_port + "..."
		ser = serial.Serial(
			port 		= user_port,
			baudrate 	= 250000,
			parity 		= serial.PARITY_NONE,
			stopbits 	= serial.STOPBITS_ONE,
			bytesize	= serial.EIGHTBITS,
			timeout 	= 0.01,
			writeTimeout = 0.01
		)
		serial_printer = threads.Serial_printer(ser)

	except serial.serialutil.SerialException:
		print "Connection failed"
		print prompt
	except ValueError:
		a = None

	if user_input is 'w':
		print 'Starting watchdog...'
		threads.Watchdog()

	if user_input is '?':
		R = random.randint(-128, 127)
		G = random.randint(-128, 127)
		B = random.randint(-128, 127)
		color = struct.pack('b', R) + struct.pack('b', G) + struct.pack('b', B)
		ser.write('@RGB' + color)

	if user_input is 'q':
		alive = False

if watchdog is not None:
	watchdog.stop()
if serial_printer is not None:
	serial_printer.stop()