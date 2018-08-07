import cv2
import numpy as np
class CircleMask():
	def __init__(self):
		mask = np.zeros((480, 640), dtype = np.uint8)
		cv2.circle(mask, (313, 226), 170, 255, -1)
		ret, mask = cv2.threshold(mask, 10, 255, cv2.THRESH_BINARY)
		self.mask = mask

	def getROI(self, img):
		return cv2.bitwise_and(img, img, mask=self.mask)