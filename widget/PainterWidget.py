from PyQt4 import QtGui, QtCore

class PainterWidget(QtGui.QWidget):
		def __init__(self, parent=None):
				QtGui.QWidget.__init__(self, parent)
				self.image = QtGui.QImage()
				width, height = 640, 480
				self._min_size = (width, height)
				self.resize(width, height)
				self.image = QtGui.QImage(width, height, QtGui.QImage.Format_RGB888)
				self.update()

		def setImageData(self, image_data):
				self.image = image_data
				self.setMinimumSize(self.image.size())
				self.update()

		

		def paintEvent(self, event):
				painter = QtGui.QPainter(self)
				# painter.begin(self)
				painter.drawImage(0, 0, self.image)
				# painter.end()