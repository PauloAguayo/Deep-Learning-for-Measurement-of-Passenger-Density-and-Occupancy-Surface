import cv2
import numpy as np


w = 22.0*np.pi/(180)   # 22 grados para imagenes de lDH

image = cv2.imread('test_1.png')
center = np.array([int(image.shape[1]/2),int(image.shape[0]/2)]) #x,y
cv2.circle(image,(center[0],center[1]),8,(255,255,255),-1)

d_w = image.shape[0]*w/(np.pi/2.0)
new_center = int(center[1]+d_w)

cv2.circle(image,(center[0],new_center),8,(255,255,255),-1)

cv2.imshow('ff',image)

while True:
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
