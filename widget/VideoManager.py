import logging

from PyQt4 import QtGui, QtCore
import cv2
from utils.auxs import *
from utils.CircleMask import CircleMask
from sql.DataBaseManager import DataBaseManager

from widget.DiagnosisDialog import DiagnosisDialog


DISPLAY_SIZE = (640, 480)

class VideoReader():
	def __init__(self):
		pass
		self.reader = cv2.VideoCapture(0)
		logger = logging.getLogger('root.VideoReader')
		try:
			self.reader.set(3,640);
			self.reader.set(4,480);
			# self.reader.set(38, 4)
		except Exception as e:
			print (str(e))
			logger.exception(e)
		logger.debug('finish open video')
		logger.info('buffer size for camera : {}'.format(self.reader.get(38)))

	def read(self):
		return self.reader.read()

def focusLedOn():
	try:
		flashLed.off()
	except Exception as e:
		pass
	try:
		infraredLed.on()
	except Exception as e:
		pass

def exposureOn():
	try:
		infraredLed.off()
	except Exception as e:
		pass
	try:
		flashLed.on()
	except Exception as e:
		pass

from sql.RunnableFunc import RunnableFunc
from sql.PoolWrapper import PoolWrapper
from network.uploadClient import uploadClient
class ImageDiagnosis(QtCore.QObject):
	remoteProcessSignal = QtCore.pyqtSignal(dict)
	def __init__(self):
		QtCore.QObject.__init__(self)
		self.pw = PoolWrapper()
		self.logger = logging.getLogger('root.diag')
		self.remoteProcessSignal.connect(self.processImageCallBack)

	def process(self, img):
		self.pw.start(
			RunnableFunc(
				uploadClient(self.dbManager).remoteProcess,
				img,
				self.remoteProcessSignal
				)
			)

	def processImageCallBack(self, diagnosis):
		self.logger.debug('diagnosis display')
		DiagnosisDialog.newInstance(diagnosis)
		self.logger.debug ('end process')
		

class VideoManager(QtCore.QObject):
	FRAME_PER_SECOND = 24
	UPDATE_FREQ = 1000.0 / FRAME_PER_SECOND

	dbInsertSignal = QtCore.pyqtSignal(bool)

	def __init__(self, canvas, patientInfo):
		QtCore.QObject.__init__(self)
		self.patientInfo = patientInfo

		self.canvas = canvas
		self.mask = CircleMask()
		self.timer = QtCore.QTimer()
		self.camera = VideoReader()
		self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.updateFrame)
		self.dbInsertSignal.connect(self.saveImageCallBack)
		self.dbManager = DataBaseManager('patientRecord.db')
		self.inProcessing = False

	def updateFrame(self):
		ret, frame = self.camera.read()
		# frame = self.mask.getROI(frame)
		frame_to_display = cv2.resize(frame, DISPLAY_SIZE)
		# assert frame_to_display.shape == frame.shape
		# if saveTodisk:
		# 	self.saveImage(frame)
		mQImage = cv2ImagaeToQtImage(frame_to_display)
		self.canvas.setImageData(mQImage)


	def startCanvas(self):
		self.timer.start(VideoManager.UPDATE_FREQ)

	def puaseCanvas(self):
		self.timer.stop()

	def flashFrame(self, num = 3):
		exposureOn()
		data = [self.mask.getROI(self.camera.read()[1])]
		focusLedOn()
		newData = [self.camera.read()[1] for i in range(5)]
		data.extend(newData)
		# best_img = get_most_colorful_image(data)
		best_img = data[4]
		self.preImageData = best_img
		
		# for img in data:
		# 	self.saveImage(img)
		self.saveImage(best_img)

		frame_to_display = cv2.resize(best_img, DISPLAY_SIZE)
		mQImage = cv2ImagaeToQtImage(frame_to_display)
		self.canvas.setImageData(mQImage)
		#end

	def snap(self):
		if self.inProcessing:
			return
		if self.timer.isActive():
			self.inProcessing = True
			
			try:
				self.puaseCanvas()
				self.flashFrame()
			except Exception as e:
				print(e)
			finally :
				self.inProcessing = False
		else :
			self.startCanvas()

	#?
	def process(self):
		pass

	def  saveImage(self, imageData):
		if self.patientInfo is None:
			return
		self.patientInfo.setTime(getTimeStamp())
		self.patientInfo.setUUID(getUUID())
		self.patientInfo.setData(
			encodeImageToDBdata(imageData)
			)
		self.dbManager.insertRecord(self.patientInfo, self.dbInsertSignal)

	def saveImageCallBack(self, isSucceed):
		print(isSucceed)
		if isSucceed:
			pass
		else :
			QtGui.QMessageBox.warning(
				QtGui.QWidget(), "Error", "save data failed!")
		