from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSlot, pyqtSignal
import os, sys

sys.path.append(os.path.dirname(os.path.realpath('.')))
from widget.VideoView import VideoView
from widget.RecordListView import RecordListView
from widget.MedicalRecordDialog import MedicalRecordDialog
from widget.NewRecordWidget import NewRecordWidget
from widget.ImageViewer import ImageViewer
from utils.logFormatter import setupLogger
from widget.HeadWidget import HeadWidget
from network.wifiWidget import WifiTableView

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
        self.wifi_config_widget = WifiTableView()
        self.image_viewer = ImageViewer()
        self.pageId = [
            self.record_list,
            self.medical_record_dialog,
            self.video_view,
            self.new_record_widget,
            self.wifi_config_widget,
            self.image_viewer,
        ]
        self.record_list.refresh()
        for w in self.pageId:
            self.stacked_widget.addWidget(w)

        self.nextPageId = -1
        self.currentPageState = None

        self.record_list.record_list_clicked.connect(self.record_list_clicked)
        self.video_view.video_leave_signal.connect(lambda :self.nav2(self.medical_record_dialog))
        self.record_list.new_record_clicked.connect(lambda: self.nav2(self.new_record_widget))
        self.record_list.wifi_config_clicked.connect(lambda: self.nav2(self.wifi_config_widget))
        self.new_record_widget.add_record_clicked.connect(lambda: (self.nav2(self.record_list), self.record_list.refresh()))
        # self.head_widget.click_left_icon.connect(lambda : self.nev_previous())
        self.medical_record_dialog.open_camera_clicked.connect(self.open_camera_clicked)
        self.wifi_config_widget.back_clicked.connect(lambda : self.nav2(self.record_list))
        self.medical_record_dialog.back_clicked.connect(lambda : self.nav2(self.record_list))
        self.new_record_widget.back_clicked.connect(lambda : self.nav2(self.record_list))
        self.medical_record_dialog.view_image_signal.connect(
            lambda pid:(self.image_viewer.set_pid(str(pid)), self.nav2(self.image_viewer))
        )
        self.image_viewer.back_clicked.connect(
            lambda : self.nav2(self.medical_record_dialog)
        )

        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.addWidget(self.head_widget)
        self.main_layout.addWidget(self.stacked_widget)
        self.main_layout.setMargin(0)
        self.main_widget.setLayout(self.main_layout)
        self.nav2(self.record_list)


    def nav2(self, item):
        logger.info('nav2 called' + str(item))
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
            logger.debug(self.pageId[item])
            self.head_widget.setRightIcon(self.pageId[item].custom_right_header)
        if hasattr(self.pageId[item], 'custom_left_header'):
            logger.debug(self.pageId[item])
            self.head_widget.setLeftIcon(self.pageId[item].custom_left_header)
        if hasattr(self.pageId[item], 'header_title'):
            logger.debug('setting header title:{}'.format(self.pageId[item].header_title))
            self.head_widget.middleText.setText(self.pageId[item].header_title)

    # def nev_previous(self):
    #     logger.debug('previous')
    #     currentWidget = self.stacked_widget.currentIndex()
    #     logger.debug(currentWidget)
    #     currentWidget = (currentWidget-1) % len(self.pageId)
    #     logger.debug(currentWidget)
    #     self.nav2(currentWidget)


    def record_list_clicked(self, item):
        logger.debug('item:{} clicked.'.format(item))
        print ('\n\n', self.record_list.recordList)
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

    def open_camera_clicked(self):
        self.video_view.fillRecord(self.medical_record_dialog.getPatientInfo())
        self.nav2(self.video_view)

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
