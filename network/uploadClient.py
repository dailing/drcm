import random
import time
import logging
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
				conn.execute("UPDATE PatientInfo SET upToServer=? WHERE uuid = ?", (1, item[0]))
			conn.commit()
			
		except Exception as e:
			logger.exception("upload error")
		finally:
			logger.debug("close conn")
			conn.close()
		dbManager.getAllRows(reply)
		#emit signal

		