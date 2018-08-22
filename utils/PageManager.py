from PyQt4 import QtCore, QtGui

from widget.VideoView import VideoView
from widget.RecordListView import RecordListView
from widget.MedicalRecordDialog import MedicalRecordDialog
from widget.PatientDataFormat import PatientInfo
class PageManager(QtCore.QObject):
	"""docstring for PageManager"""
	nextPageSignal = QtCore.pyqtSignal()
	def __init__(self):
		QtCore.QObject.__init__(self)
		self.stacked_widget = QtGui.QStackedWidget()
		self.pageId = [
			RecordListView([
			PatientInfo('name', '1234', False, '2018-09-08', True),
			PatientInfo('other', '1244', True, '2018-09-08', True)]),
			MedicalRecordDialog(PatientInfo('name', '1234', False, '2018-09-08', True)),
			VideoView()
		]
		for w in self.pageId :
			self.stacked_widget.addWidget(w)
		self.nextPageSignal.connect(self.nextPage)

		self.nextPageId = -1
		self.currentPageState = None

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



		