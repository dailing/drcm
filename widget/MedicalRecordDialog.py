from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignal
from LabelPair import LabelPair
from LabelDate import LabelDate
from SingleChoiceButton import SingleChoiceButton
from utils.logFormatter import setupLogger

logger = setupLogger('medical_record_dialog')


class MedicalRecordDialog(QtGui.QWidget):
	open_camera_signal = pyqtSignal(name='open_camera_signal()')

	def __init__(self, pageManager, parent = None):
		QtGui.QWidget.__init__(self, parent)
		# todo remove the pm dependency
		self.pm = pageManager

		layout = QtGui.QVBoxLayout(self)
		self.patientName = LabelPair(
			'name', 'patient'
			)
		layout.addWidget(self.patientName)
		self.patientId = LabelPair('  pid  ', '1111')
		layout.addWidget(self.patientId)
		self.gender = LabelPair(' sex ',  'male')
		layout.addWidget(self.gender)

		# nice widget for editing the date
		self.patientBirthDay = LabelPair('created', '1949-01-01')
		layout.addWidget(self.patientBirthDay)
		layout.addStretch(1)
		self.setStyleSheet("color : white;")

	def fillRecord(self, patient):
		logger.debug('filling {}'.format(patient))
		self.patient = patient
		self.images = patient.get_images()
		# TODO add images to the widget
		for i in self.images:
			logger.info(i)
		self.patientName.setText(
			patient.getName()
			)
		self.patientId.setText(patient.getPid())
		self.gender.setOption(patient.isMale())


	# def getImageInfo(self):
	# 	return ImageInfo(self.patientName.getText(),
	# 		self.patientId.getText(),
	# 		self.gender.getOption() == 'male' ,
	# 		self.patientBirthDay.getText())

	# def getPatientInfo(self):
	# 	'''
	# 		name, pid, gender, birthday, timestamp, uuid, data
	# 	'''
	# 	return PatientInfo(self.patientName.getText(),
	# 		self.patientId.getText(),
	# 		self.gender.getOption() == 'male' ,
	# 		self.patientBirthDay.getTime(),
	# 		self.eye.getOption() == 'left', None, None, None)


	# def back_on_click_handler(self, event):
	# 	logger.debug ('nav back')
	# 	self.pm.navBack2RecordListPage()
	# 	pass
	#
	# def camera_on_click_handler(self, event):
	# 	logger.debug ('open ca')
	# 	self.open_camera_signal.emit()
		# self.pm.nav2VideoPage(self.patient)

	# @staticmethod
	# def newRecord(default, parent = None):
	# 	dialog = MedicalRecordDialog(default, parent)
	# 	result = dialog.exec_()
	# 	if result == QtGui.QDialog.Accepted:
	# 		return (dialog.getPatientInfo()), True
	# 	else :
	# 		return None, False

def main():
	import sys
	app = QtGui.QApplication(sys.argv)
	ex = MedicalRecordDialog(None)
	ex.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()