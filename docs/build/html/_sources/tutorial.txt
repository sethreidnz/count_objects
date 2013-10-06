========================================
Object Count Tutorial
========================================

This is a short tutorial with code examples to show how to make a very simple application
to count the seeds in an image using this toolkit.

The process of counting objects in an image can be broken down into to sub-processes. The 
first is preparing the image and the second is identifying the objects in the prepared image.
This toolkit as substantially simplified this process by making these two processes into one
simple function which takes a single image parameter and two optional parameters, a threshold value
and the initValues flag. 

Note: This is not to say the image preparation functions are not available to be used
separately from these two functions but this would only be required if certain problems exist
in the image that make further image processing required. In an image that has high a contrast 
in light intensity between the foreground (objects of interest) and the background the function 
im_proc.prepareImage() will be satisfactory in creating a binary image. This function is used
in the im_proc.getContourListFrom() function which takes care of the entire process.

To create an application using this toolkit one has to simply get an image objects using openCV
cv2.imread() function then pass that image to the function im_proc.getContourListFrom() (using the initValue
flag if you wish all the statistics to be calculated on instantiation). This will return a dictionary
of contours with the key being the contours ID attribute. The following is a simple command line application
that takes an image path as an argument and then creates a contour list from it::

		import cv2
		import sys
		import numpy as np
		from count_objects import im_proc
		from count_objects import contour_features as cf
		   
		if len(sys.argv)!=2:                  ## Check for error in usage syntax
			print "Usage : python countSeeds.py <image_file>"

		else:#continue with the program
			## Read image file in colour
			img = cv2.imread(sys.argv[1],cv2.CV_LOAD_IMAGE_COLOR)
			cList = im_proc.getContourListFrom(img, initValues=False)

This list can then be passed to im_proc.drawContoursFromList() function and this will draw the contours onto
a copy of the original image in a red outline. This function has a flag 'numberContours' that defaults to true 
and controls if the function numbers the contours in the image. This can then be shown to the end user::

	output = im_proc.drawContoursFromList(cList)

	### show original
	im_proc.show_image('input',img)
	cv2.cv.MoveWindow('input',0,0)

	#Show final image
	im_proc.show_image('output',output)
	cv2.cv.MoveWindow('output',500,0)

	## Wait for keystroke to allow user to see image displays
	cv2.waitKey(0)
	cv2.destroyAllWindows()

The list passed back by to im_proc.drawContoursFromList() has contour objects in it. These have various get functions
that will give you statistics about the contour. These are listed in the contour class documentation.

The full code can be found bellow::

	import cv2
	import sys
	import numpy as np
	from count_objects import im_proc
	from count_objects import contour_features as cf
	   
	if len(sys.argv)!=2:                  ## Check for error in usage syntax
		print "Usage : python countSeeds.py <image_file>"

	else:#continue with the program
		## Read image file in colour
		img = cv2.imread(sys.argv[1],cv2.CV_LOAD_IMAGE_COLOR)
		cList = im_proc.getContourListFrom(img, initValues=False)
		output = im_proc.drawContoursFromList(cList)

		### show original
		im_proc.show_image('input',img)
		cv2.cv.MoveWindow('input',0,0)

		#Show final image
		im_proc.show_image('output',output)
		cv2.cv.MoveWindow('output',500,0)

		## Wait for keystroke to allow user to see image displays
		cv2.waitKey(0)
		cv2.destroyAllWindows()




