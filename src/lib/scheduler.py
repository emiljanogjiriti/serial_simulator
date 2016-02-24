'''@author: max@embeddedprofessional.com'''
from __future__ import print_function
from __future__ import unicode_literals
from multiprocessing import Process, Queue
from time import clock
from time import sleep

class Scheduler(Process):
	'''Schedules period or oneshot events'''

	def __init__(self, periodic_queue=None, oneshot_queue=None, period=1):
		Process.__init__(self, name='')
		self.period = period
		self.event_list = []
		self.periodic_queue = periodic_queue
		self.advanced = False
		print(periodic_queue)
		while not periodic_queue.empty():
			new_event = self.periodic_queue.get(True)
			self.add_periodic(new_event, 0.1)

	def add_periodic(self, event, time):
		self.event_list.append([event, time])

	def add_oneshot(self, event):
		return NotImplemented

	def pending_event_time(self):
		if not self.advanced:
			return self.event_list[0][1]
		else:
			return 10000

	def trigger_pending_event(self):
		self.event_list[0][0].do()

	def advance(self):
		self.advanced = True

	def run(self):
		clock_start = clock()
		last_event = clock_start

		while (self.is_alive()):
			tick = clock()
			if (tick - last_event) > self.period:
				last_event += self.period
				self.advanced = False
				print('Scheduler mark at ' + str(last_event))
			if (tick - last_event) > self.pending_event_time():
				self.trigger_pending_event()
				self.advance()

class Test1(object):
	
	def change_message(self, message):
		self.message = message

	def do(self):
		try:
			print(self.message)
		except AttributeError:
			print(str(self.__class__) + ' attribute error')

if __name__ == '__main__':
	print('Unit tests for ' + __file__)
	
	periodic = Queue()
	oneshot = Queue()

	test1 = Test1()
	periodic.put(test1)

	s = Scheduler(periodic_queue=periodic, oneshot_queue=oneshot, period=1)
	#s.add_repeated(test1, 0.1)

	try:
		s.start()
		user_in = ''
		while(user_in not in ['quit','q','exit']):
			test1.change_message(raw_input())
			print(test1.message)
	except KeyboardInterrupt:
		s.terminate()