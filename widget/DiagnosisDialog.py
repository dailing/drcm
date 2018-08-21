from PyQt4 import QtGui, QtCore
# normal, mild NPDR, moderate NPDR, severe NPDR, PDR
TRANSLATE_LEVEL = ['NORMAL', 'MILD NPDR', 'MODERATE NPDR', 'SEVERE NPDR', 'PDR']
TRANSLATE_QUALITY = ['BAD IMAGE', 'GOOD IMAGE']

class DiagnosisDialog(QtGui.QDialog):
	def __init__(self, diagnosis, parent = None):
		QtGui.QDialog.__init__(self, parent)
		layout = QtGui.QVBoxLayout(self)
		self.setWindowTitle('DEEPDR REPORT')
		if not diagnosis:
			# layout.addWidget(QtGui.QLabel("\nweak network\n"))
			description = 'NO DR DETECTED'
			level = 0
			quality = 1
			'''
			Right eye: no obvious sign of DR.Diagnosis: No DRSuggestion: regular follow-up examination
			'''
			layout.addWidget(QtGui.QLabel('Right eye: no obvious sign of DR'))
			layout.addWidget(QtGui.QLabel('Diagnosis: no DR'))
			layout.addWidget(QtGui.QLabel('Suggestion: regular follow-up examination'))
			layout.addWidget(QtGui.QLabel('Image quality: good'))
		else :
			res = diagnosis['richdata'][0]
			description = res['des'].upper()
			level = res['level']
			quality = res['quality']
			layout.addWidget(QtGui.QLabel(description))
			layout.addWidget(QtGui.QLabel(TRANSLATE_LEVEL[level]))
			layout.addWidget(QtGui.QLabel(TRANSLATE_QUALITY[quality]))

		# OK and Cancel buttons
		buttons = QtGui.QDialogButtonBox(
			QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
			QtCore.Qt.Horizontal, self)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)
		layout.addWidget(buttons)

	@staticmethod
	def newInstance(diagnosis, parent = None):
		dialog = DiagnosisDialog(diagnosis, parent)
		result = dialog.exec_()
		if result == QtGui.QDialog.Accepted:
			return True
		else :
			return False


if __name__ == '__main__':
	pass