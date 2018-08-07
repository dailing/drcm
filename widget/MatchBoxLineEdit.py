from PyQt4 import QtGui
import subprocess
#http://wiki.openmoko.org/wiki/Change_matchbox_keyboard_layout
#http://ozzmaker.com/virtual-keyboard-for-the-raspberry-pi/
class MatchBoxLineEdit(QtGui.QLineEdit):
	def focusInEvent(self, e):
		try:
			subprocess.Popen(["matchbox-keyboard numword"])
		except FileNotFoundError:
			pass

	def focusOutEvent(self,e):
		subprocess.Popen(["killall","matchbox-keyboard"])

if __name__=="__main__":
	subprocess.Popen(["matchbox-keyboard", "numword"])
