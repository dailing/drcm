import random
import time
import logging
from utils.auxs import encodeImageToDBdata
class uploadClient():
	def __init__(self, dbManager):
		self.dbManager = dbManager


	def getDataAndUpload(self, reply):
		
		#upload data:[(id, imageData)]
		
		try:
			logger = logging.getLogger('root.uploadClient')
			dbManager = self.dbManager.newInstance()
			# data : [[uuid, imageData]]
			data = dbManager.getAllLocalOnlyImageData()
			conn = dbManager.newConnection()
			logger.debug("process data {}".format(len(data)))
			for item in data:
				#to do : updata image data

				conn.execute("UPDATE PatientInfo SET upToServer=? WHERE uuid = ?", (1, item[0]))
			conn.commit()
			
		except Exception as e:
			logger.exception("upload error")
		finally:
			logger.debug("close conn")
			conn.close()
		dbManager.getAllRows(reply)
		#emit signal

	def remoteProcess(self, cv2ImageData, reply):
		cv2ImageData = 255 - cv2ImageData
		res = encodeImageToDBdata(cv2ImageData)
		reply.emit(res)

		