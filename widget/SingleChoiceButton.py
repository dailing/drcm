from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot

def setLabelStyle(label):
	label.setAlignment(QtCore.Qt.AlignCenter)
	label.setStyleSheet("QLabel{color:black;font-size:24px}"
		);

class SingleChoiceButton(QtGui.QWidget):
	"""docstring for SingleChoiceButton"""
	def __init__(self, label, options, parent = None):
		QtGui.QWidget.__init__(self, parent)
		self.parent = parent
		optionButtons = [QtGui.QRadioButton(option) for option in options]
		optionButtons[0].setChecked(True)
		self.optionText = options[0]
		group = QtGui.QButtonGroup(self)
		for optionButton in optionButtons:
			group.addButton(optionButton)

		group.buttonClicked['QAbstractButton *'].connect(self.button_clicked)
		

		# horizontal box layout
		hlayout = QtGui.QHBoxLayout()
		labelWidget = QtGui.QLabel(label)
		hlayout.addWidget(labelWidget)
		setLabelStyle(labelWidget)
		for optionButton in optionButtons:
			hlayout.addWidget(optionButton)

		self.setLayout(hlayout)
		self.optionButtons = optionButtons

	# button_clicked slot
	@pyqtSlot(QtGui.QAbstractButton)
	def button_clicked(self, button):
		print(button.text())
		self.optionText = button.text()

	def setOption(self, isFirst):
		self.optionButtons[0 if isFirst else 1].setChecked(True)

	def getOption(self):
		return self.optionText