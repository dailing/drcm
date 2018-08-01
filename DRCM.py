#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
show video from camera 
capture, save and upload video frame

author: knowthy
last edited: july 2018
"""
import sys
from PyQt4 import QtGui, QtCore
import cv2

from widget.PainterWidget import PainterWidget
from widget.MedicalRecordDialog  import MedicalRecordDialog
from widget.SplashScreen import SplashScreen
from widget.ViewModel import ViewModel

from sql.sqlConn import SqlConn
from sql.RunnableFunc import RunnableFunc
from sql.PoolWrapper import PoolWrapper
from sql.DataBaseManager import DataBaseManager

from network.uploadClient import uploadClient
from network.wifiWidget import WifiTableView

from utils.logFormatter import setupLogger
from utils.auxs import *
from utils.folderUtils import ensurePath


class VideoReader():
	def __init__(self):
		pass
		self.reader = cv2.VideoCapture(0)

	def read(self):
		return self.reader.read()


def setBackGroundColor(aWidget, color):
	aWidget.setAutoFillBackground(True)
	pal = aWidget.palette()
	pal.setColor(aWidget.backgroundRole(), color)
	aWidget.setPalette(pal)

def setTextColor(aWidget, color):
	aWidget.setStyleSheet("color:white;");

		
class ImageCapture(QtGui.QMainWindow):

	FRAME_PER_SECOND = 24
	UPDATE_FREQ = 1000.0 / FRAME_PER_SECOND
	LAST_PATIENT = 'patientInfo.pkl'


	dbInsertSignal = QtCore.pyqtSignal(bool)
	uploadSignal = QtCore.pyqtSignal(list)
	queryTableSignal = QtCore.pyqtSignal(list)
	remoteProcessSignal = QtCore.pyqtSignal(bytes)
	
	def __init__(self, logger):
		QtGui.QMainWindow.__init__(self, None)
		self.logger = logger
		self.logger.info('logging started in {}'.format(self.__class__.__name__))
		self.initEnv()
		self.initUI()
		self.timer.start(ImageCapture.UPDATE_FREQ)

	def initEnv(self):
		self.preImageData = None
		self.pw = PoolWrapper()
		self.dbManager = DataBaseManager('patientRecord.db')
		self.patientInfo = loadObj(ImageCapture.LAST_PATIENT)
		self.timer = QtCore.QTimer()
		self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.updateFrame)
		self.camera = VideoReader()
		self.model = ViewModel()

		#register callback
		
		self.dbInsertSignal.connect(self.saveImageCallBack)
		self.uploadSignal.connect(self.uploadCallBack)
		self.queryTableSignal.connect(self.appendDataToModel)
		self.remoteProcessSignal.connect(self.processImageCallBack)
		#get all previous captured image to list view
		self.dbManager.getAllRows(self.queryTableSignal)
		
	def initUI(self):
		self.setWindowTitle('DRCM')
		# self.showMaximized()
		self.setGeometry(0, 0, 800, 480)
		self.resize(800, 480)


		self.create_menu()
		self.createMainGui()
		self.show()
		


	def processImage(self):
		if self.timer.isActive() or self.preImageData is None:
			return
		self.pw.start(
			RunnableFunc(
				uploadClient(self.dbManager).remoteProcess,
				self.preImageData,
				self.remoteProcessSignal
				)
			)

	def processImageCallBack(self, imageData):
		image = decodeDBImage(imageData)
		frame_to_display = cv2.resize(image, (640, 480))
		mQImage = cv2ImagaeToQtImage(frame_to_display)
		self.painter.setImageData(mQImage)

	def createBottomGroupBox(self):
		bottomLayout = QtGui.QVBoxLayout()

		self.patientIdentify = QtGui.QLabel(
			'name' if self.patientInfo is None else self.patientInfo.getPid()
			)
		setTextColor(self.patientIdentify, QtCore.Qt.white)
		bottomLayout.addWidget(self.patientIdentify)

		bottomLayout.addStretch(1)
		def addButton(label, action):
			button = QtGui.QPushButton(label)
			# button.setContentsMargins(2, 2, 2, 2)
			bottomLayout.addWidget(button)
			self.connect(button, QtCore.SIGNAL("clicked()"),
					action)
			return button
			
		self.captureButton = addButton('Capture', self.snapShot)
		pageButton = addButton('NewRecord', self.newRecord)
		uploadButton  = addButton('Upload', self.uploadImages)
		addButton('Process', self.processImage)

		bottomLayout.addStretch(1)

		addButton('IMAGE', self.switchToImageView)
		addButton('INFO', self.switchToInfoView)
		addButton('WLAN', self.switchToWlanView)
		
		bottomLayout.addStretch(1)
		buttonGroupBox = QtGui.QGroupBox()
		buttonGroupBox.setLayout(bottomLayout)

		setBackGroundColor(buttonGroupBox, QtCore.Qt.black)
		return buttonGroupBox

	def uploadImages(self):
		print('upload images')
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
		if self.patientInfo is None:
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
			self.updateFrame(True)
		else :
			self.timer.start(ImageCapture.UPDATE_FREQ)

	def updateFrame(self, saveTodisk = False):
		ret, frame = self.camera.read()
		if not ret:
			print(ret)
			return
		frame_to_display = cv2.resize(frame, (640, 480))
		if saveTodisk:
			self.preImageData = frame
			self.saveImage(frame)
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
		self.stacked_widget.addWidget(self.createListView())
		self.stacked_widget.addWidget(WifiTableView())
		# self.stacked_widget.setCurrentIndex(1)
		setBackGroundColor(self.stacked_widget, QtCore.Qt.black)
		return self.stacked_widget

	def switchToImageView(self):
		if self.stacked_widget.currentIndex() == 0:
			return
		self.stacked_widget.setCurrentIndex(0)

	def switchToInfoView(self):
		if self.stacked_widget.currentIndex() == 1:
			return
		self.stacked_widget.setCurrentIndex(1)

	def switchToWlanView(self):
		if self.stacked_widget.currentIndex() == 2:
			return
		self.stacked_widget.setCurrentIndex(2)

	def createMainGui(self):

		buttonGroupBox = self.createBottomGroupBox()
		leftPanelView = self.createLeftPanelView()
		layout = QtGui.QGridLayout()
		layout.addWidget(leftPanelView, 0, 0, 4, 1)
		layout.addWidget(buttonGroupBox, 0, 4, 4, 1)
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