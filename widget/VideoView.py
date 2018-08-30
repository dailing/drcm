from PyQt4 import QtGui, QtCore
import os, sys
sys.path.append(os.path.dirname(os.path.realpath('.')))
# /media/markalso/0C9EC8AB9EC88F20/test/camera/
#https://github.com/opencv/opencv/tree/b3cd2448cdb4a95f78864c2ec75914f8a628dd05/modules/videoio/src
from PainterWidget import PainterWidget
from VideoManager import VideoManager

from LabelSpinBox import LabelSpinBox
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
	"""docstring for VideoView"""
	def __init__(self, pageManager):
		QtGui.QWidget.__init__(self)
		self.pm = pageManager
		self.initUI()
		self.resize(800, 480)

		self.setObjectName("window")
		# self.setStyleSheet("QWidget{background-color : white;}")
		setBackGroundColor(self, QtCore.Qt.black)
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

	def leavePage(self, event):
		#clean resource
		self.vm.pauseCanvas()
		self.pm.navBack2PatientPage()
		#to do : LED related

	def addLabel(self, iconPath, action, layout):
			
		button = QtGui.QLabel()
		button.setPixmap(QtGui.QPixmap(iconPath))
		button.setAlignment(QtCore.Qt.AlignCenter)
		layout.addWidget(button)
		button.mousePressEvent = action
		return button

	def createLeftButtons(self):
		leftLayout = QtGui.QVBoxLayout()
		#left panel moved here for the convinience of program test
		leftLayout.addStretch(1)
		self.addLabel('icons/back_48.png', self.leavePage, leftLayout)
		self.addLabel('icons/led_48.png', defaultButtonClickHandler, leftLayout)
		leftLayout.addStretch(1)

		return leftLayout


	def hiddenSpinBoxs(self):
		HUE_SPIN = LabelSpinBox('HUE')
		leftLayout.addWidget(HUE_SPIN)
		HUE_SPIN.setValue(50)
		HUE_SPIN.connect_on_value_changed(self.set_HUE)

	def set_HUE(self, value):
		self.vm.set_HUE(value / 100.0)


	def createRightButtons(self):
		leftLayout = QtGui.QVBoxLayout()
		
		#right panel
		leftLayout.addStretch(1)

		self.addLabel('icons/snap_48.png', self.vm.snap, leftLayout)
		self.addLabel('icons/diagnosis_48.png', defaultButtonClickHandler, leftLayout)
		leftLayout.addStretch(1)

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


		