from PyQt4 import QtCore, QtGui
import os, sys
sys.path.append(os.path.dirname(os.path.realpath('.')))
from widget.VideoView import VideoView
from widget.RecordListView import RecordListView
from widget.MedicalRecordDialog import MedicalRecordDialog
from widget.PatientDataFormat import PatientInfo
class PageManager(QtCore.QObject):
	"""docstring for PageManager"""
	recordList2patientSignal = QtCore.pyqtSignal(object)
	def __init__(self):
		QtCore.QObject.__init__(self)
		self.stacked_widget = QtGui.QStackedWidget()
		self.pageId = [
			RecordListView(self, [
			PatientInfo('name', '1234', False, '2018-09-08', True),
			PatientInfo('other', '1244', True, '2018-09-08', True)]),
			MedicalRecordDialog(self),
			VideoView(self)
		]
		self.pageId[0].initDefault()
		for w in self.pageId :
			self.stacked_widget.addWidget(w)

		self.nextPageId = -1
		self.currentPageState = None


		# self.recordList2patientSignal.connect(self.nav2PatientPage)

	def navBack2PatientPage(self):
		self.stacked_widget.setCurrentIndex(1)

	def navBack2RecordListPage(self):
		self.stacked_widget.setCurrentIndex(0)
		pass

	def nav2PatientPage(self, patient):
		self.pageId[1].fillRecord(patient)
		self.stacked_widget.setCurrentIndex(1)

	def nav2VideoPage(self, patient):
		self.pageId[2].fillRecord(patient)
		self.stacked_widget.setCurrentIndex(2)

	def getWidget(self):
		return self.stacked_widget

	def setNextPageId(self, pageId):
		self.nextPageId = pageId

	def setCurrentPageState(self, state):
		self.currentPageState = state

	def addWidget(self, widget):
		self.pageId.append(widget)

	def getPageId(self, page):
		for i in range(len(self.pageId)):
			if page ==  self.pageId:
				return i
		return -1

	def nextPage(self):
		if self.nextPageId == -1:
			#error
			return
		self.pageId[self.nextPageId].setState(self.currentPageState)
		self.stacked_widget.setCurrentIndex(self.nextPageId)



		