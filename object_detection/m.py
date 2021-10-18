import cv2
import numpy as np


image = cv2.imread('test_1.png')
center = [image.shape[1]/2,image.shape[0]/2]
cv2.circle(image,(center[0],center[1]),8,(255,255,255),-1)


cv2.imshow('ff',image)

while True:
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
