import sys
from PyQt4 import QtGui, QtCore

class HeadWidget(QtGui.QWidget):
	"""docstring for HeadWidget"""
	def __init__(self, middleText):
		QtGui.QWidget.__init__(self)
		self.resize(800, 42)
		self.leftIcon = QtGui.QLabel()
		self.rightIcon = QtGui.QLabel()
		self.middleText = QtGui.QLabel(middleText)
		self.allQHBoxLayout = QtGui.QHBoxLayout()
		self.allQHBoxLayout.addWidget(self.leftIcon, 0)
		self.allQHBoxLayout.addWidget(self.middleText, 1)
		self.allQHBoxLayout.addWidget(self.rightIcon, 2)
		# self.allQHBoxLayout.addWidget(self.leftIcon)
		# self.allQHBoxLayout.addWidget(self.middleText)
		# self.allQHBoxLayout.addWidget(self.rightIcon)
		self.setLayout(self.allQHBoxLayout)
		
		self.middleText.setStyleSheet("color:black;font-size:36px;");
		self.allQHBoxLayout.setAlignment(self.middleText, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
		#set bg color
		# self.setStyleSheet("background-color:#969b2b;");
		# self.allQHBoxLayout.setContentsMargins(0, 0, 0, 0)
	

		self.getHeightWidth()
		

	def setLeftIcon(self, iconPath):
		self.leftIcon.setPixmap(QtGui.QPixmap(iconPath))
		self.leftIcon.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

	def setRightIcon(self, iconPath):
		self.rightIcon.setPixmap(QtGui.QPixmap(iconPath))
		self.rightIcon.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

	def leftLabel(self):
		return self.leftIcon

	def rightLabel(self):
		return self.rightIcon

	def getHeightWidth(self):
		print ('hwhead', self.sizeHint())

def main():
	app = QtGui.QApplication(sys.argv)
	ex = HeadWidget('Head widget')
	ex.setLeftIcon('../icons/back_48.png')
	ex.setRightIcon('../icons/back_48.png')

	ex.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()