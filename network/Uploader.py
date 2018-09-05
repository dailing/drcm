# -*- coding: utf-8 -*-
import base64
import random
import time
import logging
import requests
import json
import cv2
import numpy as np
from utils.auxs import encodeImageToDBdata, decodeDBImage


class uploadClient():
	def __init__(self):
		self.logger = logging.getLogger('root.uploadClient')

	def post_test(self, b64_encoded_png_image):
		obj = dict(data=[b64_encoded_png_image], eng=1)
		print ('request')
		resp = requests.post(url='http://106.14.140.203:6006/api/dr_grade_no_limit', json=obj)
		return resp.text

	# emit signal
	def remoteProcess(self, cv2ImageData, reply):
		try:
			print (cv2ImageData.shape)
			res = self.post_test(encodeImageToDBdata(cv2ImageData))
			res = json.loads(res)
		except Exception as e:
			self.logger.exception("remote process error")
			reply.emit(dict())
			return
		reply.emit(res)


	def transferImage(self, img, reply=None):
		try:
			print ('to transfer image')
			
			data = encodeImageToDBdata(img)
			obj={'image':data}
			resp = requests.post(url='http://111.231.144.111:7878/home/ubuntu/colortransfer', data=obj)
			res = decodeDBImage(resp.data()['image'])
			print ('get transfer image')
			if reply:
				reply.emit(res)
		except Exception as e:
			print(e)
			if reply:
				reply.emit(None)




if __name__ == '__main__':
	upc = uploadClient()
	upc.transferImage(cv2.imread('/home/d/workspace/drsys/classification_service/app/static/uploads/000623092880309.jpg'))
	pass