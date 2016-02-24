'''@author: max@embeddedprofessional.com'''
from __future__ import print_function
from __future__ import unicode_literals
from multiprocessing import Process, Queue
from time import clock
from time import sleep

class Scheduler(Process):
	'''Schedules repeated or oneshot events'''

	def __init__(self, queue=None, period=1):
		Process.__init__(self, name='')
		self.period = period
		self.event_list = []
		self.queue = queue
		self.advanced = False
		print(queue)
		while not queue.empty():
			new_event = self.queue.get(True)
			self.add_repeated(new_event, 0.1)

	def add_repeated(self, event, time):
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
	def do(self):
		print('Yay')

if __name__ == '__main__':
	print('Unit tests for ' + __file__)
	
	q = Queue()
	test1 = Test1()
	q.put(test1)

	s = Scheduler(queue=q, period=1)
	#s.add_repeated(test1, 0.1)

	try:
		s.start()
	except KeyboardInterrupt:
		s.terminate()