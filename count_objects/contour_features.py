'''
****************
Contour Features
****************
This module contains the Contour Class used to calculate the statistics of objects found using cv2.findContours()
'''
import cv2
import numpy as np
import collections
import math
import im_proc

class Contour:
        '''Contour class used to create and store statists about the obejcts found in an image using cv2.findContours function.
        The attributes can be calcuted on instantiation of the contour object or they can be called and populated as the GET function
        for that attribute is called. This is done by means of an optional boolean parameter initValues. This means each GET function
        first determines if the value has been changed from default value of None before doing any calculation.

        Attributes:
                img (image):
                        The image that the contour was found in
                cnt (openCV moment):
                        The detected contour points from the original image
                size (int):
                        The number of different points in the contour boundry that defines the contour itself
                area (double):
                        Total area of the contour in pixels
                centroid (array):
                        X and y value of the center of the contour. Calculated as the average position of all of the pixels contained inside the contour
		boundingBox (array):
                        The four x,y values of the corners of the bounding box around the contour that has sides perpendicular to the image x,y axis.
                minBoundingBox_Points (array):
                        The four x,y values of the corners of the minimal bounding box around the contour.
                boundingEllipse (array):
                        The points that make up the best fitting bounding ecplise of the contour.
                majorAxis (double):
                        The length of the major axis of the bounding ellipse in pixels
                minorAxis (double):
                        The lenth of the minor axis of the bounding ellipse in pixels
                height: (double):
                        The length (longest side) of the bounding box which can be considered a proxy for length
                width: (double):
                        The width (longest side) of the bounding box which can be considered a proxy for width
                ellipse (array):
                        An array of hte points in the smallest bounding ellipse
                ellipse_MinorAxisLength: (double):
                        The length of the minor axis of the bounding ellipse in pixels            
                ellipse_MajorAxisLength: (double):
                        The length of the major axis of the bounding ellipse in pixels
                contourLengthToWidth: (double):
                        The ratio of the contours length to width (calculated from the minBoundingBoxDims)               
                allPixelPoints: (array):
                        Two arrays one with the x and one with the y coordinates of every pixel inside the contour.                    
                allPixelPointColours: (array):
                        Two arrays one with the an array containing the x,y coordinates and the other an array containing the BGR values [Coordinates, Colours]
                totalReflectance: (double)
                        Total Reflectance or the colour intensity of the contour (total colour intensity). The sum of pixel colour values in the red green and blue channel averaged over the whole contour.
        '''
        def __init__(self,originalImg,cnt,binaryImg = None,initValues=False):
                '''The constructor for a contour object

                Args:
                    img (image): The image that the contour moments were detected from
                    cnt (moment): An openCV contour moment structure that is returned using cv2.findContours()
                    initValues (boolean): True == calculate the attributes upon initialisation. False == set all non supplied attribues to None as default.

                Returns:
                    None

                '''
                self.originalImg = originalImg
                self.cnt = cnt
                self.size = len(cnt)
                if (binaryImg is None):
                        self.binaryImg = im_proc.prepareImage(self.originalImg)
                        im_proc.show_image (self.binaryImg)
                else:
                        self.binaryImg = binaryImg
                
                self.initValuesToNone()
                if (initValues):
                        self.getArea()
                        self.getCentroid()
                        self.getBoundingBox()
                        self.getMinBoundingBox()
                        self.getBoundingEllipse()
                        self.getMajorAxis()
                        self.getMinorAxis()
                        self.getMinBoundingBoxDimensions()
                        self.getContourLength()
                        self.getCircularity()
                        self.getContourLengthToWidth()
                        self.getPixelPoints()
                        self.getPixelPointColours()
                        self.getTotalReflectance()
               
                       
                        
        def initValuesToNone(self):
                self.area = None
                self.centroid = None
                self.circularity = None
                self.boundingBox_Points = None
                self.minBoundingBox_Points = None
                self.boundingEllipse = None
                self.boundingAxis = None
                self.boundingElliplse = None
                self.majorAxis = None
                self.minorAxis = None
                self.height = None
                self.width = None
                self.contourLength = None
                self.ellipse = None
                self.ellipse_MinorAxisLength = None
                self.ellipse_MajorAxisLength = None
                self.contourLengthToWidth = None
                self.allPixelPoints = None
                self.allPixelPointColours = None
                self.totalReflectance = None
        
        #get contour area
        def getArea(self):
                '''Finds the area of the contour in pixels

                Args:
                     none

                Returns:
                     The area in pixels
                '''
                if (self.area is None):
                        self.area = cv2.contourArea(self.cnt)
                return self.area
            

        #get average position (centroid) of the contour relative to top left 0px,0px
        def getCentroid(self):
                '''

                Args:
                         

                Returns:
                      
                '''
                if (self.centroid is None):
                        self.moments = cv2.moments(self.cnt)
                        if self.moments['m00'] != 0.0:       
                                self.cx = self.moments['m10']/self.moments['m00']
                                self.cy = self.moments['m01']/self.moments['m00']
                                self.centroid = (int(round(self.cx,0)),int(round(self.cy)))                                         
                        else:
                                return "Region has zero area"
                return self.centroid 
	def getBoundingBox(self):
                '''Get a bounding box that has sides that are perperdicular to the image x and y axis.
		Args:
                	none
		Returns:
			An array containing the x,y values of the four corners of the bounding box
		'''
                if (self.boundingBox_Points is None):
                        bx,by,bw,bh = cv2.boundingRect(self.cnt)
                        self.boundingBox_points = bx,by,bw,bh
                return self.boundingBox_Points

        def getMinBoundingBox(self):
                '''Get the minimal bounding box for the countour
                Args:
                   None
                   
                Returns:
                   An array containing the x,y values of the four corners of the bounding box
                '''
                if (self.minBoundingBox_Points is None):                        
                        rect = cv2.minAreaRect(self.cnt)              
                        points = cv2.cv.BoxPoints(rect)
                        points = np.int0(np.around(points))
                        self.minBoundingBox_Points = points
                        self.minBoundingBox_top = points[0]
                        self.minBoundingBox_right = points[1]
                        self.minBoundingBox_bottom = points[2]
                        self.minBoundingBox_right = points[3]                
                return self.minBoundingBox_Points

        def getBoundingEllipse(self):
                '''Get the smallest bounding ellipse for the contour

                Args:
                    None

                Returns:
                    An array of the points in the bounding ellipse
                '''
                if (self.ellipse is None):
                        self.ellipse = cv2.fitEllipse(self.cnt)
                        (self.ellipose_center,self.ellipse_axes,self.ellipse_orientation) = self.ellipse
                return self.ellipse
        
        def getMajorAxis(self):
                '''Get the major axis of the bounding ellipse of the contour

                Args:
                    None
                
                Returns:
                    A double representing the length in pixels of the major axis
                '''
                if (self.ellipse_MajorAxisLength is None):
                        if (self.ellipse is None):
                                self.getBoundingEllipse()                
                self.ellipse_MajorAxisLength = max(self.ellipse_axes)
                return self.ellipse_MajorAxisLength
                
        def getMinorAxis(self):
                '''Get the minor axis of the bounding ellipse of the contour

                Args:
                    None
                
                Returns:
                    A double representing the length in pixels of the minor axis
                '''
                if (self.ellipse_MinorAxisLength is None):
                        if (self.ellipse is None):
                                self.getBoundingEllipse()
                
                        self.ellipse_MinorAxisLength = min(self.ellipse_axes)  
                return self.ellipse_MinorAxisLength

        def getMinBoundingBoxDimensions(self):
                '''Find the length and width of the bounding box of the contour. This can be used as  proxy for the length and width of the contour itself

                Args:
                    None 

                Returns:
                    An array containing the width and the height in that order [width,height]
                '''
                if (self.width is None or self.height is None):
                        if (self.minBoundingBox_Points is None):
                                self.getMinBoundingBox()

                        #for dimention 1 using the top corner and the right corner
               
                        a = (self.minBoundingBox_right[0] - self.minBoundingBox_top[0])            
                        b = (self.minBoundingBox_right[1] - self.minBoundingBox_top[1])
                        dimension1 = math.sqrt(a**2 + b**2)

                        #for dimension 2 using the bottom corner and the left corner

                        c = (self.minBoundingBox_right[0] - self.minBoundingBox_bottom[0])
                        d = (self.minBoundingBox_right[1] - self.minBoundingBox_bottom[1])
                    
                                    
                        dimension2 = math.sqrt(c**2 + d**2)

                        self.width = round(min(dimension1,dimension2),2)
                        self.height = round(max(dimension1, dimension2),2)
                return [self.width,self.height]
        def getContourLength(self):
                '''Returns the length of the perimiter of the contour in pixels

                Args:
                    None

                Returns:
                    The length of the perimeter of the contour in pixel
                '''
                if (self.contourLength is None):
                        self.contourLength = cv2.arcLength(self.cnt,True)
                return self.contourLength
        
        def getCircularity(self):
                '''Calculate the circularity of the the contour using the Haywood Circularity Factor formula. The function returns the inverse of the result of the Haywoord formula

                Args:
                    None

                Returns:
                    A double that represents the circularity of the contour with a value between 0 and 1 where a value of 1 represents a perfect circle.
                '''
               
                if(self.circularity is None):
                        if (self.area is None):
                                self.getArea()
                        if (self.contourLength is None):
                                self.getContourLength()
                        self.circularity = 1/((self.contourLength/(2*math.sqrt(math.pi*self.area))))
                return self.circularity

        def getContourLengthToWidth(self):
                '''Returns the ratio of  to width (hieght/width)

                Args:
                    None

                Returns:
                    The ratio of length to width as a double
                '''
                
                if (self.contourLengthToWidth == None):
                        if (self.width == None or self.height == None):
                                self.getBoundingBoxDimensions()
                        self.contourLengthToWidth = self.height/self.width
                return self.contourLengthToWidth

        def getPixelPoints(self):
                '''Returns an array of all the pixel points in the contour

                Args:
                    img : the original image that is used as reference point for the pixel points.

                Returns:
                    An array of all the pixel points in the contour
                '''
                if(self.allPixelPoints is None):
                        drawing = np.zeros(self.binaryImg.shape,np.uint8) #create a zero'd drawing with same dimensions as given image
                        cv2.drawContours(drawing,[self.cnt],0,(255,255,255),-1)              
                        pixelPoints = np.nonzero(drawing)
                        self.allPixelPoints = pixelPoints
		return self.allPixelPoints	
	def getPixelPointColours(self):
                '''Returns an tuple of cordinates and colour arrays

                Args:
                    img : the original image that is used as reference point for the pixel points and the colours.

                Returns:
                    An array of all the pixel points in the contour
                '''
                #destRGB = cv2.cvtColor(colourImg,cv2.COLOR_BGR2RGB) #convert openCV BGR colour to RGB
                if (self.allPixelPointColours is None):
                        if (self.allPixelPoints is None):
                                pixelpoints = c.getPixelPoints(self.binaryImg)
                        colourList = list()
                        rows = self.allPixelPoints[0]
                        cols = self.allPixelPoints[1]
                        for x in range(0, len(rows)):
                                colourList.append([[rows[x],cols[x]],self.originalImg[rows[x],cols[x]]])
                        self.allPixelPointColours = colourList
                return  self.allPixelPointColours

        def getTotalReflectance(self):
                '''Returns an tuple of cordinates and colour arrays

                Args:
                    None

                Returns:
                    An array of all the pixel points in the contour
                '''
                totalReflectance = 0 #to keep track of the total of all colour channels added together
                totalColourValueCount = 0 #keep track of how many colour channels we have added together
                if (self.totalReflectance is None):
                        if (self.allPixelPointColours is None):
                                self.getPixelPointColours(self.binaryImage)
        
                        for colours in self.allPixelPointColours:
                                for channel in colours[1]:
                                        totalColourValueCount += 1
                                        totalReflectance += channel
                                        
                        #the total reflectance devided by number of channels and then by three to get for each pixel (three channels per pixel)
                        self.totalReflectance = totalReflectance/(totalColourValueCount/3)
                return self.totalReflectance
                
                        
