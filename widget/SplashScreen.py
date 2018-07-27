from PyQt4 import QtGui
import time
class SplashScreen(QtGui.QSplashScreen):
	def __init__(self, imgFile):
		QtGui.QSplashScreen.__init__(self, QtGui.QPixmap(imgFile))
		self.setGeometry(0, 0, 800, 480)
		

	def effect(self):
		self.setWindowOpacity(0)
		for i in range(50):
			newOpacity = self.windowOpacity() + 0.02
			if newOpacity > 1:
				break

			self.setWindowOpacity(newOpacity)
			self.show()
			time.sleep(0.04)
		for i in range(50):
			newOpacity = self.windowOpacity() - 0.02
			if newOpacity < 0:
				break

			self.setWindowOpacity(newOpacity)
			self.show()
			time.sleep(0.04)


		