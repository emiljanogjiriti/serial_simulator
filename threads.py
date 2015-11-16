import setup
import random
from time import clock, sleep
from threading import Thread

io = setup.IO()
user_input = '';
 
class MyThread(Thread):

    def __init__(self, name):

        Thread.__init__(self)
        self.name = name
        self.start()

    def run(self):

        amount = random.randint(1, 5)
        sleep(amount)
        clock_start = clock()
        while (clock() - clock_start) > 1:
        	a = 1
        msg = "%s has finished!" % self.name
        print(msg)
 
def create_threads():

    for i in range(1):
        name = "Thread #%s" % (i+1)
        my_thread = MyThread(name=name)
 
if __name__ == "__main__":

	last_clock = clock()
	this_clock = clock()

	while user_input != 'q':

		user_input = io.getch()
		last_clock = this_clock
		this_clock = clock()

		print str(this_clock - last_clock) + ' seconds since last keypress'
		print user_input
		create_threads()