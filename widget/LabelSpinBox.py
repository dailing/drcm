import sys

from PyQt4 import QtGui

class LabelSpinBox(QtGui.QWidget):
	"""docstring for LabelSpinBox"""
	def __init__(self, label):
		QtGui.QWidget.__init__(self)
		self.label = QtGui.QLabel(label)

		self.steps_spin = QtGui.QSpinBox()
		self.steps_spin.setRange(0, 100)
		layout = QtGui.QVBoxLayout(self)
		layout.addWidget(self.label)
		layout.addWidget(self.steps_spin)

	def connect_on_value_changed(self, func):
		self.steps_spin.valueChanged.connect(func)

	def setValue(self, value):
		self.steps_spin.setValue(value)

	def setRange(self, l, r):
		self.steps_spin.setRange(l, r)

def main():
	app = QtGui.QApplication(sys.argv)
	ex = LabelSpinBox('label')
	ex.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
