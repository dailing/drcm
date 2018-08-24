from PyQt4 import QtGui, QtCore
import subprocess

from MatchBoxLineEdit import MatchBoxLineEdit

def setLabelStyle(label):
	label.setAlignment(QtCore.Qt.AlignCenter)
	label.setStyleSheet("QLabel{color:black;font-size:24px}"
		);

def setEditTextStyle(widget) :
	widget.setAlignment(QtCore.Qt.AlignCenter)
	widget.setStyleSheet("QWidget{color:black;font-size:24px}"
		);

class LabelText(QtGui.QWidget):
	"""edit text box with label"""
	def __init__(self, label):
		QtGui.QWidget.__init__(self)
		
		self.editText = MatchBoxLineEdit()
		setEditTextStyle(self.editText)
		layout = QtGui.QHBoxLayout()
		labelWidget = QtGui.QLabel(label)
		setLabelStyle(labelWidget)
		layout.addWidget(labelWidget)

		layout.addWidget(self.editText)
		self.setLayout(layout)

	def getText(self):
		return self.editText.text()

	def setText(self, text):
		self.editText.setText(text)