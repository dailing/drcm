from PyQt4 import QtGui, QtCore
from LabelText import LabelText
from LabelDate import LabelDate

from SingleChoiceButton import SingleChoiceButton

from utils.icons import get_icon
from model.patient import Patient
import model

from HeadWidget import HeadWidget
from utils.logFormatter import setupLogger

logger = setupLogger('new_record_list')

class NewRecordWidget(QtGui.QWidget):
	add_record_clicked = QtCore.pyqtSignal(name='new_record_click()')
	back_clicked = QtCore.pyqtSignal(name = 'back_clicked()')
	def __init__(self, pageManager, parent = None, patients=None):
		QtGui.QWidget.__init__(self, parent)
		self.resize(800, 480)
		self.pm = pageManager

		layout = QtGui.QVBoxLayout(self)
		self.patientName = LabelText(' name ')
		self.patientName.setText('bob')
		layout.addWidget(self.patientName)
		self.patientId = LabelText('  ID  ')
		self.patientId.setText('1212')
		layout.addWidget(self.patientId)
		self.gender = SingleChoiceButton('gender',  ['male', 'female'])
		layout.addWidget(self.gender)

		#patient address
		# nice widget for editing the date
		self.bornAt = LabelDate('born')
		layout.addWidget(self.bornAt)
		self.setStyleSheet("color : white;")
		self.patients = model.patient.Patients()


	@property
	def custom_right_header(self):
		right_header = get_icon('save_record')
		right_header.mouseReleaseEvent = self.save_on_click_handler
		return right_header

	@property
	def custom_left_header(self):
		logger.debug('custom_left_header')
		left_header = get_icon('back')
		logger.debug('get icon for custom_left_header')

		left_header.mouseReleaseEvent = lambda event:self.back_clicked.emit()
		return left_header


	def getPatientInfo(self):
		'''
			name, pid, gender, birthday, leftEye
		'''
		return Patient(
			name =self.patientName.getText(),
			pid = self.patientId.getText(),
			gender = int(self.gender.getOption() == 'male'),
			birthday = self.bornAt.getTime())

	def createHeadWidget(self):
		myQCustomQWidget = HeadWidget('Record list')
		myQCustomQWidget.setLeftIcon('icons/back_48.png')
		myQCustomQWidget.setRightIcon('icons/save_48.png')
		myQCustomQWidget.rightLabel().mousePressEvent = self.save_on_click_handler
		myQCustomQWidget.leftLabel().mousePressEvent = self.back_on_click_handler
		return myQCustomQWidget

	def back_on_click_handler(self, event):
		self.pm.navBack2RecordListPage()
		pass

	def save_on_click_handler(self, event):
		#save if all set
		if self.patientName.getText() == '' or self.patientId.getText() == '':
			QtGui.QMessageBox.warning(
				QtGui.QWidget(), "Field warning", "All text must be set!")
			return

		self.patients.add_patient(
			name =self.patientName.getText(),
			pid = self.patientId.getText(),
			gender = int(self.gender.getOption() == 'male'),
			birthday = self.bornAt.getTime(),
		)
		self.add_record_clicked.emit()

	# @staticmethod
	# def newRecord(default, parent = None):
	# 	dialog = MedicalRecordDialog(default, parent)
	# 	result = dialog.exec_()
	# 	if result == QtGui.QDialog.Accepted:
	# 		return (dialog.getPatientInfo()), True
	# 	else :
	# 		return None, False

import sys
def main():
	app = QtGui.QApplication(sys.argv)
	ex = NewRecordWidget(None)
	ex.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()