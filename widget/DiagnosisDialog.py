from PyQt4 import QtGui, QtCore

TRANSLATE_LEVEL = ['NO DR', 'MILD DR', 'MODERATE DR', 'SEVERE DR', 'PDR']
TRANSLATE_QUALITY = ['BAD IMAGE', 'GOOD IMAGE']

class DiagnosisDialog(QtGui.QDialog):
	def __init__(self, diagnosis, parent = None):
		QtGui.QDialog.__init__(self, parent)
		res = diagnosis['richdata'][0]
		description = res['des']
		level = res['level']
		quality = res['quality']
		layout = QtGui.QVBoxLayout(self)
		
		
		layout.addWidget(QtGui.QLabel(description))
		layout.addWidget(QtGui.QLabel(TRANSLATE_LEVEL[level])
		layout.addWidget(QtGui.QLabel(TRANSLATE_QUALITY[quality])

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