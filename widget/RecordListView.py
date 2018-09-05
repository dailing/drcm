from PyQt4 import QtGui, QtCore
import sys
from HeadWidget import HeadWidget
from utils.logFormatter import setupLogger
import model.patient
from model.patient import Patient
from utils.icons import get_icon

logger = setupLogger('root.record_list')


class QCustomQWidget (QtGui.QWidget):
	def __init__ (self, patient, parent = None):
		super(QCustomQWidget, self).__init__(parent)
		self.patient = patient
		self.iconQLabel      = QtGui.QLabel()
		if patient.isMale():
			self.iconQLabel.setPixmap(QtGui.QPixmap('icons/male_48.png'))
		else:
			self.iconQLabel.setPixmap(QtGui.QPixmap('icons/female_48.png'))
		self.nameQLabel = QtGui.QLabel(patient.getName())
		self.pidQLabel = QtGui.QLabel(patient.getPid())
		self.createTimeQLabel = QtGui.QLabel(patient.getCreationTime())
		self.allQHBoxLayout = QtGui.QHBoxLayout()
		self.allQHBoxLayout.addWidget(self.iconQLabel, 1)
		self.allQHBoxLayout.addWidget(self.nameQLabel, 1)
		self.allQHBoxLayout.addWidget(self.pidQLabel, 1)
		self.allQHBoxLayout.addWidget(self.createTimeQLabel, 1)
		self.allQHBoxLayout.addStretch(1)
		
		self.setLayout(self.allQHBoxLayout)

	def getPatient(self):
		return self.patient


class RecordListView(QtGui.QListWidget):
	# todo add page here
	"""docstring for RecordListView"""
	record_list_clicked = QtCore.pyqtSignal(int, name='record_list_clicked()')
	new_record_clicked = QtCore.pyqtSignal(name='open_camera_signal()')
	wifi_config_clicked = QtCore.pyqtSignal(name='wifi_config_clicked()')



	def __init__(self, pageManager, recordList = []):
		QtGui.QListWidget.__init__(self)
		self.setGeometry(200, 200, 800, 480)
		self.setStyleSheet( "QListWidget::item { border-bottom: 1px solid #999999; }");

		self.clicked.connect(self.expandRecord)

		self.recordList = recordList
		self.pm = pageManager
		print(self.pm, pageManager)
		#add head bar
		myQCustomQWidget = QtGui.QWidget()
		# myQCustomQWidget.setLeftIcon('icons/back_48.png')
		# myQCustomQWidget.setRightIcon('icons/new_record.png')
		item = QtGui.QListWidgetItem(self)
		# item.setSizeHint(myQCustomQWidget.sizeHint())
		# item.setBackgroundColor(QtGui.QColor("#969b2b;"));

		self.addItem(item)
		self.setItemWidget(item, myQCustomQWidget)
		# myQCustomQWidget.leftLabel().mousePressEvent = self.backEvent
		# myQCustomQWidget.rightLabel().mousePressEvent = self.newRecord
		self.patients = model.patient.Patients()
		self.header_title = 'Records'

	@property
	def custom_right_header(self):
		right_header = get_icon('add_record')
		right_header.mouseReleaseEvent = lambda event:self.new_record_clicked.emit()
		return right_header

	@property
	def custom_left_header(self):
		left_header = get_icon('wifi_config')
		left_header.mouseReleaseEvent = lambda event:self.wifi_config_clicked.emit()
		return left_header

	def refresh(self):
		logger.debug('refresh table')
		self.clear()
		self.recordList = self.patients[:]
		pp = Patient('test_pathent1', '1234')
		self.recordList.insert(0, pp)
		self.appendRow(pp)
		for i in self.patients[:]:
			self.appendRow(i)

	def expandRecord(self, event):
		row = event.row()
		logger.debug('expand item:{}'.format(row))
		self.record_list_clicked.emit(row)

	def backEvent(self, event):
		#emit signal
		print (event)

	def setState(self, state):
		self.state = state
		# todo : clear view and repaint

	def getState(self):
		return self.selectedRecord


	def appendRow(self, patient):
		myQCustomQWidget = QCustomQWidget(patient)
		item = QtGui.QListWidgetItem(self)
		item.setSizeHint(myQCustomQWidget.sizeHint())
		self.addItem(item)
		self.setItemWidget(item, myQCustomQWidget)
		

	# def initDefault(self):
	# 	# if self.state is not []:
	# 	# 	for record in self.state:
	# 	# 		self.appendRow(record)
	# 	# 	return
	# 	for record in [
	# 		PatientInfo('name', '1234', False, '2018-09-08', True),
	# 		PatientInfo('other', '1244', True, '2018-09-08', True),
	# 		PatientInfo('other', '1244', True, '2018-09-08', True),
	# 		PatientInfo('other', '1244', True, '2018-09-08', True),
	# 		PatientInfo('other', '1244', True, '2018-09-08', True),
	# 		PatientInfo('other', '1244', True, '2018-09-08', True)] :
	# 		self.appendRow(record)
	# 	return self


def main():
	app = QtGui.QApplication([])
	window = RecordListView(None)
	window.initDefault()
	window.refresh()
	window.show()
	app.exec_()
	return ss


if __name__ == '__main__':
	ss = main()

