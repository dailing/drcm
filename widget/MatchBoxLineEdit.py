from PyQt4 import QtGui
import subprocess
class MatchBoxLineEdit(QtGui.QLineEdit):
	def focusInEvent(self, e):
		try:
			subprocess.Popen(["wmctrl -r keyboard -e 0, 100,200,300,400"])
		except FileNotFoundError:
			pass

	def focusOutEvent(self,e):
		subprocess.Popen(["killall","matchbox-keyboard"])