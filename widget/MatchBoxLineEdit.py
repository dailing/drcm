from PyQt4 import QtGui
import subprocess
class MatchBoxLineEdit(QtGui.QLineEdit):
	def focusInEvent(self, e):
		try:
			subprocess.Popen(["wmctrl -r keyboard -e"])
		except FileNotFoundError:
			pass

	def focusOutEvent(self,e):
		subprocess.Popen(["killall","wmctrl"])