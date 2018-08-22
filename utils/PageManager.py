from PyQt4 import QtCore, QtGui

from widget.VideoView import VideoView
from widget.RecordListView import RecordListView
from widget.MedicalRecordDialog import MedicalRecordDialog
class PageManager(QtCore.QObject):
	"""docstring for PageManager"""
	nextPageSignal = QtCore.pyqtSignal()
	def __init__(self):
		QtCore.QObject.__init__(self)
		self.stacked_widget = QtGui.QStackedWidget()
		self.pageId = [
			RecordListView(),
			MedicalRecordDialog(),
			VideoView()
		]
		self.nextPageSignal.connect(self.nextPage)

		self.nextPageId = -1
		self.currentPageState = None

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



		