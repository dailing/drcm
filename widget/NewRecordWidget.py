from PyQt4 import QtGui, QtCore
from LabelText import LabelText
from LabelDate import LabelDate

from SingleChoiceButton import SingleChoiceButton

from PatientDataFormat import PatientInfo, ImageInfo

from HeadWidget import HeadWidget
class NewRecordWidget(QtGui.QWidget):
	def __init__(self, pageManager, parent = None):
		QtGui.QWidget.__init__(self, parent)
		self.resize(800, 480)
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

		# nice widget for editing the date
		self.bornAt = LabelDate('born')
		layout.addWidget(self.bornAt)

		self.setStyleSheet("color : white;")

	def getPatientInfo(self):
		'''
			name, pid, gender, birthday, leftEye
		'''
		return PatientInfo(self.patientName.getText(), 
			self.patientId.getText(),
			self.gender.getOption() == 'male' ,
			self.bornAt.getTime())

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
		self.pm.saveRecord(self.getPatientInfo())

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