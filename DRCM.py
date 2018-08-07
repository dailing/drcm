#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
show video from camera 
capture, save and upload video frame

author: knowthy
last edited: july 2018
"""
#sudo -E bash -c 'sleep 15;python /home/pi/Desktop/drcm/DRCM.py &>> /tmp/drcm.log'
import sys
from PyQt4 import QtGui, QtCore
import cv2
import numpy as np

from widget.PainterWidget import PainterWidget
from widget.MedicalRecordDialog  import MedicalRecordDialog
from widget.SplashScreen import SplashScreen
from widget.ViewModel import ViewModel
from widget.DiagnosisDialog import DiagnosisDialog

from sql.sqlConn import SqlConn
from sql.RunnableFunc import RunnableFunc
from sql.PoolWrapper import PoolWrapper
from sql.DataBaseManager import DataBaseManager

from network.uploadClient import uploadClient
from network.wifiWidget import WifiTableView

from utils.logFormatter import setupLogger
from utils.auxs import *
from utils.folderUtils import ensurePath
from utils.singleShotTimer import SingleShotTimer
from subprocess import Popen, PIPE

try:
	from gpiozero import LED
	from gpiozero import PWMLED as pwm
except Exception as e:
	pass

import socket

def get_host_ip():
	"""
	查询本机ip地址
	:return: ip
	"""
	try:
		process = Popen(['ip','addr','show'],stdout=PIPE)
		olines = process.stdout.read().splitlines()
		addresses = []
		for line in olines:
			line = line.strip()
			if line.startswith('inet '):
				line = line.split()[1]
				addresses.append(line)
	except Exception as e :
		print(e)
		return 'None'
	return '\n'.join(addresses[1:])

class VideoReader():
	def __init__(self):
		pass
		self.reader = cv2.VideoCapture(0)
		logger = logging.getLogger('root.VideoReader')
		try:
			self.reader.set(3,640);
			self.reader.set(4,480);
			self.reader.set(38, 4)
		except Exception as e:
			print (str(e))
			logger.exception(e)
		logger.debug('finish open video')
		logger.info('buffer size for camera : {}'.format(self.reader.get(38)))

		


	def read(self):
		return self.reader.read()

CaptureButtonStyle = "QPushButton { \
background-color: #FFFFFF;\
font-family:arial;\
    border-style: solid;\
    color:black;\
    border-width: 2px;\
    border-radius: 10px;\
    border-color: white;\
    font: bold 24px;\
    padding: 6px;\
}\
"

#13,26
FIXED_LED = [5,6,13,19,26,16,20,21]
def offFixedLed():
	try:
		for l in FIXED_LED:
			LED(l).off()
	except Exception as e:
		pass
try:
	led5 = pwm(5)
	led6 = LED(6)
except Exception as e:
	pass

def toggleFixedLed():
	led5.toggle()

def switchFixedLed():
	try:
		for l in FIXED_LED:
			LED(l).toggle()
	except Exception as e:
		pass

# def infraredLed():
# 	LED(2).toggle()

# def flashLed():
# 	LED(3).toggle()
try:
	infraredLed = LED(17)
	flashLed = pwm(4)
except Exception as e:
	pass
def focusLedOn():
	try:
		flashLed.value = 0.0
	except Exception as e:
		pass
	try:
		infraredLed.on()
	except Exception as e:
		pass
	try:
		led5.value = 0
	except Exception as e:
		pass


def exposureOn():
	try:
		infraredLed.off()
	except Exception as e:
		pass
	try:
		led5.value = 0
	except Exception as e:
		pass
	try:
		flashLed.value = 0.8
		led6.off()
	except Exception as e:
		pass


def function():
	pass

def setBackGroundColor(aWidget, color):
	aWidget.setAutoFillBackground(True)
	pal = aWidget.palette()
	pal.setColor(aWidget.backgroundRole(), color)
	aWidget.setPalette(pal)

def setLabelStyle(label):
	label.setAlignment(QtCore.Qt.AlignCenter)
	label.setStyleSheet("QLabel{color:white;font-size:16px}"
		);

DISPLAY_SIZE = (640, 480)
class ImageCapture(QtGui.QMainWindow):

	FRAME_PER_SECOND = 24
	UPDATE_FREQ = 1000.0 / FRAME_PER_SECOND
	LAST_PATIENT = 'patientInfo.pkl'


	dbInsertSignal = QtCore.pyqtSignal(bool)
	uploadSignal = QtCore.pyqtSignal(list)
	queryTableSignal = QtCore.pyqtSignal(list)
	remoteProcessSignal = QtCore.pyqtSignal(dict)
	
	def __init__(self, logger):
		QtGui.QMainWindow.__init__(self, None)
		self.logger = logger
		self.logger.info('logging started in {}'.format(self.__class__.__name__))
		self.initEnv()
		self.logger.info('inienv finished')
		self.initUI()
		self.logger.info('init ui finished')

		self.timer.start(ImageCapture.UPDATE_FREQ)
		offFixedLed()
		focusLedOn()
		self.logger.info('init main finished')

	def initEnv(self):
		self.imgCnt = 0
		self.preImageData = None
		self.pw = PoolWrapper()
		self.dbManager = DataBaseManager('patientRecord.db')
		self.patientInfo = loadObj(ImageCapture.LAST_PATIENT)
		self.timer = QtCore.QTimer()
		self.ledTimer = SingleShotTimer()
		self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.updateFrame)
		self.ledTimer.connect(self, focusLedOn)
		self.camera = VideoReader()
		self.model = ViewModel()
		self.logger.info('to register callback')
		#register callback
		
		self.dbInsertSignal.connect(self.saveImageCallBack)
		self.uploadSignal.connect(self.uploadCallBack)
		self.queryTableSignal.connect(self.appendDataToModel)
		self.remoteProcessSignal.connect(self.processImageCallBack)
		#get all previous captured image to list view
		self.dbManager.getAllRows(self.queryTableSignal)
		
		
	def initUI(self):
		self.setWindowTitle('DRCM')
		self.showFullScreen()
		# self.setGeometry(200, 200, 800, 480)
		# self.resize(800, 480)


		self.create_menu()
		self.createMainGui()
		self.show()
		


	def processImage(self):
		self.logger.debug('processImage')
		if self.timer.isActive() or self.preImageData is None:
			return
		self.pw.start(
			RunnableFunc(
				uploadClient(self.dbManager).remoteProcess,
				self.preImageData,
				self.remoteProcessSignal
				)
			)

	def processImageCallBack(self, diagnosis):
		self.logger.debug('diagnosis display')
		DiagnosisDialog.newInstance(diagnosis)
		print (diagnosis)
		

	def createButtonLayout(self):
		bottomLayout = QtGui.QVBoxLayout()

		bottomLayout.addStretch(1)
		ipadd = get_host_ip()
		print(ipadd, type(ipadd))
		self.patientIdentify = QtGui.QLabel(
			ipadd
			)
		setLabelStyle(self.patientIdentify)
		bottomLayout.addWidget(self.patientIdentify)

		bottomLayout.addStretch(1)
		def addButton(label, action):
			button = QtGui.QPushButton(label)
			button.setStyleSheet('QPushButton {border-radius: 12px;font-size:32px;font-family:arial;background-color: #1B87E4; color : white}; QPushButton:pressed{background-color:#007ED9}')
			bottomLayout.addWidget(button)
			self.connect(button, QtCore.SIGNAL("clicked()"),
					action)
			# button.setStyleSheet("")
			return button
			
		self.captureButton = addButton('Capture', self.snapShot)
		# uploadButton  = addButton('Upload', self.uploadImages)
		# ledButton = addButton('Led', toggleFixedLed)
		# pageButton = addButton('NewRecord', self.newRecord)
		
		addButton('Process', self.processImage)

		bottomLayout.addStretch(1)
		# self.captureButton.setStyleSheet(CaptureButtonStyle)

		addButton('IMAGE', self.switchToImageView)
		# addButton('INFO', self.switchToInfoView)
		addButton('WLAN', self.switchToWlanView)
		
		bottomLayout.addStretch(1)
		return bottomLayout

	def uploadImages(self):
		# ipadd = get_host_ip()
		# self.patientIdentify.setText(ipadd)
		# return
		self.logger.debug('upload images')
		self.pw.start(
			RunnableFunc(
				uploadClient(self.dbManager).getDataAndUpload,
				self.uploadSignal
				)
			)


	def clearListView(self):
		self.model.clear()

	def appendDataToModel(self, items):
		for item in items:
			patiendName = item[1]
			recordTime = getDateTimeFromTS(item[2])
			if item[0] == 0:
				foo = '{} {}'.format(patiendName, recordTime)
			else :
				foo = u'\u2713 {} {}'.format(patiendName, recordTime)
			self.model.pushBack(foo)

	def uploadCallBack(self, items):
		#clear and update list view
		self.clearListView()
		self.appendDataToModel(items)


	def snapShot(self):
		
		self.scheduleUpdating()
		
		

	def saveImage(self, imageData):
		self.imgCnt += 1
		cv2.imwrite('{}.png'.format(self.imgCnt), imageData)
		if self.patientInfo is None:
			self.captureButton.setEnabled(True)
			return

		
		self.patientInfo.setTime(getTimeStamp())
		self.patientInfo.setUUID(getUUID())
		self.patientInfo.setData(
			encodeImageToDBdata(imageData)
			)
		# to do: push to DB
		# self.pw.start(
		# 	RunnableFunc(
		# 		self.dbManager.insertRecord,
		# 		self.patientInfo,
		# 		self.dbInsertSignal
		# 		)
		# 	)
		self.dbManager.insertRecord(self.patientInfo, self.dbInsertSignal)


	def saveImageCallBack(self, isSucceed):
		print(isSucceed)
		if isSucceed:
			ts = self.patientInfo.getTimeId()
			print(ts, type(ts))
			dt = getDateTimeFromTS(ts)
			foo = '{} {}'.format(self.patientInfo.getPid(), dt)
			self.model.pushFront(foo)
		else :
			QtGui.QMessageBox.warning(
				QtGui.QWidget(), "Error", "save data failed!")

		self.captureButton.setEnabled(True)


	def newRecord(self):
		reply, okPressed = MedicalRecordDialog.newRecord(self.patientInfo);
		print(reply)
		if okPressed:
			self.patientInfo = reply
			self.patientIdentify.setText(self.patientInfo.getPid())
			saveObj(ImageCapture.LAST_PATIENT,
				self.patientInfo)
			

	def scheduleUpdating(self):
		if self.timer.isActive():
			self.captureButton.setEnabled(False)
			self.timer.stop()
			
			try:
				self.flashFrame()
			except Exception as e:
				self.logger.exception('flash Frame')
				pass
			finally :
				self.captureButton.setEnabled(True)
				
		else :
			self.timer.start(ImageCapture.UPDATE_FREQ)

	def flashFrame(self, num = 3):
		#exposure
		exposureOn()
		data = [self.camera.read()[1]]
		focusLedOn()
		newData = [self.camera.read()[1] for i in range(9)]
		data.extend(newData)
		best_img = get_most_colorful_image(data)
		# best_img = data[0]
		self.preImageData = best_img
		
		for img in data:
			self.saveImage(img)
		# self.saveImage(best_img)

		frame_to_display = cv2.resize(best_img, DISPLAY_SIZE)
		mQImage = cv2ImagaeToQtImage(frame_to_display)
		self.painter.setImageData(mQImage)
		#end

	def updateFrame(self, saveTodisk = False):
		ret, frame = self.camera.read()
		if not ret:
			if not sys.platform.startswith('win'):
				self.camera = VideoReader()
			self.captureButton.setEnabled(True)
			return
		frame_to_display = cv2.resize(frame, DISPLAY_SIZE)
		# if saveTodisk:
		# 	self.saveImage(frame)
		mQImage = cv2ImagaeToQtImage(frame_to_display)
		self.painter.setImageData(mQImage)

	def createListView(self):
		listView = QtGui.QListView()
		listView.setModel(self.model)
		return listView

		

	def createLeftPanelView(self):
		self.painter = PainterWidget()
		self.stacked_widget = QtGui.QStackedWidget()
		self.stacked_widget.addWidget(self.painter)
		# self.stacked_widget.addWidget(self.createListView())
		self.stacked_widget.addWidget(WifiTableView())
		setBackGroundColor(self.stacked_widget, QtCore.Qt.black)
		return self.stacked_widget

	def switchToImageView(self):
		if self.stacked_widget.currentIndex() == 0:
			return
		self.stacked_widget.setCurrentIndex(0)

	def switchToInfoView(self):
		if self.stacked_widget.currentIndex() == 2:
			return
		self.stacked_widget.setCurrentIndex(2)

	def switchToWlanView(self):
		if self.stacked_widget.currentIndex() == 1:
			return
		self.stacked_widget.setCurrentIndex(1)

	def createMainGui(self):

		buttonLayout = self.createButtonLayout()
		leftPanelView = self.createLeftPanelView()
		layout = QtGui.QGridLayout()
		layout.addWidget(leftPanelView, 0, 0, 4, 4)
		layout.addLayout(buttonLayout, 0, 4, 4, 1)
		self.main_frame = QtGui.QWidget()
		self.main_frame.setLayout(layout)
		setBackGroundColor(self.main_frame, QtCore.Qt.black)
		self.setCentralWidget(self.main_frame)

	def exitElegantly(self):
		self.timer.stop()
		self.close()

	def create_menu(self):
		pass
		self.connect(QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self), QtCore.SIGNAL('activated()'), self.exitElegantly)
		# self.file_menu = self.menuBar().addMenu("&File")
		
		# getImageAction = self.create_action("snapShot",
		# 	shortcut="Ctrl+I", slot=self.snapShot, tip="take a picture")
		
		# exit_action = self.create_action("E&xit", slot=self.exitElegantly, 
		# 	shortcut="Ctrl+W", tip="Exit the application")

		
		# self.add_actions(self.file_menu, 
		# 	(   getImageAction,
		# 		None, exit_action))
		
	# The following two methods are utilities for simpler creation
	# and assignment of actions
	#
	def add_actions(self, target, actions):
		for action in actions:
			if action is None:
				target.addSeparator()
			else:
				target.addAction(action)
	#-----------------------------------------------

	def create_action(
		self, text, slot=None, shortcut=None, 
						icon=None, tip=None, checkable=False, 
						signal="triggered()"):
		action = QtGui.QAction(text, self)
		if icon is not None:
			action.setIcon(QIcon(":/{}.png".format(icon)))
		if shortcut is not None:
			action.setShortcut(shortcut)
		if tip is not None:
			action.setToolTip(tip)
			action.setStatusTip(tip)
		if slot is not None:
			self.connect(action, QtCore.SIGNAL(signal), slot)
		if checkable:
			action.setCheckable(True)
		return action
	#-----------------------------------------------
		
		
def main(logger):
	app = QtGui.QApplication(sys.argv)
	# splash= SplashScreen("logo.png")  
	# splash.effect()
	# app.processEvents() 
	ex = ImageCapture(logger)
	ex.show()
	# splash.finish(ex)
	sys.exit(app.exec_())


if __name__ == '__main__':
	ensurePath()
	logger = setupLogger('root')
	main(logger)