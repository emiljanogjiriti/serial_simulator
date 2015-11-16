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

	elif input == 'x' :
		ser.close()
		exit()