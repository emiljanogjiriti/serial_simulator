class IO:

	os_name = ""
	os_mac = "Mac"
	os_win = "Windows"
	os_linux = "Linux"

	getch_lib = None

	def __init__(self):

		print "Checking dependencies..."

		import platform

		if platform.mac_ver()[0] != '':
			self.os_name = self.os_mac
		elif platform.win32_ver()[0] != '':
			self.os_name = self.os_win
		elif platform.dist()[0] != '':
			self.os_name = self.os_linux

		print self.os_name + " platform detected"

		if self.os_name == self.os_win:
			import msvcrt
			self.getch_lib = msvcrt
		else:
			try:
				import getch
			except ImportError:
		   		from subprocess import call
		    	call(["python", "getch/setup.py", "install"])
		    	import getch
			self.getch_lib = getch

	def getch(self):
		return self.getch_lib.getch()