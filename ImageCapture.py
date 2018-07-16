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


from PainterGui import PainterGui
from MedicalRecordDialog  import MedicalRecordDialog

from utils import getTimeStamp, getDateTimeFromTS, getUUID

from conn.conn import Uploader


				
class ImageCapture(QtGui.QMainWindow):

	FRAME_PER_SECOND = 12
	UPDATE_FREQ = 1000.0 / FRAME_PER_SECOND
	
	def __init__(self):
		super(ImageCapture, self).__init__()
		self.initEnv()
		self.initUI()

	def initEnv(self):
		self.timer = QtCore.QTimer()
		self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.updateFrame)
		self.camera = cv2.VideoCapture(0)
		self.model = QtGui.QStandardItemModel()
		self.thread = Uploader()
		self.thread.start()
		self.connect(self.thread, 
			SIGNAL("pic_upload_finished(bool)"), 
			self.saveImageCallBack)
		
	def initUI(self):
		self.setWindowTitle('Image UI')
		self.setGeometry(300, 300, 800, 600)
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
			
		captureButton = addButton('Capture', self.snapShot)
		pageButton = addButton('newRecord', self.newRecord)
		uploadButton  = addButton('Upload', self.uploadImages)

		self.patientName = QtGui.QLabel('name')
		bottomLayout.addWidget(self.patientName)

		buttonGroupBox = QtGui.QGroupBox('Button group')
		buttonGroupBox.setLayout(bottomLayout)

		self.timer.start(ImageCapture.UPDATE_FREQ)
		
		return buttonGroupBox

	def uploadImages(self):
		print('upload images')
		

	def uploadCallBack(self):
		#retrive data
		#update list view
		pass


	def snapShot(self):
		self.scheduleUpdating()
		self.updateFrame(True)

		

	def saveImage(self, imageData):
		ts = getTimeStamp()
		dt = getDateTimeFromTS(ts)
		foo = '{}_{}'.format(self.patientInfo[0], dt)
		self.insertFrontToList(foo)
		self.patientInfo.setUTC(ts)
		self.patientInfo.setUUID(getUUID())
		self.patientInfo.setData(imageData)
		# to do: push to DB


	def saveImageCallBack(self, isSucceed):
		print(isSucceed)


	def newRecord(self):
		reply, okPressed = MedicalRecordDialog.newRecord();
		print(reply)
		if okPressed:
			self.patientInfo = reply
			self.patientName.setText(self.patientInfo.getName())
			self.imCnt = 0

	def scheduleUpdating(self):
		if self.timer.isActive():
			self.timer.stop()
		else :
			self.timer.start(ImageCapture.UPDATE_FREQ)

	def updateFrame(self, saveTodisk = False):
		# Capture frame-by-frame
		ret, frame = self.camera.read()
		if not ret:
			return
		if saveTodisk:
			self.saveImage(frame)
		mQImage = cv2ImagaeToQtImage(frame)
		self.painter.setImageData(mQImage)

	def insertFrontToList(data):
		if self.model:
			self.model.insetRow(0, QtGui.QStandardItem(data))

	def appendLastToList(data):
		if self.model:
			self.model.appendRow(QtGui.QStandardItem(data))

	def createListView(self):
		listView = QtGui.QListView()
		entries = ['one',u'\u2713' + 'two', 'three']
		listView.setModel(self.model)
		for i in entries:
			item = QtGui.QStandardItem(i)
			self.model.appendRow(item)
		return listView

		

	def createImageBox(self):
		self.painter = PainterGui()
		wrapperLayout = QtGui.QGridLayout()
		wrapperLayout.addWidget(self.painter, 0, 0, 12, 12)
		wrapperLayout.addWidget(self.createListView(), 0, 13, 12, 4)

		self.wrapperBox 	= QtGui.QGroupBox("Image")
		self.wrapperBox.setLayout(wrapperLayout)
		return self.wrapperBox

	def createMainGui(self):
		buttonGroupBox = self.createBottomGroupBox()
		imageGroupBox = self.createImageBox()
		layout = QtGui.QGridLayout()
		layout.addWidget(imageGroupBox, 0, 0, 12, 12)
		layout.addWidget(buttonGroupBox, 13, 0, 1, 1)
		self.main_frame = QtGui.QWidget()
		# self.setLayout(layout)
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
			shortcut="Ctrl+X", tip="Exit the application")

		
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