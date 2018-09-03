from PyQt4 import QtGui, QtCore

def setLabelStyle(label):
	label.setAlignment(QtCore.Qt.AlignCenter)
	label.setStyleSheet("QLabel{color:black;font-size:24px}"
		);

class LabelPair(QtGui.QWidget):
	"""edit text box with label"""
	def __init__(self, key, value):
		QtGui.QWidget.__init__(self)
		
		layout = QtGui.QHBoxLayout()
		labelWidget = QtGui.QLabel(key)
		setLabelStyle(labelWidget)
		layout.addWidget(labelWidget, 1)

		labelWidget = QtGui.QLabel(":")
		setLabelStyle(labelWidget)
		layout.addWidget(labelWidget)

		editableLabel = QtGui.QLabel(value)
		setLabelStyle(editableLabel)
		layout.addWidget(editableLabel, 8)
		editableLabel.setAlignment(QtCore.Qt.AlignLeft)
		layout.addStretch(1)
		self.setLayout(layout)

		self.editText = editableLabel

	def getText(self):
		return self.editText.text()

	def setText(self, text):
		self.editText.setText(text)