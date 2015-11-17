import threads
import setup
import serial.tools.list_ports
import serial
import random
import struct
io = setup.IO()

user_input = None
user_port = None

alive = True
ser = None

watchdog = None
serial_printer = None

def toggle_watchdog(serial=None):
	global watchdog
	if watchdog is None:
		print 'Starting watchdog...'
		watchdog = threads.Watchdog()
	else:
		print 'Stopping watchdog...'
		watchdog.stop()
		watchdog = None

def quit(serial=None): 
	global alive
	alive = False

def start_serial_printer(serial):
	global serial_printer
	serial_printer = threads.Serial_printer(serial)

function_dict = {
	'w':toggle_watchdog,
	'q':quit,
	'p':start_serial_printer
	}

print "Select a port to connect to or a menu option below"
print ""

ports = list(serial.tools.list_ports.comports())

for i in xrange(len(ports)):
    print "[" + str(i) + "] " + ports[i][0]

for key in function_dict.keys():
	print "[" + key + "] " + function_dict[key].__name__

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

	except serial.serialutil.SerialException:
		print "Connection failed"
		print function_dict

	except ValueError:
		a = None

	try:
		function_dict[user_input](ser)
		print "'" + user_input + "' pressed"
	except KeyError:
		print 'No command for that key'

if watchdog is not None:
	watchdog.stop()
if serial_printer is not None:
	serial_printer.stop()