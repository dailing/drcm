from PyQt4 import QtCore

class PoolWrapper():
	def __init__(self):
		
		self.pool = QtCore.QThreadPool.globalInstance()
		self.pool.setMaxThreadCount(2)

	def start(self, worker):
		self.pool.start(worker)