import cv2
import numpy as np

def get_most_colorful_image(imgs) :
	scores = []
	for img in imgs :
		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		scores.append(np.mean(hsv[:,:, 1]))
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
	res = get_most_colorful_image(getImages(range(37, 43)))
	print (res)
if __name__ == '__main__':
	main()