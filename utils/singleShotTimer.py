from PyQt4 import QtCore

class SingleShotTimer():
	def __init__(self):
		self.timer = QtCore.QTimer()
		self.timer.setSingleShot(True)

	def connect(self, qobj, func):
		qobj.connect(self.timer, QtCore.SIGNAL('timeout()'), func)

	def start(self, msec):
		self.timer.start(msec)
		