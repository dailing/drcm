from PyQt4 import QtGui
import subprocess
from utils.logFormatter import setupLogger
#http://wiki.openmoko.org/wiki/Change_matchbox_keyboard_layout
#http://ozzmaker.com/virtual-keyboard-for-the-raspberry-pi/
logger = setupLogger('MatchBoxLineEdit')

class MatchBoxLineEdit(QtGui.QLineEdit):
	def focusInEvent(self, e):
		try:
			logger.debug('matchbox foucus in')
			subprocess.Popen(["matchbox-keyboard", "-i"])
		except FileNotFoundError:
			pass

	def focusOutEvent(self,e):
		logger.debug('matchbox foucus out')
		subprocess.Popen(["killall","matchbox-keyboard"])

if __name__=="__main__":
	subprocess.Popen(["matchbox-keyboard", "numword"])
