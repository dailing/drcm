from PyQt4 import QtGui, QtCore

class LabelDate(QtGui.QWidget):
	"""edit text box with label"""
	def __init__(self, label : str):
		super(LabelDate, self).__init__()
		dateEdit = QtGui.QDateTimeEdit()
		dateEdit.setDisplayFormat("yyyy.MM.dd")
		dateEdit.setCalendarPopup(True)
		dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
		self.datetime = dateEdit
		layout = QtGui.QHBoxLayout()
		layout.addWidget(QtGui.QLabel(label))

		layout.addWidget(self.datetime)
		self.setLayout(layout)

	def getTime(self):
		return self.datetime.dateTime()