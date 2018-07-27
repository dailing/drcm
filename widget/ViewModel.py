from PyQt4 import QtGui

class ViewModel(QtGui.QStandardItemModel):
	"""list view model"""
	def __init__(self):
		QtGui.QStandardItem.__init__(self)
		pass

	def pushBack(self, data):
		self.appendRow(QtGui.QStandardItem(data))

	def pushFront(self, data):
		self.insertRow(0, QtGui.QStandardItem(data))