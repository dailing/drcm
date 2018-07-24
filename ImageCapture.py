#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
show video from camera 
capture, save and upload frame

author: knowthy
last edited: july 2018
"""

import sys
from PyQt4 import QtGui, QtCore
import cv2

from widget.PainterWidget import PainterWidget
from widget.MedicalRecordDialog  import MedicalRecordDialog

from utils import *
from ViewModel import ViewModel

from conn.conn import Uploader

from sql.sqlConn import SqlConn
from sql.RunnableFunc import RunnableFunc
from sql.PoolWrapper import PoolWrapper
from sql.DataBaseManager import DataBaseManager

class VideoReader():
	def __init__(self):
		pass
		self.reader = cv2.VideoCapture("F:\TDDOWNLOAD\open courses\Justice_ What's the right thing to do\Lecture04.mp4")

	def read(self):
		return self.reader.read()

				
class ImageCapture(QtGui.QMainWindow):

	FRAME_PER_SECOND = 24
	UPDATE_FREQ = 1000.0 / FRAME_PER_SECOND
	LAST_PATIENT = 'patientInfo.pkl'


	dbInsertSignal = QtCore.pyqtSignal(bool)
	
	def __init__(self):
		super(ImageCapture, self).__init__()
		self.initEnv()
		self.initUI()
		self.timer.start(ImageCapture.UPDATE_FREQ)

	def initEnv(self):
		self.pw = PoolWrapper()
		self.dbManager = DataBaseManager('patientRecord.db')
		self.patientInfo = loadObj(ImageCapture.LAST_PATIENT)
		self.timer = QtCore.QTimer()
		self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.updateFrame)
		self.camera = VideoReader()
		self.model = ViewModel()

		#register callback
		# self.thread = Uploader()
		# self.thread.start()
		
		self.dbInsertSignal.connect(self.saveImageCallBack)
		
	def initUI(self):
		self.setWindowTitle('DRCM')
		self.setGeometry(0, 0, 800, 480)
		self.create_menu()
		self.createMainGui()
		self.show()
		

	def createBottomGroupBox(self):
		bottomLayout = QtGui.QHBoxLayout()

		def addButton(label, action):
			button = QtGui.QPushButton(label)
			bottomLayout.addWidget(button)
			self.connect(button, QtCore.SIGNAL("clicked()"),
					action)
			return button
			
		self.captureButton = addButton('Capture', self.snapShot)
		pageButton = addButton('newRecord', self.newRecord)
		uploadButton  = addButton('Upload', self.uploadImages)
		bottomLayout.addStretch(1)
		self.patientIdentify = QtGui.QLabel(
			'name' if self.patientInfo is None else self.patientInfo.getPid()
			)
		bottomLayout.addWidget(self.patientIdentify)
		buttonGroupBox = QtGui.QGroupBox()
		buttonGroupBox.setLayout(bottomLayout)
		return buttonGroupBox

	def uploadImages(self):
		print('upload images')


	def clearListView(self):
		self.model.clear()
		

	def uploadCallBack(self):
		#retrive data

		#clear and update list view
		self.model.clearListView()
		for row in res:
			self.model.pushFront(row)


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
		# Capture frame-by-frame
		ret, frame = self.camera.read()
		if not ret:
			return
		frame = cv2.resize(frame, (620, 372))
		if saveTodisk:
			
			self.saveImage(frame)
		mQImage = cv2ImagaeToQtImage(frame)
		self.painter.setImageData(mQImage)

	def createListView(self):
		listView = QtGui.QListView()
		entries = ['one',u'\u2713' + 'two', 'three']
		listView.setModel(self.model)
		for i in entries:
			self.model.pushBack(i)
		return listView

		

	def createImageBox(self):
		self.painter = PainterWidget()
		wrapperLayout = QtGui.QGridLayout()
		wrapperLayout.addWidget(self.painter, 0, 0, 12, 10)
		wrapperLayout.addWidget(self.createListView(), 0, 13, 12, 2)
		self.wrapperBox 	= QtGui.QGroupBox()
		self.wrapperBox.setLayout(wrapperLayout)
		return self.wrapperBox

	def createMainGui(self):
		buttonGroupBox = self.createBottomGroupBox()
		imageGroupBox = self.createImageBox()
		layout = QtGui.QGridLayout()
		layout.addWidget(imageGroupBox, 0, 0, 12, 12)
		layout.addWidget(buttonGroupBox, 13, 0, 1, 12)
		self.main_frame = QtGui.QWidget()
		self.main_frame.setLayout(layout)
		self.setCentralWidget(self.main_frame)

	def exitElegantly(self):
		self.timer.stop()
		self.close()

	def create_menu(self):
		self.file_menu = self.menuBar().addMenu("&File")
		
		getImageAction = self.create_action("snapShot",
			shortcut="Ctrl+I", slot=self.snapShot, tip="take a picture")
		
		exit_action = self.create_action("E&xit", slot=self.exitElegantly, 
			shortcut="Ctrl+W", tip="Exit the application")

		
		self.add_actions(self.file_menu, 
			(   getImageAction,
				None, exit_action))
		
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

	def create_action(  self, text, slot=None, shortcut=None, 
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
		
		
def main():
	
	app = QtGui.QApplication(sys.argv)
	# MedicalRecordDialog.newRecord()
	ex = ImageCapture()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()