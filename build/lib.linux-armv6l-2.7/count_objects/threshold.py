import cv2
import numpy as np
img2 = cv2.imread('ligthboximage2.bmp')

ret,thresh = cv2.threshold(img2, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

print ret
