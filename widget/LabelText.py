from PyQt4 import QtGui, QtCore
import subprocess

from widget.MatchBoxLineEdit import MatchBoxLineEdit

class LabelText(QtGui.QWidget):
	"""edit text box with label"""
	def __init__(self, label):
		QtGui.QWidget.__init__(self)
		
		self.editText = MatchBoxLineEdit()
		layout = QtGui.QHBoxLayout()
		layout.addWidget(QtGui.QLabel(label))

		layout.addWidget(self.editText)
		self.setLayout(layout)

	def getText(self):
		return self.editText.text()

	def setText(self, text):
		self.editText.setText(text)