import sys
from PyQt4 import QtGui, QtCore
from utils.icons import get_icon
from PyQt4.QtCore import pyqtSignal
from utils.logFormatter import setupLogger

logger = setupLogger('header')

class HeadWidget(QtGui.QWidget):
	"""docstring for HeadWidget"""
	click_right_icon = pyqtSignal(name='header_right_icon_click()')
	click_left_icon = pyqtSignal(name='header_left_icon_click()')

	def __init__(self, middleText):
		QtGui.QWidget.__init__(self)
		self.resize(800, 10)
		self.leftIcon = get_icon('back')
		self.rightIcon = get_icon('back')

		self.middleText = QtGui.QLabel(middleText)
		self.allQHBoxLayout = QtGui.QHBoxLayout()

		self.allQHBoxLayout.addWidget(self.leftIcon)
		self.allQHBoxLayout.addWidget(self.middleText)
		self.allQHBoxLayout.addWidget(self.rightIcon)

		self.setLayout(self.allQHBoxLayout)
		
		self.middleText.setStyleSheet("color:black;font-size:20px;");
		self.allQHBoxLayout.setAlignment(self.middleText, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
		self.leftIcon.mousePressEvent = self.left_icon_click
		self.rightIcon.mousePressEvent= self.right_icon_click

		# self.setRightIcon(self.forwardIcon)
		#set bg color
		# self.setStyleSheet("background-color:#969b2b;");
		# self.allQHBoxLayout.setContentsMargins(0, 0, 0, 0)
		# self.setLeftIcon(self.leftIcon)
		# self.setRightIcon(self.rightIcon)
		# self.getHeightWidth()
	def left_icon_click(self, event):
		logger.debug(event)
		# logger.debug('left click')
		self.click_left_icon.emit()

	def right_icon_click(self, event):
		self.click_right_icon.emit()

	# TODO fix this
	def setLeftIcon(self,icon):
		self.allQHBoxLayout.removeItem(self.allQHBoxLayout.itemAt(0))
		if icon is not None:
			self.allQHBoxLayout.insertWidget(0, icon)
		else:
			self.allQHBoxLayout.insertWidget(0, self.leftIcon)


	def setRightIcon(self, icon):
		logger.debug('set right icon:' + str(icon))
		self.allQHBoxLayout.removeItem(self.allQHBoxLayout.itemAt(2))
		if icon is not None:
			self.allQHBoxLayout.insertWidget(2, icon)
			icon.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
		else:
			self.allQHBoxLayout.insertWidget(2, self.leftIcon)

	# def setRightIcon(self, iconPath):
	# 	self.rightIcon.setPixmap(QtGui.QPixmap(iconPath))
	# 	self.rightIcon.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

	def leftLabel(self):
		return self.leftIcon

	def rightLabel(self):
		return self.rightIcon

	def getHeightWidth(self):
		print ('hwhead', self.sizeHint())

def main():
	app = QtGui.QApplication(sys.argv)
	ex = HeadWidget('Head widget')
	print(ex.allQHBoxLayout.itemAt(0))
	# ex.setLeftIcon('../icons/back_48.png')
	# ex.setRightIcon('../icons/back_48.png')

	ex.show()
	app.exec_()

if __name__ == '__main__':
	xx = main()