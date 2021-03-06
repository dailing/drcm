from time import gmtime, strftime, time
import datetime
import uuid

import pickle

import numpy as np
import logging
import cv2
from PyQt4 import QtGui


def saveObj(fname, obj):
	fname = 'state/' + fname
	with open(fname, 'wb') as output:
		pickle.dump(obj, output)

def encodeImageToDBdata(imageData):
	res = cv2.imencode('.png', imageData)[-1]
	logging.getLogger('root.utils')

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
	# data = md5(encodeImageToDBdata(cv2.imread('logo.png'))).hexdigest()
	# print(type(data))
	
