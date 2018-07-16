from PyQt4 import QtGui, QtCore
from LabelText import LabelText
from LabelDate import LabelDate

from SingleChoiceButton import SingleChoiceButton

from DataFormat import PatientInfo


class MedicalRecordDialog(QtGui.QDialog):
	def __init__(self, parent = None):
		super(MedicalRecordDialog, self).__init__(parent)

		layout = QtGui.QVBoxLayout(self)

		self.patientName = LabelText('name')
		layout.addWidget(self.patientName)
		self.patientId = LabelText('ID_No')
		layout.addWidget(self.patientId)

		self.gender = SingleChoiceButton('gender',  ['male', 'female'])
		layout.addWidget(self.gender)

		# nice widget for editing the date
		self.patientBirthDay = LabelDate('birthDay')
		layout.addWidget(self.patientBirthDay)


		#patient address
		self.address = LabelText("address")
		layout.addWidget(self.address)

		# OK and Cancel buttons
		buttons = QtGui.QDialogButtonBox(
			QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
			QtCore.Qt.Horizontal, self)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)
		layout.addWidget(buttons)

	def getPatientInfo(self):
		return PatientInfo(self.patientName.getText(), 
			self.patientId.getText(),
			self.gender.getOption(),
			self.patientBirthDay.getTime(),
			self.address.getText(), None, None, None)

	@staticmethod
	def newRecord(parent = None):
		dialog = MedicalRecordDialog(parent)
		result = dialog.exec_()
		if result == QtGui.QDialog.Accepted:
			return (dialog.getPatientInfo()), True
		else :
			return None, False