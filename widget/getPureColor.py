import cv2
import numpy as np

bg = np.zeros((48, 48, 3), dtype = np.uint8)
bg[:,:, 0] = 255
cv2.imwrite('background.png', bg)