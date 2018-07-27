from PyQt4 import QtGui, QtCore
from LabelText import LabelText
from LabelDate import LabelDate

from SingleChoiceButton import SingleChoiceButton

from PatientDataFormat import PatientInfo


class MedicalRecordDialog(QtGui.QDialog):
	def __init__(self, default, parent = None):
		QtGui.QDialog.__init__(self, parent)

		layout = QtGui.QVBoxLayout(self)

		self.patientName = LabelText(
			' name '
			)
		self.patientName.setText(
			'' if default is None else default.getName()
			)
		layout.addWidget(self.patientName)
		self.patientId = LabelText(
			'  ID  '
			)
		self.patientId.setText('' if default is None else default.getPid())
		layout.addWidget(self.patientId)


		self.gender = SingleChoiceButton('gender',  ['male', 'female'])
		if default is not None:
			self.gender.setOption(default.isMale())
		layout.addWidget(self.gender)

		#patient address
		self.eye = SingleChoiceButton("eye", ['left', 'right'])
		if default is not None:
			self.eye.setOption(default.isLeftEye())
		layout.addWidget(self.eye)

		# nice widget for editing the date
		self.patientBirthDay = LabelDate('birthDay')
		layout.addWidget(self.patientBirthDay)


		


		# OK and Cancel buttons
		buttons = QtGui.QDialogButtonBox(
			QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
			QtCore.Qt.Horizontal, self)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)
		layout.addWidget(buttons)

	def getPatientInfo(self):
		'''
			name, pid, gender, birthday, leftEye, timestamp, uuid, data
		'''
		return PatientInfo(self.patientName.getText(), 
			self.patientId.getText(),
			self.gender.getOption() == 'male' ,
			self.patientBirthDay.getTime(),
			self.eye.getOption() == 'left', None, None, None)

	@staticmethod
	def newRecord(default, parent = None):
		dialog = MedicalRecordDialog(default, parent)
		result = dialog.exec_()
		if result == QtGui.QDialog.Accepted:
			return (dialog.getPatientInfo()), True
		else :
			return None, False