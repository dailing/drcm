from PyQt4 import QtGui, QtCore
import os, sys
sys.path.append(os.path.dirname(os.path.realpath('.')))
# /media/markalso/0C9EC8AB9EC88F20/test/camera/
#https://github.com/opencv/opencv/tree/b3cd2448cdb4a95f78864c2ec75914f8a628dd05/modules/videoio/src
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

def setBackGroundColor(aWidget, color):
	aWidget.setAutoFillBackground(True)
	pal = aWidget.palette()
	pal.setColor(aWidget.backgroundRole(), color)
	aWidget.setPalette(pal)

def defaultButtonClickHandler():
	print ('clicked')
	pass

class VideoView(QtGui.QWidget):
	no_head = True
	video_leave_signal = QtCore.pyqtSignal(name='video_leave()')
	leave_page_signal = QtCore.pyqtSignal(name='leave_page_signal()')

	"""docstring for VideoView"""
	def __init__(self, pageManager):
		QtGui.QWidget.__init__(self)
		self.pm = pageManager
		self.initUI()
		self.resize(800, 480)

		self.setObjectName("window")
		# self.setStyleSheet("QWidget{background-color : white;}")
		setBackGroundColor(self, QtCore.Qt.black)

		self.leave_page_signal.connect(self.leavePage)

	def addButton(self, label, action, layout):

		button = QtGui.QPushButton(label)
		button.setStyleSheet(ButtonStyle)
		layout.addWidget(button)
		self.connect(button, QtCore.SIGNAL("clicked()"),
				action)
		return button

	#enter page
	def fillRecord(self, patient):
		self.vm.fillRecord(patient)
		self.vm.startCanvas()

	def leavePage(self):
		#clean resource
		self.vm.pauseCanvas()
		self.video_leave_signal.emit()
		#to do : LED related

	def addLabel(self, iconPath, signal, layout):

		button = QtGui.QLabel()
		button.setPixmap(QtGui.QPixmap(iconPath))
		button.setAlignment(QtCore.Qt.AlignCenter)
		layout.addWidget(button)
		button.mousePressEvent = lambda event: signal.emit()
		return button

	def createLeftButtons(self):
		leftLayout = QtGui.QVBoxLayout()
		#left panel moved here for the convinience of program test
		self.addLabel('icons/back_48.png', self.leave_page_signal, leftLayout)
		self.addLabel('icons/led_48.png', self.leave_page_signal, leftLayout)

		return leftLayout


	# def hiddenSpinBoxs(self):
	# 	HUE_SPIN = LabelSpinBox('HUE')
	# 	leftLayout.addWidget(HUE_SPIN)
	# 	HUE_SPIN.setValue(50)
	# 	HUE_SPIN.connect_on_value_changed(self.set_HUE)

	def set_HUE(self, value):
		self.vm.set_HUE(value / 100.0)


	def createRightButtons(self):
		leftLayout = QtGui.QVBoxLayout()
		#right panel
		self.addLabel('icons/snap_48.png', self.vm.take_picture_signal, leftLayout)
		self.addLabel('icons/diagnosis_48.png', self.vm.diag_image_signal, leftLayout)
		return leftLayout

	def initUI(self):
		self.canvas = PainterWidget()
		self.vm = VideoManager(self.canvas)

		leftLayout = self.createLeftButtons()
		rightLayout = self.createRightButtons()

		layout = QtGui.QGridLayout(self)
		layout.addLayout(leftLayout, 0, 0, 8, 1)
		layout.addWidget(self.canvas, 0, 1, 8, 8)
		layout.addLayout(rightLayout, 0, 9, 8, 1)



def main():
	app = QtGui.QApplication(sys.argv)
	ex = VideoView(None)
	ex.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()


