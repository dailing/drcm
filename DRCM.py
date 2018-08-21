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
from utils.CircleMask import CircleMask
from utils.CameraLED import ViewFixationLED, Infrared_LED, Flash_LED
from subprocess import Popen, PIPE

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
		# self.reader = cv2.VideoCapture(0)
		# logger = logging.getLogger('root.VideoReader')
		# try:
		# 	self.reader.set(3,640);
		# 	self.reader.set(4,480);
		# 	# self.reader.set(38, 4)
		# except Exception as e:
		# 	print (str(e))
		# 	logger.exception(e)
		# logger.debug('finish open video')
		# logger.info('buffer size for camera : {}'.format(self.reader.get(38)))
		self.image = cv2.imread('eye.jpg')


	def read(self):
		return [True, self.image]

CaptureButtonStyle = "QPushButton { \
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
default_button_style = 'QPushButton {border-radius: 12px;font-size:32px;font-family:arial;background-color: white;} QPushButton:pressed{background-color:#007ED9}'



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


	uploadSignal = QtCore.pyqtSignal(list)
	queryTableSignal = QtCore.pyqtSignal(list)
	
	def __init__(self, logger):
		QtGui.QMainWindow.__init__(self, None)
		self.logger = logger
		self.logger.info('logging started in {}'.format(self.__class__.__name__))
		self.initEnv()
		self.logger.info('inienv finished')
		self.initUI()
		self.logger.info('init ui finished')

		self.timer.start(ImageCapture.UPDATE_FREQ)
		focusLedOn()
		self.logger.info('init main finished')

	def initEnv(self):
		self.imgCnt = 0
		self.patientInfo = loadObj(ImageCapture.LAST_PATIENT)
		
		self.logger.info('to register callback')
		#register callback
		
		self.uploadSignal.connect(self.uploadCallBack)
		self.queryTableSignal.connect(self.appendDataToModel)
		#get all previous captured image to list view
		# self.dbManager.getAllRows(self.queryTableSignal)
		
		
	def initUI(self):
		self.setWindowTitle('DRCM')
		# self.showFullScreen()
		self.setGeometry(200, 200, 800, 480)
		# self.resize(800, 480)


		self.create_menu()
		self.createMainGui()
		self.show()
		



		

	def createButtonLayout(self):
		bottomLayout = QtGui.QVBoxLayout()

		bottomLayout.addStretch(1)
		ipadd = get_host_ip()
		print(ipadd, type(ipadd))
		self.patientIdentify = QtGui.QLabel(
			ipadd
			)
		setLabelStyle(self.patientIdentify)
		# bottomLayout.addWidget(self.patientIdentify)

		bottomLayout.addStretch(1)
		def addButton(label, action):
			
			button = QtGui.QPushButton(label)
			button.setStyleSheet(CaptureButtonStyle)
			bottomLayout.addWidget(button)
			self.connect(button, QtCore.SIGNAL("clicked()"),
					action)
			# button.setStyleSheet("")
			return button
			
		self.captureButton = addButton('Capture', self.snapShot)
		
		# setButtonIcon('icons/photo-camera.svg', self.captureButton)
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

	def newRecord(self):
		reply, okPressed = MedicalRecordDialog.newRecord(self.patientInfo);
		print(reply)
		if okPressed:
			self.patientInfo = reply
			self.patientIdentify.setText(self.patientInfo.getPid())
			saveObj(ImageCapture.LAST_PATIENT,
				self.patientInfo)


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
		self.connect(QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self), QtCore.SIGNAL('activated()'), self.exitElegantly)
		
		
def main(logger):
	app = QtGui.QApplication(sys.argv)
	splash= SplashScreen("icons/logo.jpg")  
	splash.effect()
	app.processEvents() 
	ex = ImageCapture(logger)
	ex.show()
	splash.finish(ex)
	sys.exit(app.exec_())


if __name__ == '__main__':
	ensurePath()
	logger = setupLogger('root')
	main(logger)