import thread
import threads
import serial
import serial.tools.list_ports
import sys
import struct

class SerialManager(object):

    def __init__(self):
        self.port_blacklist = ["ttyS", "COM35"] #ignore internal linux ports, bad bluetooth
        self.find_ports()
        self.mutex = thread.allocate_lock()
        print ""
        print "Initializing serial manager..."
        self.counter = 0

    def open_port(self, user_input, baud):
        '''
        wrapper around the pyserial class Serial
        '''
        self.acq_mutex()
        try:
            self.user_port = self.ports[int(user_input)][0]
            print "Attempting to connect to port " + self.user_port + "..."
            self.serial_io = serial.Serial(
                port        = self.user_port,
                baudrate    = baud,
                parity      = serial.PARITY_NONE,
                stopbits    = serial.STOPBITS_ONE,
                bytesize    = serial.EIGHTBITS,
                xonxoff     = False,
                timeout     = 0.5,
                writeTimeout = None
            )
            print ""
            print "Connected"
            self.rel_mutex()
            return True
        except serial.serialutil.SerialException:
            print ""
            print "Connection failed"   
            self.rel_mutex()
            return False

    def acq_mutex(self):
        #print('Acquiring mutex')
        self.mutex.acquire()

    def rel_mutex(self):
        #print('Releasing mutex')
        self.mutex.release()

    def receive_into(self, data_structure):
        '''
        Attempts to load the received serial data into a c-like struct
        @returns True if successful
        '''
        if self.serial_io is not None:
                if self.serial_io.in_waiting == data_structure.from_struct.size:
                    return data_structure.pack_into_received(self.serial_io.read(data_structure.from_struct.size))
        self.serial_io.reset_input_buffer()
        return False

    def write(self, message):
        self.counter += 1
        self.counter = self.counter % 128
        if self.serial_io is not None:
            self.serial_io.write(message)

    def read_serial(self, nBytes=1):
        # It is up to the caller to acquire / release mutex
        rep = self.serial_io.read( nBytes )
        return rep

    def start_serial_printer(self):
        DataStructure = data_structures.v2_drivetrain
        print "Starting serial printer listening to " + DataStructure.delimiter + " on " + self.user_port
        self.serial_printer = threads.SerialPrinter(self.serial_io, DataStructure)

    def find_ports(self):
        '''
        Finds all the connected ports and saves them to self.ports
        Called by constructor
        '''
        self.ports = list(serial.tools.list_ports.comports())
        dead_ports = list()
        for port in self.ports:
            if any(x in port[1] for x in self.port_blacklist):
                dead_ports.append(port)
        for port in dead_ports:
            self.ports.remove(port)
        return self.ports

    def list_ports(self):
        for i in xrange(len(self.ports)):
            print "[" + str(i) + "] " + self.ports[i][0]

    def close(self):
        try:
            self.serial_printer.stop()
        except AttributeError:
            pass

if __name__ == '__main__':
    ser = SerialManager()
    ser.list_ports()