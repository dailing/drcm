from time import gmtime, strftime, time
import datetime
import uuid
import logging
import pickle
from hashlib import md5
import base64

import numpy as np

import cv2
from PyQt4 import QtGui

def setButtonIcon(iconFile, button):
	icon = QtGui.QIcon(iconFile)
	button.setIcon(icon)


def image_colorfulness(image):
	# split the image into its respective RGB components
	(B, G, R) = cv2.split(image.astype("float"))

	# compute rg = R - G
	rg = np.absolute(R - G)

	# compute yb = 0.5 * (R + G) - B
	yb = np.absolute(0.5 * (R + G) - B)

	# compute the mean and standard deviation of both `rg` and `yb`
	(rbMean, rbStd) = (np.mean(rg), np.std(rg))
	(ybMean, ybStd) = (np.mean(yb), np.std(yb))

	# combine the mean and standard deviations
	stdRoot = np.sqrt((rbStd ** 2) + (ybStd ** 2))
	meanRoot = np.sqrt((rbMean ** 2) + (ybMean ** 2))

	# derive the "colorfulness" metric and return it
	return stdRoot + (0.3 * meanRoot)

def colorfulnessByHSV(img):
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	return np.mean(hsv[:,:, 1])

def get_most_colorful_image(imgs) :
	scores = [image_colorfulness(img) for img in imgs]
	print (scores)
	return np.argmax(scores)

def saveObj(fname, obj):
	fname = 'state/' + fname
	with open(fname, 'wb') as output:
		pickle.dump(obj, output)

def decodeDBImage(dbData):
	bytesImage =base64.b64decode(dbData)
	nparr = np.frombuffer(bytesImage, np.uint8)
	image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
	return image

def encodeImageToDBdata(imageData):
	res = cv2.imencode('.png', imageData)[-1]
	pngBytes = base64.b64encode(res)
	return pngBytes

def loadObj(fname):
	fname = 'state/' + fname
	try:
		with open(fname, 'rb') as fin:
			obj = pickle.load(fin)
	except Exception as e:
		print(e)
		obj = None
	finally:
		return obj

def cv2ImagaeToQtImage(data):
	if data is None:
		return data
	data = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
	height, width, byteValue = data.shape
	byteValue = byteValue * width
	return QtGui.QImage(data, width, height, byteValue, QtGui.QImage.Format_RGB888)

def getTimeStamp():
	return time()

def getDateTimeFromTS(ts):
	return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def getMDTimeFromTS(ts):
	return datetime.datetime.fromtimestamp(ts).strftime('%m-%d %H:%M:%S')

def getUUID():
	return uuid.uuid4()

def getContrast(imageData):
	gray = cv2.cvtColor(imageData, cv2.COLOR_BGR2GRAY)
	lapabs = np.abs(cv2.Laplacian(gray, cv2.CV_64F))
	return lapabs

if __name__ == '__main__':
	pass
	code = encodeImageToDBdata(cv2.imread('../logo.png'))
	ori = decodeDBImage(code)
	cv2.imwrite('decoded.png', ori)
	# print(getTimeStamp())
	# uuidStr = str(getUUID())
	# print(uuidStr)
	# print(len(uuidStr))
	# saveObj('str.pkl','dump')
	# print(loadObj('str.pkl'))
	# print(loadObj('err.pkl'))
	# print(
	# 	'name' if uuidStr is None else uuidStr
	# 	)
	
	
