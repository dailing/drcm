from PyQt4 import QtGui, QtCore
from LabelText import LabelText
from LabelDate import LabelDate

from SingleChoiceButton import SingleChoiceButton

from PatientDataFormat import PatientInfo, ImageInfo

from HeadWidget import HeadWidget
class MedicalRecordDialog(QtGui.QWidget):
	def __init__(self, pageManager, parent = None):
		QtGui.QWidget.__init__(self, parent)
		
		self.pm = pageManager

		layout = QtGui.QVBoxLayout(self)
		layout.addWidget(self.createHeadWidget())
		self.patientName = LabelText(
			' name '
			)
		
		layout.addWidget(self.patientName)
		self.patientId = LabelText(
			'  ID  '
			)
		
		layout.addWidget(self.patientId)


		self.gender = SingleChoiceButton('gender',  ['male', 'female'])
			
		layout.addWidget(self.gender)

		#patient address
		self.eye = SingleChoiceButton("eye", ['left', 'right'])
			
		layout.addWidget(self.eye)

		# nice widget for editing the date
		self.patientBirthDay = LabelDate('time')
		layout.addWidget(self.patientBirthDay)

	def fillRecord(self, patient):
		self.patient = patient
		self.patientName.setText(
			patient.getName()
			)
		self.patientId.setText(patient.getPid())
		self.gender.setOption(patient.isMale())
		self.eye.setOption(patient.isLeftEye())

	def getImageInfo(self):
		return ImageInfo(self.patientName.getText(), 
			self.patientId.getText(),
			self.gender.getOption() == 'male' ,
			self.patientBirthDay.getTime(),
			self.eye.getOption() == 'left')

	def getPatientInfo(self):
		'''
			name, pid, gender, birthday, leftEye, timestamp, uuid, data
		'''
		return PatientInfo(self.patientName.getText(), 
			self.patientId.getText(),
			self.gender.getOption() == 'male' ,
			self.patientBirthDay.getTime(),
			self.eye.getOption() == 'left', None, None, None)

	def createHeadWidget(self):
		myQCustomQWidget = HeadWidget('Record list')
		myQCustomQWidget.setLeftIcon('icons/back_48.png')
		myQCustomQWidget.setRightIcon('icons/camera_48.png')
		myQCustomQWidget.rightLabel().mousePressEvent = self.camera_on_click_handler
		return myQCustomQWidget

	def camera_on_click_handler(self, event):
		self.pm.nav2VideoPage(self.patient)

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
	ex = MedicalRecordDialog()
	ex.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()