from PyQt4 import QtGui, QtCore
from LabelText import LabelText
from LabelDate import LabelDate

from SingleChoiceButton import SingleChoiceButton

from PatientDataFormat import PatientInfo


class LineEditDialog(QtGui.QDialog):
	def __init__(self, defaultLabel, parent = None):
		QtGui.QDialog.__init__(self, parent)

		layout = QtGui.QVBoxLayout(self)
		self.editInput = LabelText(
			defaultLabel
			)
		
		layout.addWidget(self.editInput)

		# OK and Cancel buttons
		buttons = QtGui.QDialogButtonBox(
			QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
			QtCore.Qt.Horizontal, self)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)
		layout.addWidget(buttons)

	def setText(self, text):
		self.editInput.setText(text)

	def getText(self):
		'''
			name, pid, gender, birthday, leftEye, timestamp, uuid, data
		'''
		return self.editInput.getText()

	@staticmethod
	def newInstance(defaultLabel, defaultText = '', parent = None):
		dialog = LineEditDialog(defaultLabel, parent)
		dialog.setText(defaultText)
		result = dialog.exec_()
		if result == QtGui.QDialog.Accepted:
			return str(dialog.getText()), True
		else :
			return '', False