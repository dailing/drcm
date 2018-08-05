import base64
import random
import time
import logging

import requests

from utils.auxs import encodeImageToDBdata
class uploadClient():
	def __init__(self, dbManager):
		self.dbManager = dbManager


	def post_test(file_names):
		datas = []
		for file_name in file_names:
			data = open(file_name, 'rb').read()
			# print('len', len(data))
			code = base64.b64encode(data)
			code = code.decode('utf-8')
			datas.append(code)
		obj = dict(data=datas)
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
		cv2ImageData = 255 - cv2ImageData
		res = encodeImageToDBdata(cv2ImageData)
		reply.emit(res)

		