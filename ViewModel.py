from PyQt4 import QtGui

class ViewModel(QtGui.QStandardItemModel):
	"""list view model"""
	def __init__(self):
		super(ViewModel, self).__init__()
		pass

	def pushBack(self, data):
		self.appendRow(QtGui.QStandardItem(data))

	def pushFront(self, data):
		self.insertRow(0, QtGui.QStandardItem(data))