import sys
from wifi import Cell, Scheme

from PyQt4 import QtCore, QtGui
from time import sleep
from random import randint

import logging

class Worker(QtCore.QRunnable):
	def __init__(self, func, msgSignal):
		QtCore.QRunnable.__init__(self)
		self.func = func
		self.msgSignal = msgSignal

	def run(self):
		print('Running Worker')
		self.func()
		self.msgSignal.emit(randint(1, 20), [randint(5, 90), "fdjk"])

class PoolWrapper():
	def __init__(self):
		self.pool = QtCore.QThreadPool.globalInstance()
		self.pool.setMaxThreadCount(2)

	def start(self, worker):
		self.pool.start(worker)
		# self.pool.waitForDone()
		

class Task(QtCore.QObject):
	"""docstring for Task"""
	def __init__(self):
		super(Task, self).__init__()
		self.trigger = QtCore.pyqtSignal()

	def connect_and_emit(self):
		QtCore.QObject.connect(self, 
			QtCore.SIGNAL('sig()'), 
			self.handleTrigger)
		self.emit(QtCore.SIGNAL('sig()'))
	def handleTrigger(self):
		print('handler')

class Foo(object):
	pass

def printmsg(first):
	print('arg', first)
	sleep(2)
def defaultPrint():
	print('default')

class MyWidget(QtGui.QWidget):
	randSignal = QtCore.pyqtSignal(int, list)

	def __init__(self, parent=None):
		super(MyWidget, self).__init__(parent)
		task = Task()
		self.pw = PoolWrapper()
		
		self.hlayout = QtGui.QVBoxLayout()
		self.setLayout(self.hlayout)
		self.b = QtGui.QPushButton("Emit your signal!", self)
		self.label = QtGui.QLabel('ini')
		self.hlayout.addWidget(self.b)
		print(Cell.all('wlan0'))
		self.hlayout.addWidget(self.label)
		self.b.clicked.connect(self.clickHandler)
		self.randSignal.connect(self.mySignalHandler)

	def clickHandler(self):
		self.pw.start(Worker(printmsg, self.randSignal))
		
		
		# self.mysignal.emit(5, ["a", Foo(), 6])

	def mySignalHandler(self, n, l):
		print (n)
		print (l)
		self.label.setText(str(n) + str(l))


def caller(func, *arg):
	print(arg)
	func(*arg)

if __name__ == '__main__':
	pass
	cells = Cell.all('wlan0')
	print (cells[0].__dict__)
	for cell in cells :
		print (cell.address, str(cell.ssid))
	cell = cells[0]
	scheme = Scheme.for_cell('wlan0', 'home', cell, '12345678')
	try:
		scheme.activate()
	except Exception as e:
		logging.exception("error in network connection {}".format(cell.ssid))
		pass
	# app = QtGui.QApplication(sys.argv)
	# w = MyWidget()
	# w.show()
	# sys.exit(app.exec_())
	
# if __name__ == '__main__':
	# msgSignal = QtCore.pyqtSignal()
	# msgSignal.emit()
	

   