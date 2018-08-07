import cv2
import numpy as np


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
	scores = [colorfulnessByHSV(img) for img in imgs]
	print(scores)
	return np.argmax(scores)
def drawCircles(circles, cimg):
	for i in circles[0,:]:
		cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
		# cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
def scoreIt(dataIdx):
	scores = []
	for idx in dataIdx:
		img = cv2.imread("{}.png".format(idx))
		grayimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		# circles = cv2.HoughCircles(grayimg,cv2.HOUGH_GRADIENT,1,20, param1=185,param2=70,minRadius=0,maxRadius=0)
		# print(circles[0][2:])
		# drawCircles(circles, img)
		img = cv2.Canny(img,100,200)
		cv2.imwrite('circle.png', img)
		res = np.sum(np.var(img))
		scores.append(res)
		print (idx, res)
	print(np.argmin(scores))

def getImages(imgIdxs):
	return [cv2.imread('{}.png'.format(i)) for i in imgIdxs]

def main():
	get_most_colorful_image(getImages(range(33, 49)))
if __name__ == '__main__':
	main()