'''
****************
Contour Features Unit Tests
****************
Tests used for the Contour Features module
'''
from count_objects import im_proc
from count_objects import contour_features as cf
import unittest
import cv2
import numpy as np


class TestCountourFeaturesFunctions(unittest.TestCase):

	def setUp(self):
		imgPath = 'img/lightboximage4.bmp'
		self.img = cv2.imread(sys.argv[1],cv2.CV_LOAD_IMAGE_COLOR)
		self.windowName = "Named_Window"
	

if __name__ == '__main__':
    unittest.main()

