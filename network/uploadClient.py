import base64
import random
import time
import logging

import requests
import json

from utils.auxs import encodeImageToDBdata

class uploadClient():
	def __init__(self, dbManager):
		self.dbManager = dbManager


	def post_test(self, b64_encoded_png_image):
		obj = dict(data=[b64_encoded_png_image])
		resp = requests.post(url='http://106.14.140.203:6006/api/dr_grade_no_limit', json=obj)
		return resp.text

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
		res = self.post_test(encodeImageToDBdata(cv2ImageData))
		res = json.loads(res)
		reply.emit(res)

		