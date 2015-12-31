import numpy
import matplotlib.pyplot as pyplot
import matplotlib.animation as animation
import time


def update_line(num, data, line):
    line.set_data(data[..., :num])
    return line,

fig1 = pyplot.figure()

data_file = open("data.txt", 'r')
print data_file.name
data = []

for line in data_file.readlines():
	try:
		trimmed_line = line.rstrip()
		data.append(trimmed_line.split(','))
	except Exception as e:
		print e

print data
print data.pop(0)

processed_data = []

display_data = numpy.array(numpy.float32(data)).transpose()

print display_data
print display_data.dtype

l, = pyplot.plot([], [], 'r-')
pyplot.xlim(0, 1)
pyplot.ylim(0, 1)
pyplot.xlabel('x')
pyplot.title('test')
line_ani = animation.FuncAnimation(fig1, update_line, 9, fargs=(display_data, l),
                                   interval=50, blit=True)
#line_ani.save('lines.mp4')

"""

fig2 = pyplot.figure()

x = numpy.arange(-9, 10)
y = numpy.arange(-9, 10).reshape(-1, 1)
base = numpy.hypot(x, y)
ims = []
for add in numpy.arange(15):
    ims.append((pyplot.pcolor(x, y, base + add, norm=pyplot.Normalize(0, 30)),))

im_ani = animation.ArtistAnimation(fig2, ims, interval=50, repeat_delay=3000,
                                   blit=True)
"""
#im_ani.save('im.mp4', metadata={'artist':'Guido'})

pyplot.show()
