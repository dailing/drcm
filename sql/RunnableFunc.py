from PyQt4 import QtCore

class RunnableFunc(QtCore.QRunnable):
	def __init__(self, func, *arg):
		QtCore.QRunnable.__init__(self)
		self.func = func
		self.arg = arg

	def run(self):
		print('Running Worker')
		self.func(*self.arg)
		