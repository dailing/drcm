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
from utils.PageManager import PageManager
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

		# focusLedOn()
		self.logger.info('init main finished')

	def initEnv(self):
		self.imgCnt = 0
		self.patientInfo = loadObj(ImageCapture.LAST_PATIENT)
		
		self.logger.info('to register callback')
		#register callback
		
		self.uploadSignal.connect(self.uploadCallBack)
		# self.queryTableSignal.connect(self.appendDataToModel)
		#get all previous captured image to list view
		# self.dbManager.getAllRows(self.queryTableSignal)
		
	def initUI(self):
		self.setWindowTitle('DRCM')
		# self.showFullScreen()
		self.setGeometry(200, 200, 800, 480)
		# self.resize(800, 480)


		self.createShortCut()
		self.createMainGui()
		self.show()

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



	def uploadCallBack(self, items):
		#clear and update list view
		self.clearListView()
		self.appendDataToModel(items)

		

	def createMainGui(self):

		self.pm = PageManager()
		self.main_frame = self.pm.getWidget()
		setBackGroundColor(self.main_frame, QtCore.Qt.black)
		self.setCentralWidget(self.main_frame)

	def exitElegantly(self):
		self.close()

	def createShortCut(self):
		self.connect(QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self), QtCore.SIGNAL('activated()'), self.exitElegantly)
		
		
def main(logger):
	app = QtGui.QApplication(sys.argv)
	# splash= SplashScreen("icons/logo.jpg")  
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