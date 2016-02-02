from serial_manager import SerialManager as ser
from data_structures import v2_drivetrain as v
s = ser()
s.list_ports()
s.open_port(0, 230400)
s.start_serial_printer(v)