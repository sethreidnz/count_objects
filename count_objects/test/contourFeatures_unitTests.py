'''
****************
Contour Features Unit Tests
****************
Tests used for the Contour Features module
'''
from count_objects import im_proc
import unittest

class TestCountourFeaturesFunctions(unittest.TestCase):

	def setUp(self):
		self.jpgPath = 'img/image5.jpg'
		self.bmpPath = 'img/lightboximage4.bmp'
		self.windowName = "Named_Window"
	

if __name__ == '__main__':
    unittest.main()

