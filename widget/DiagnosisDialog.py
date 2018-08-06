from PyQt4 import QtGui, QtCore

class DiagnosisDialog(QtGui.QDialog):
	def __init__(self, diagnosis, parent = None):
		QtGui.QDialog.__init__(self, parent)
		res = diagnosis['richdata'][0]
		description = res['des']
		level = str(res['level'])
		quality = str(res['quality'])
		layout = QtGui.QVBoxLayout(self)
		
		
		layout.addWidget(QtGui.QLabel(description))
		layout.addWidget(QtGui.QLabel('level : ' + level))
		layout.addWidget(QtGui.QLabel('quality : ' + quality))

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