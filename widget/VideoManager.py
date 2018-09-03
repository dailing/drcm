import logging
import os

from PyQt4 import QtGui, QtCore
import cv2
from utils.auxs import *
from utils.CircleMask import CircleMask, RectangleMask
from sql.DataBaseManager import DataBaseManager

from widget.DiagnosisDialog import DiagnosisDialog
from widget.PatientDataFormat import ImageInfo

DISPLAY_SIZE = (640, 480)

class VideoReader():
	def __init__(self):
		pass
		try:
			V_DES = os.environ['VIDEO_DEFAULT']
			self.reader = cv2.VideoCapture(int(V_DES))
		except Exception as e:
			print (e)
			self.reader = cv2.VideoCapture(0)
		logger = logging.getLogger('root.VideoReader')
		try:
			self.reader.set(3,640);
			self.reader.set(4,480);
			# self.reader.set(38, 4)
		except Exception as e:
			print (str(e))
			logger.exception(e)
		self.getParameters()
		logger.debug('finish open video')
		logger.info('buffer size for camera : {}'.format(self.reader.get(38)))

	def getParameters(self):
		self.reader.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
		self.reader.set(cv2.CAP_PROP_EXPOSURE, 0.1)
		self.reader.set(cv2.CAP_PROP_HUE, 0.5)

		print ('CAP_PROP_FPS', self.reader.get(cv2.CAP_PROP_FPS))
		print ('CAP_PROP_MODE', self.reader.get(cv2.CAP_PROP_MODE))
		print ('CAP_PROP_BRIGHTNESS', self.reader.get(cv2.CAP_PROP_BRIGHTNESS))
		print ('CAP_PROP_CONTRAST', self.reader.get(cv2.CAP_PROP_CONTRAST))
		print ('CAP_PROP_SATURATION', self.reader.get(cv2.CAP_PROP_SATURATION))
		print ('CAP_PROP_EXPOSURE', self.reader.get(cv2.CAP_PROP_EXPOSURE))
		print ('CAP_PROP_BUFFERSIZE', self.reader.get(cv2.CAP_PROP_BUFFERSIZE))
		print ('CAP_PROP_GAIN', self.reader.get(cv2.CAP_PROP_GAIN))
		print ('CAP_PROP_HUE', self.reader.get(cv2.CAP_PROP_HUE))
		print ('CAP_PROP_ISO_SPEED', self.reader.get(cv2.CAP_PROP_ISO_SPEED))

	def getDevice(self):
		return self.reader



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

	def __init__(self, canvas):
		QtCore.QObject.__init__(self)

		self.logger = logging.getLogger('root.video_manager')
		self.patientInfo = None

		self.canvas = canvas
		self.mask = CircleMask()
		self.timer = QtCore.QTimer()
		self.camera = VideoReader()
		self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.updateFrame)
		self.dbInsertSignal.connect(self.saveImageCallBack)
		self.dbManager = DataBaseManager('patientRecord.db')
		self.inProcessing = False

	def fillRecord(self, patient):
		self.patientInfo = patient

	def set_HUE(self, value):
		self.camera.getDevice().set(cv2.CAP_PROP_HUE, value)

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

	def pauseCanvas(self):
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
				self.logger.exception('snap error')
			finally :
				self.inProcessing = False
		else :
			self.startCanvas()

	#?
	def process(self):
		pass

	def saveImage(self, imageData):
		if self.patientInfo is None:
			cv2.imwrite('default.png', imageData)
			return
		print ('save to database')
		imageInfo = ImageInfo.fromPatientInfo(self.patientInfo)
		imageInfo.setTime(getTimeStamp())
		imageInfo.setUUID(getUUID())
		imageInfo.setData(
			encodeImageToDBdata(imageData)
			)
		print ('start to save')
		self.dbManager.insertRecord(imageInfo, self.dbInsertSignal)

	def saveImageCallBack(self, isSucceed):
		print(isSucceed)
		if isSucceed:
			pass
		else :
			QtGui.QMessageBox.warning(
				QtGui.QWidget(), "Error", "save data failed!")
		