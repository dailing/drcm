import sys

from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSlot


class Window(QtGui.QWidget):
	def __init__(self, parent=None):
		super(Window, self).__init__(parent)

		# radiobuttons
		option_1 = QtGui.QRadioButton('Option 1')
		option_2 = QtGui.QRadioButton('Option 2')
		option_3 = QtGui.QRadioButton('Option 3')
		option_1.setChecked(True)  # default option

		# button group
		group = QtGui.QButtonGroup(self)
		group.addButton(option_1)
		group.addButton(option_2)
		group.addButton(option_3)
		# buttonClicked signals with two different signatures
		group.buttonClicked['QAbstractButton *'].connect(self.button_clicked)
		group.buttonClicked['int'].connect(self.button_clicked)

		# output 1
		self.output_1 = QtGui.QLineEdit()
		self.output_1.setReadOnly(True)  # read-only
		self.output_1.setAlignment(Qt.AlignCenter)  # centered

		# output 2
		self.output_2 = QtGui.QLineEdit()
		self.output_2.setReadOnly(True)  # read-only
		self.output_2.setAlignment(Qt.AlignCenter)  # centered

		# vertical box layout
		vlayout = QtGui.QVBoxLayout()
		vlayout.addWidget(option_1)
		vlayout.addWidget(option_2)
		vlayout.addWidget(option_3)
		vlayout.addSpacing(10)
		vlayout.addWidget(self.output_1)
		vlayout.addWidget(self.output_2)
		vlayout.addStretch()
		self.setLayout(vlayout)

	# button_clicked slot
	@pyqtSlot(QtGui.QAbstractButton)
	@pyqtSlot(int)
	def button_clicked(self, button_or_id):
		if isinstance(button_or_id, QtGui.QAbstractButton):
			self.output_1.setText('"{}" was clicked'.format(button_or_id.text()))
		elif isinstance(button_or_id, int):
			self.output_2.setText('"Id {}" was clicked'.format(button_or_id))


application = QtGui.QApplication(sys.argv)

# window
window = Window()
window.setWindowTitle('Button Group')
window.resize(220, 120)
window.show()

sys.exit(application.exec_())