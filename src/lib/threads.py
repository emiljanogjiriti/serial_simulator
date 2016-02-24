from __future__ import print_function
from __future__ import unicode_literals

from time import clock
from threading import Thread
 
class Watchdog(Thread):
	
	def __init__(self):
		Thread.__init__(self)
		self.start()
		self.thread_alive = True

	def run(self):
		clock_start = clock()
		clock_last = clock()

		while (self.thread_alive):
			if (clock_last - clock_start) > 1:
				print('TICK')
				clock_start = clock_last
			else:
				clock_last = clock()

	def stop(self):
		self.thread_alive = False

class AutoTimer(Thread):
	
	def __init__(self, period=1, events=None):
		Thread.__init__(self)
		self.period = period
		self.events = events
		self.finished_events = False
		self.alive = True
		print(events)

	def run(self):
		clock_start = clock()
		last_event = clock_start
		cei = 0 #current event index
		while (self.alive):
			tick = clock()
			if (tick - last_event) > self.period:
				last_event += self.period
				self.finished_events = False
				cei = 0
			if not self.finished_events:
				try:
					if (tick - last_event) > self.events[cei].time:
						self.events[cei].run()
						cei += 1
				except IndexError:
					self.finished_events = True

	def kill(self):
		self.alive = False

class EventWrapper:
	def __init__(self, event, time=0):
		self.time = time
		self.event = event

	def run(self):
		self.event()

if __name__ == '__main__':
	def ev0():
		print('start of events')
	def ev1():
		print('ohe yes')
	e0 = EventWrapper(ev0)
	e1 = EventWrapper(ev1, time=0.001)

	a = AutoTimer(events=[e0, e1], period=1.0)
	a.start()

	try:
		while True:
			pass
	except KeyboardInterrupt:
		a.kill()
		a.join()
		quit(0)