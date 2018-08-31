from PyQt4 import QtGui, QtCore
import sys
from HeadWidget import HeadWidget
from utils.logFormatter import setupLogger
import model.patient

logger = setupLogger('record_list')


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

	def __init__(self, pageManager, recordList = []):
		QtGui.QListWidget.__init__(self)
		self.setGeometry(200, 200, 800, 480)
		self.setStyleSheet( "QListWidget::item { border-bottom: 1px solid #999999; }");

		self.clicked.connect(self.expandRecord)

		self.recordList = recordList
		self.pm = pageManager
		print(self.pm, pageManager)
		#add head bar
		myQCustomQWidget = HeadWidget('Record list')
		myQCustomQWidget.setLeftIcon('icons/back_48.png')
		myQCustomQWidget.setRightIcon('icons/new_record.png')
		item = QtGui.QListWidgetItem(self)
		item.setSizeHint(myQCustomQWidget.sizeHint())
		# item.setBackgroundColor(QtGui.QColor("#969b2b;"));

		self.addItem(item)
		self.setItemWidget(item, myQCustomQWidget)
		myQCustomQWidget.leftLabel().mousePressEvent = self.backEvent
		myQCustomQWidget.rightLabel().mousePressEvent = self.newRecord

		self.patients = model.patient.Patients()

	def refresh(self):
		self.clear()
		self.recordList = []
		for i in self.patients[:]:
			self.appendRow(i)

	def newRecord(self, event):
		#emit signal
		self.pm.createRecord()

	def expandRecord(self, event):
		row = event.row()
		if 0 == row :
			return
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
		self.recordList.append(patient)

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

