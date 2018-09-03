from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSlot, pyqtSignal
import os, sys

sys.path.append(os.path.dirname(os.path.realpath('.')))
from widget.VideoView import VideoView
from widget.RecordListView import RecordListView
from widget.MedicalRecordDialog import MedicalRecordDialog
from widget.NewRecordWidget import NewRecordWidget
from utils.logFormatter import setupLogger
from widget.HeadWidget import HeadWidget

logger = setupLogger('page_manager')


class PageManager(QtCore.QObject):
    """docstring for PageManager"""
    recordList2patientSignal = QtCore.pyqtSignal(object)

    def __init__(self):
        QtCore.QObject.__init__(self)
        self.head_widget = HeadWidget('you dont need it')
        self.main_widget = QtGui.QWidget()

        self.stacked_widget = QtGui.QStackedWidget()
        # define each sub page
        self.record_list = RecordListView(self)
        self.medical_record_dialog = MedicalRecordDialog(self)
        self.video_view = VideoView(self)
        self.new_record_widget = NewRecordWidget(self)
        self.pageId = [
            self.record_list,
            self.medical_record_dialog,
            self.video_view,
            self.new_record_widget,
        ]
        self.record_list.refresh()
        for w in self.pageId:
            self.stacked_widget.addWidget(w)

        self.nextPageId = -1
        self.currentPageState = None

        self.record_list.record_list_clicked.connect(self.record_list_clicked)
        self.video_view.video_leave_signal.connect(lambda :self.nav2(self.record_list))

        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.addWidget(self.head_widget)
        self.main_layout.addWidget(self.stacked_widget)
        self.main_widget.setLayout(self.main_layout)
        self.nav2(self.video_view)


    def nav2(self, item):
        logger.info('nav2 called')
        if type(item) is int:
            pass
        else:
            item = self.pageId.index(item)
        logger.debug('jumping to index:{}'.format(item))
        self.stacked_widget.setCurrentIndex(item)
        if hasattr(self.pageId[item], 'no_head') and \
                self.pageId[item].no_head:
            self.head_widget.hide()
        else:
            self.head_widget.show()
        if hasattr(self.pageId[item], 'custom_right_header'):
            self.head_widget.setRightIcon(self.pageId[item].custom_right_header)

    def record_list_clicked(self, item):
        logger.debug('item:{} clicked.'.format(item))
        self.medical_record_dialog.fillRecord(self.record_list.recordList[item])
        self.nav2(self.medical_record_dialog)

    def navBack2PatientPage(self):
        self.stacked_widget.setCurrentIndex(1)

    def navBack2RecordListPage(self):
        self.stacked_widget.setCurrentIndex(0)
        pass

    def createRecord(self):
        self.stacked_widget.setCurrentIndex(3)

    def saveRecord(self, patient):
        self.pageId[0].appendRow(patient)
        self.stacked_widget.setCurrentIndex(0)

    def nav2PatientPage(self, patient):
        self.pageId[1].fillRecord(patient)
        self.stacked_widget.setCurrentIndex(1)

    def nav2VideoPage(self, patient):
        self.pageId[2].fillRecord(patient)
        self.stacked_widget.setCurrentIndex(2)

    def getWidget(self):
        return self.main_widget

    def setNextPageId(self, pageId):
        self.nextPageId = pageId

    def setCurrentPageState(self, state):
        self.currentPageState = state

    def addWidget(self, widget):
        self.pageId.append(widget)

    def getPageId(self, page):
        for i in range(len(self.pageId)):
            if page == self.pageId:
                return i
        return -1

    def nextPage(self):
        if self.nextPageId == -1:
            # error
            return
        self.pageId[self.nextPageId].setState(self.currentPageState)
        self.stacked_widget.setCurrentIndex(self.nextPageId)
