from PyQt4 import QtGui, QtCore

def setLabelStyle(label):
	label.setAlignment(QtCore.Qt.AlignCenter)
	label.setStyleSheet("QLabel{color:black;font-size:24px}"
		);

class LabelDate(QtGui.QWidget):
	"""edit text box with label"""
	def __init__(self, label):
		QtGui.QWidget.__init__(self)
		dateEdit = QtGui.QDateTimeEdit()
		dateEdit.setDisplayFormat("yyyy.MM.dd")
		dateEdit.setCalendarPopup(True)
		dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
		dateEdit.setStyleSheet("QDateTimeEdit{color:black;font-size:24px}"
		);
		self.datetime = dateEdit
		layout = QtGui.QHBoxLayout()
		
		labelWidget = QtGui.QLabel(label)
		setLabelStyle(labelWidget)
		layout.addWidget(labelWidget)

		layout.addWidget(self.datetime)
		self.setLayout(layout)

	def getTime(self):
		return self.datetime.dateTime().toString("yyyy-MM-dd")



if __name__ == '__main__':
	dt = QtCore.QDateTime.currentDateTime()
	print(dt.toString("yyyy-MM-dd"))