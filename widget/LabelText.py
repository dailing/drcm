from PyQt4 import QtGui, QtCore

class LabelText(QtGui.QWidget):
	"""edit text box with label"""
	def __init__(self, label):
		super(LabelText, self).__init__()
		self.editText = QtGui.QLineEdit()
		layout = QtGui.QHBoxLayout()
		layout.addWidget(QtGui.QLabel(label))

		layout.addWidget(self.editText)
		self.setLayout(layout)

	def getText(self):
		return self.editText.text()

	def setText(self, text):
		self.editText.setText(text)