import sys

from PyQt4 import QtCore, QtGui
from time import sleep
from random import randint

import logging
import time


import cv2
from utils.auxs import cv2ImagaeToQtImage
from widget.PainterWidget import PainterWidget
from utils.auxs import decodeDBImage

from sql.DataBaseManager import DataBaseManager

def getImage():
	dbm = DataBaseManager('sql/patientRecord.db')
	imgs = dbm.getAllLocalOnlyImageData()
	i = 0
	for img in imgs:
		i += 1
		cv2.imwrite('images/{}.png'.format(i), decodeDBImage(img[-1]))


def timeWork():
	vreader = cv2.VideoCapture(0)
	end = time.time() + 9
	vdata = []
	while time.time() < end :
		ret, frame = vreader.read()
		print(ret)
		vdata.append(frame)
	print (len(vdata), len(vdata) / 9)


class Worker(QtCore.QRunnable):
	def __init__(self, func, msgSignal):
		QtCore.QRunnable.__init__(self)
		self.func = func
		self.msgSignal = msgSignal

	def run(self):
		print('Running Worker')
		self.func()
		self.msgSignal.emit(randint(1, 20), [randint(5, 90), "fdjk"])

class PoolWrapper():
	def __init__(self):
		self.pool = QtCore.QThreadPool.globalInstance()
		self.pool.setMaxThreadCount(2)

	def start(self, worker):
		self.pool.start(worker)
		# self.pool.waitForDone()
		

class Task(QtCore.QObject):
	"""docstring for Task"""
	def __init__(self):
		super(Task, self).__init__()
		self.trigger = QtCore.pyqtSignal()

	def connect_and_emit(self):
		QtCore.QObject.connect(self, 
			QtCore.SIGNAL('sig()'), 
			self.handleTrigger)
		self.emit(QtCore.SIGNAL('sig()'))
	def handleTrigger(self):
		print('handler')

class Foo(object):
	pass

def printmsg(first):
	print('arg', first)
	sleep(2)
def defaultPrint():
	print('default')
	time.sleep(10)

buttonStyle = "QPushButton { \
background-color: white;\
font-family:arial;\
    border-style: outset;\
    border-width: 2px;\
    border-radius: 10px;\
    border-color: white;\
    font: bold 24px;\
    min-width: 10em;\
    padding: 6px;\
    selection-color : white;\
    selection-background-color : white;\
};\
QPushButton:selected{background-color:white; color: black;}\
QPushButton:cliked{background-color:white; color: black;}\
QPushButton:pressed{background-color:white; color: black;}\
QPushButton:hover{background-color:white; color: black;}\
QPushButton:focus{background-color:white; color: black;}\
QPushButton:checked{background-color:white; color: black;}\
"
class MyWidget(QtGui.QWidget):
	randSignal = QtCore.pyqtSignal(int, list)

	def __init__(self, parent=None):
		super(MyWidget, self).__init__(parent)
		self.setGeometry(0, 0, 800, 480)
		print(self.x())
		print(self.frameGeometry())
		self.setStyleSheet('background-color:black')
		self.resize(800, 480)
		print(self.x())
		print(self.geometry().x())
		print(self.frameGeometry())

		task = Task()
		self.pw = PoolWrapper()
		
		self.hlayout = QtGui.QVBoxLayout()
		self.setLayout(self.hlayout)
		self.b = QtGui.QPushButton("Emit your signal!", self)
		# self.b.resize((self.b.size()[0], self.b.size()[1] * 2))
		self.b.setStyleSheet('QPushButton {border-radius: 12px;font-size:32px;font-family:arial;background-color: #1B87E4; color : white}; QPushButton:pressed{background-color:#006ED9}')
		# self.b.setStyleSheet(buttonStyle)
		self.connect(self.b, QtCore.SIGNAL("clicked()"),
					self.clickHandler)
		self.label = QtGui.QLabel('ini')
		self.hlayout.addWidget(self.b)
		self.hlayout.addWidget(self.label)
		self.painter = PainterWidget()
		# self.hlayout.addWidget(self.painter)
		self.painter.setImageData(cv2ImagaeToQtImage(cv2.imread('logo.png')))

	def clickHandler(self):
		self.b.setEnabled(False)
		print ('sleep 10 secs')
		time.sleep(3)
		self.b.setEnabled(True)
		print ('sleep end')
		
		
		# self.mysignal.emit(5, ["a", Foo(), 6])

	def mySignalHandler(self, n, l):
		print (n)
		print (l)
		self.label.setText(str(n) + str(l))


def caller(func, *arg):
	print(arg)
	func(*arg)

def main():
	app = QtGui.QApplication(sys.argv)
	w = MyWidget()
	w.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	#getImage()
	main()
	
	
# if __name__ == '__main__':
	# msgSignal = QtCore.pyqtSignal()
	# msgSignal.emit()
	

   
