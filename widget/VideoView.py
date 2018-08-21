from PyQt4 import QtGui, QtCore
import sys

from PainterWidget import PainterWidget
def defaultButtonClickHandler():
	pass
	
class VideoView(QtGui.QWidget):
	"""docstring for VideoView"""
	def __init__(self):
		QtGui.QWidget.__init__(self)
		self.initUI()
		self.setGeometry(200, 200, 800, 480)

	def addButton(self, label, action, layout):
			
		button = QtGui.QPushButton(label)
		layout.addWidget(button)
		self.connect(button, QtCore.SIGNAL("clicked()"),
				action)
		return button

	def createLeftButtons(self):
		leftLayout = QtGui.QVBoxLayout()
		self.addButton('Back', defaultButtonClickHandler, leftLayout)
		self.addButton('LED', defaultButtonClickHandler, leftLayout)
		return leftLayout

	def createRightButtons(self):
		leftLayout = QtGui.QVBoxLayout()
		self.addButton('SNAP', defaultButtonClickHandler, leftLayout)
		self.addButton('DIAGNOSIS', defaultButtonClickHandler, leftLayout)
		return leftLayout

	def initUI(self):
		leftLayout = self.createLeftButtons()
		rightLayout = self.createRightButtons()
		self.canvas = PainterWidget()
		layout = QtGui.QGridLayout(self)
		layout.addLayout(leftLayout, 0, 0, 8, 1)
		layout.addWidget(self.canvas, 0, 1, 8, 8)
		layout.addLayout(rightLayout, 0, 9, 8, 1)



def main():
	app = QtGui.QApplication(sys.argv)
	ex = VideoView()
	ex.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()


		