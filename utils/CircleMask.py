import cv2
import numpy as np

center = (313, 226)
radius = 170
class CircleMask():
	def __init__(self):
		mask = np.zeros((480, 640), dtype = np.uint8)
		cv2.circle(mask, center, radius, 255, -1)
		ret, mask = cv2.threshold(mask, 10, 255, cv2.THRESH_BINARY)
		self.mask = mask

	def getROI(self, img):
		return cv2.bitwise_and(img, img, mask=self.mask)

class RectangleMask():
	def __init__(self):
		mask = np.zeros((480, 640), dtype = np.uint8)
		sx = center[0] - radius
		sy = center[1] - radius
		ex = center[0] + radius + 1
		ey = center[1] + radius + 1
		mask[sx: ex, sy: ey] = 255
		ret, mask = cv2.threshold(mask, 10, 255, cv2.THRESH_BINARY)
		self.mask = mask

	def getROI(self, img):
		return cv2.bitwise_and(img, img, mask=self.mask)