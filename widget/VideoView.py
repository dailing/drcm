from PyQt4 import QtGui, QtCore
import os, sys
sys.path.append(os.path.dirname(os.path.realpath('.')))
# /media/markalso/0C9EC8AB9EC88F20/test/camera/
from PainterWidget import PainterWidget
from VideoManager import VideoManager
ButtonStyle = "QPushButton { \
background-color: #1B87E4;\
font-family:arial;\
    border-style: solid;\
    color:black;\
    border-width: 2px;\
    border-radius: 10px;\
    border-color: #1B87E4;\
    font: bold 24px;\
    padding: 6px;\
}\
QPushButton:pressed{background-color:#007E59}\
"

def defaultButtonClickHandler():
	print ('clicked')
	pass
	
class VideoView(QtGui.QWidget):
	"""docstring for VideoView"""
	def __init__(self):
		QtGui.QWidget.__init__(self)
		self.initUI()
		self.resize(800, 480)

	def addButton(self, label, action, layout):
			
		button = QtGui.QPushButton(label)
		button.setStyleSheet(ButtonStyle)
		layout.addWidget(button)
		self.connect(button, QtCore.SIGNAL("clicked()"),
				action)
		return button

	def addLabel(self, iconPath, action, layout):
			
		button = QtGui.QLabel()
		button.setPixmap(QtGui.QPixmap(iconPath))
		layout.addWidget(button)
		self.connect(button, QtCore.SIGNAL("clicked()"),
				action)
		return button

	def createLeftButtons(self):
		leftLayout = QtGui.QVBoxLayout()
		self.addButton('BACK', defaultButtonClickHandler, leftLayout)
		self.addButton('LED', defaultButtonClickHandler, leftLayout)
		return leftLayout

	def createRightButtons(self):
		leftLayout = QtGui.QVBoxLayout()
		self.addButton('SNAP', self.vm.snap, leftLayout)
		self.addButton('DIAG', defaultButtonClickHandler, leftLayout)
		return leftLayout

	def initUI(self):
		self.canvas = PainterWidget()
		self.vm = VideoManager(self.canvas, None)
		self.vm.startCanvas()

		leftLayout = self.createLeftButtons()
		rightLayout = self.createRightButtons()
		
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


		