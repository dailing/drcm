from PyQt4 import QtGui, QtCore
import sys
from HeadWidget import HeadWidget
from PatientDataFormat import PatientInfo
class QCustomQWidget (QtGui.QWidget):
	def __init__ (self, patient, parent = None):
		super(QCustomQWidget, self).__init__(parent)
		self.patient = patient
		self.iconQLabel      = QtGui.QLabel()
		if patient.isMale():
			self.iconQLabel.setPixmap(QtGui.QPixmap('male_48.png'))
		else :
			self.iconQLabel.setPixmap(QtGui.QPixmap('female_48.png'))
		self.nameQLabel = QtGui.QLabel(patient.getName())
		self.pidQLabel = QtGui.QLabel(patient.getPid())
		self.createTimeQLabel = QtGui.QLabel(patient.getCreationTime())
		self.allQHBoxLayout = QtGui.QHBoxLayout()
		self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
		self.allQHBoxLayout.addStretch(1)
		self.allQHBoxLayout.addWidget(self.nameQLabel, 1)
		self.allQHBoxLayout.addWidget(self.pidQLabel, 2)
		self.allQHBoxLayout.addWidget(self.createTimeQLabel, 3)
		self.setLayout(self.allQHBoxLayout)
	def getPatient(self):
		return self.patient
		
class RecordListView(QtGui.QListWidget):
	"""docstring for RecordListView"""

	def __init__(self, pageManager, recordList = []):
		QtGui.QListWidget.__init__(self)
		self.setGeometry(200, 200, 800, 480)
		self.setStyleSheet( "QListWidget::item { border-bottom: 1px solid #999999; }");

		self.clicked.connect(self.expandRecord)

		self.recordList = recordList
		self.pm = pageManager

		#add head bar
		myQCustomQWidget = HeadWidget('Record list')
		myQCustomQWidget.setLeftIcon('back_48.png')
		myQCustomQWidget.setRightIcon('new_record.png')
		item = QtGui.QListWidgetItem(self)
		item.setSizeHint(myQCustomQWidget.sizeHint())
		myQCustomQWidget.resize(item.sizeHint())
		self.addItem(item)
		self.setItemWidget(item, myQCustomQWidget)
		myQCustomQWidget.leftLabel().mousePressEvent = self.backEvent
		myQCustomQWidget.rightLabel().mousePressEvent = self.newRecord

		pass

	def setPageManager(self, pm):
		self.pm = pm

	def newRecord(self, event):
		#emit signal

		print ('new Record')

	def expandRecord(self, event):
		row = event.row()
		if 0 == row :
			return
		#put patient to page manager
		#emit signal
		self.pm.setState(self.recordList[row])
		print ('expand')

	def backEvent(self, event):
		#emit signal

		print (event)

	def setState(self, state):
		self.state = state
		#to do : clear view and repaint

	def getState(self):
		return self.selectedRecord


	def appendRow(self, patient):
		myQCustomQWidget = QCustomQWidget(patient)
		item = QtGui.QListWidgetItem(self)
		item.setSizeHint(myQCustomQWidget.sizeHint())
		self.addItem(item)
		self.setItemWidget(item, myQCustomQWidget)

	def initDefault(self):
		# if self.state is not []:
		# 	for record in self.state:
		# 		self.appendRow(record)
		# 	return
		for record in [
			PatientInfo('name', '1234', False, '2018-09-08', True),
			PatientInfo('other', '1244', True, '2018-09-08', True)] :
			self.appendRow(record)

app = QtGui.QApplication([])
window = RecordListView(None)
window.initDefault()
window.show()
sys.exit(app.exec_())
