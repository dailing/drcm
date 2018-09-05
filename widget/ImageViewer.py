from PyQt4 import QtGui, QtCore
import cv2
from utils.icons import get_icon
from model import patient
from widget.PainterWidget import PainterWidget

from utils.logFormatter import setupLogger
from utils.auxs import cv2ImagaeToQtImage

logger = setupLogger('new_record_list')


class ImageViewer(QtGui.QWidget):
	back_clicked = QtCore.pyqtSignal(name='back_clicked()')

	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.resize(800, 480)
		self.current_index = 0

		self.image_widget = PainterWidget()
		self.images = None
		self.next_icon = get_icon('next')
		self.prev_icon = get_icon('previous')
		self.icons_layout = QtGui.QHBoxLayout()
		self.icons_layout.addWidget(self.prev_icon)
		self.icons_layout.addWidget(self.image_widget)
		self.icons_layout.addWidget(self.next_icon)
		self.icons_layout.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
		# self.layout = QtGui.QVBoxLayout(self)
		# self.layout.addWidget(self.image_widget)
		# self.layout.addLayout(self.icons_layout)
		self.setLayout(self.icons_layout)
		self.next_icon.mousePressEvent = self.next_image
		self.prev_icon.mousePressEvent = self.prev_image
		self.ps = patient.Patients()

	@property
	def custom_right_header(self):
		right_header = get_icon('save_record')
		right_header.mouseReleaseEvent = self.save_on_click_handler
		return right_header

	@property
	def custom_left_header(self):
		logger.debug('custom_left_header')
		left_header = get_icon('back')
		logger.debug('get icon for custom_left_header')

		left_header.mouseReleaseEvent = lambda event: self.back_clicked.emit()
		return left_header

	def set_pic_list(self, images):
		self.images = images
		if len(self.images) <= 0:
			return
		self.show_img()

	def set_pid(self, pid):
		logger.debug('set pid: {}'.format(pid))
		assert type(pid) is str
		self.set_pic_list(self.ps[pid].get_images())

	def show_img(self, index=0):
		logger.debug('show {}'.format(index))
		img = self.images[index].get_img()
		img = cv2.resize(img,(480,360))
		self.image_widget.setImageData(
			cv2ImagaeToQtImage(img))

	def next_image(self, event=None):
		self.current_index = (self.current_index+1) % len(self.images)
		logger.debug(self.current_index)
		self.show_img(self.current_index)

	def prev_image(self, event=None):
		self.current_index = (self.current_index-1) % len(self.images)
		self.show_img(self.current_index)


import sys

def main():
	# call this main function to add default images
	# patient.main()
	nn = patient.Patients()
	pp = nn['123']
	app = QtGui.QApplication(sys.argv)
	ex = ImageViewer(None)
	xx = pp.get_images()
	ex.set_pic_list(xx)
	ex.show()
	app.exec_()
	return xx


if __name__ == '__main__':
	xx = main()