from time import gmtime, strftime, time
import datetime
import uuid

import cv2
from PyQt4 import QtGui


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

def getUUID():
	return uuid.uuid4()

if __name__ == '__main__':
	print(getTimeStamp())

