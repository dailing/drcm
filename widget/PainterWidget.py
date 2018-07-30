from PyQt4 import QtGui, QtCore

class PainterWidget(QtGui.QWidget):
		def __init__(self, parent=None):
				QtGui.QWidget.__init__(self, parent)
				self.image = QtGui.QImage()
				self._width = 2
				self._min_size = (30, 30)

		def setImageData(self, image_data):
				self.image = image_data
				self.setMinimumSize(self.image.size())
				self.update()

		

		def paintEvent(self, event):
				painter = QtGui.QPainter(self)
				# painter.begin(self)
				painter.drawImage(0, 0, self.image)
				# painter.end()