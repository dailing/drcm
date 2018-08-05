from PyQt4 import QtGui
import subprocess
class MatchBoxLineEdit(QtGui.QLineEdit):
	def focusInEvent(self, e):
		try:
			subprocess.Popen(["matchbox-keyboard"])
		except FileNotFoundError:
			pass

	def focusOutEvent(self,e):
		subprocess.Popen(["killall","matchbox-keyboard"])