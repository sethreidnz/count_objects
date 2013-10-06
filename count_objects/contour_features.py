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
        The attributes can be calcuted on instantiation of the contour object or they can be called and populated as the 'get' function
        for that attribute is called. This is done by means of an optional boolean parameter initValues. This means each 'get' function
        first determines if the value has been changed from default value of None before doing any calculation. These values should
        be treated as read only and accessed via their respective 'get' function.

        Attributes:
                img (image):
                        The image that the contour was found in

                cnt (OpenCV contour-return-data):
                        The detected contour points from the original image

                size (int):
                        The number of different points in the contour boundry that defines the contour itself

                originalImg (cv2-image-object[numpy-aray]):
                        The original image the contour was found in

                binaryImg (cv2-image-object[numpy-aray]):
                        The prepared binarized version of the image used for the actual contour detection

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

                convexHull (OpenCV contour-return-data):
                        The convex hull of the contour

                convexHullArea (float):
                        The area of the convex hull of the contour (in px)

                convexAreaDivCntArea (float):
                        The area of the convex hull divided by the area of the contour itself (in px)

                allPixelPoints: (array):
                        Two arrays one with the x and one with the y coordinates of every pixel inside the contour.

                totalPixelsContained(int):
                        The total number of pixels contained within the contour

                allPixelPointColours: (array):
                        Two arrays one with the an array containing the x,y coordinates and the other an array containing the BGR values [Coordinates, Colours]

                totalColourIntensity (int):
                        The total count of all colour channels across all pixels in the contour

                totalReflectance: (double)
                        Total Reflectance or the colour intensity of the contour (total colour intensity). The sum of pixel colour values in the red green and blue channel averaged over the whole contour.

                totalBlueValues (int):
                        The total count of blue values across all pixels in the contour
                        
                totalGreenValues(int):
                        The total count of green values across all pixels in the contour
                        
                totalRedValues(int):
                        The total count of red values across all pixels in the contour
                        
                redToGreenRatio(float):
                        The ratio of red to blue channel values accross the whole contour
                        
                allColourDensities (Array of floats):
                        Three values that represent the total value of each colour channel devided by the total intensity. In openCV native channel order of BGR. IE redTotal/totalColourIntensity.
        '''
        def __init__(self,originalImg,cnt,ID,binaryImg = None,initValues=False):
                '''The constructor for a contour object

                Args:
                    img (image): The image that the contour moments were detected from
                    cnt (moment): An openCV contour moment structure that is returned using cv2.findContours()
                    ID (integer): A unique identifier for this contour within the contect of the image in which it is found
                    binaryImg (cv2-image-object[numpy-aray])
                    initValues (boolean): True == calculate the attributes upon initialisation. False == set all non supplied attribues to None as default.

                Returns:
                    None

                '''
                self.originalImg = originalImg
                self.cnt = cnt #the actual contour data returned by cv2.findContours()
                self.size = len(cnt) #perimiter of the contour
                self.ID = ID #unique identifier within the image the contour is found
                
                if (binaryImg is None):
                        self.binaryImg = im_proc.prepareImage(self.originalImg)
                        im_proc.show_image (self.binaryImg)
                else:
                        self.binaryImg = binaryImg
                
                
                self.initValuesToNone()
                if (initValues): #if initValues flag is true calculate all attributes
                        self.getArea()
                        self.getCentroid()
                        self.getBoundingBox()
                        self.getMinBoundingBox()
                        self.getBoundingEllipse()
                        self.getMajorAxis()
                        self.getMinorAxis()
                        self.getMinBoundingBoxDimensions()
                        self.getPerimeter()
                        self.getHeywoodCircularity()
                        self.getContourLengthToWidth()
                        self.getConvexHull()
                        self.getConvexHullArea()
                        self.getConvexAreaDivCntArea()
                        self.getPixelPoints()
                        self.getPixelPointColours()
                        self.getTotalReflectance()
                        self.getTotalGreenValues()
                        self.getTotalBlueValues()
                        self.getTotalRedValues()
                        self.getRedToGreenRatio()
                        self.getAllColourDensities()
               
                       
                        
        def initValuesToNone(self): #function to set up the object with empy attributes in order to be able to check they have been set
                self.area = None
                self.averageWidth = None
                self.centroid = None
                self.circularity = None
                self.boundingBox_Points = None
                self.minBoundingBox_Points = None
                self.boundingEllipse = None
                self.boundingAxis = None
                self.boundingElliplse = None
                self.majorAxis = None
                self.minorAxis = None
                self.length = None
                self.width = None
                self.perimeter = None
                self.ellipse = None
                self.ellipse_MinorAxisLength = None
                self.ellipse_MajorAxisLength = None
                self.contourLengthToWidth = None
                self.convexHull = None
                self.convexHullArea = None
                self.convexAreaDivCntArea = None
                self.convexArea = None
                self.allPixelPoints = None
                self.allPixelPointColours = None
                self.totalColourIntensity = None
                self.totalReflectance = None
                self.totalBlueValues = None
                self.totalGreenValues = None
                self.totalRedValues = None
                self.totalPixelsContained = None
                self.redToGreenRatio = None
                self.allColourDensities = None
               
        
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
        def getAverageWidth(self):
                '''Finds the average width of the contour (area/length)

                Args:
                    none
                
                Returns:
                    The area in pixels
                '''
                if (self.averageWidth is None):
                        self.averageWidth = float(self.getArea())/float(self.getLength())
                return self.averageWidth

        #get average position (centroid) of the contour relative to top left 0px,0px
        def getCentroid(self):
                '''The average central position of the contour expressed as an x,y coordinate

                Args:
                    none    

                Returns:
                    An array containing the X and Y coordinates of the centroid
                    
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
                        self.getBoundingEllipse()
                        self.ellipse_MinorAxisLength = min(self.ellipse_axes)  
                return self.ellipse_MinorAxisLength

        def getMinBoundingBoxDimensions(self):
                '''Find the length and width of the bounding box of the contour. This can be used as  proxy for the length and width of the contour itself

                Args:
                     None 

                Returns:
                     An array containing the width and length in that order [width,length]
                     
                '''
                if (self.width is None or self.length is None):
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
                        self.length = round(max(dimension1, dimension2),2)
                return [self.width,self.length]
        def getLength(self):
                '''Get just the length of the contour from the minBoundingBoxDimensions() function

                Args:
                    None 

                Returns:
                    Integer
                    
                '''
                if(self.length is None):
                        self.getMinBoundingBoxDimensions()
                return self.length
        
        def getWidth(self):
                '''Get just the length of the contour from the minBoundingBoxDimensions() function

                Args:
                    None 

                Returns:
                    Integer
                    
                '''
                if(self.width is None):
                        self.getMinBoundingBoxDimensions()
                return self.width
        
        def getPerimeter(self):
                '''Returns the length of the perimiter of the contour in pixels

                Args:
                    None
                    
                Returns:
                    The length of the perimeter of the contour in pixel
                
                '''
                if (self.perimeter is None):
                        self.contourLength = cv2.arcLength(self.cnt,True)
                return self.contourLength
        
        def getHeywoodCircularity(self):
                '''Calculate the circularity of the the contour using the Haywood Circularity Factor formula. The function returns the inverse of the result of the Haywoord formula

                Args:
                    None

                Returns:
                    A double that represents the circularity of the contour with a value between 0 and 1 where a value of 1 represents a perfect circle.

                '''
               
                if(self.circularity is None):
                        self.getArea()
                        self.circularity = 1/((self.getPerimeter()/(2*math.sqrt(math.pi*self.area))))
                return self.circularity

        def getContourLengthToWidth(self):
                '''Returns the ratio of  to width (hieght/width)

                Args:
                    None
                
                Returns:
                    The ratio of length to width as a double
                '''
                
                if (self.contourLengthToWidth == None):
                        self.getMinBoundingBoxDimensions()
                        self.contourLengthToWidth = float(self.getLength())/float(self.getWidth())
                return self.contourLengthToWidth
        def getConvexHull(self):
                '''Returns an array of all the pixel points in the convex hull of the contour

                Args:
                    None
                
                Returns:
                    An array of all the pixel points in the contour
                '''
                if(self.convexHull is None):
                        self.convexHull = cv2.convexHull(self.cnt)
                return self.convexHull
        def getConvexHullArea(self):
                '''Returns the area of the convex hull of the contour

                Args:
                    None
                
                Returns:
                    Float
                    
                '''
                if(self.convexHullArea is None):
                        self.convexHullArea = float(cv2.contourArea(self.getConvexHull()))
                return self.convexHullArea
        def getConvexAreaDivCntArea(self):
                '''Returns the convex area devided by the area of the contour

                Args:
                    None
                
                Returns:
                    Float
                    
                '''
                if (self.convexAreaDivCntArea is None):
                        self.convexAreaDivCntArea = float(self.getConvexHullArea())/float(self.getArea())
                return self.convexAreaDivCntArea
        def getPixelPoints(self):
                '''Returns an array of all the pixel points in the contour

                Args:
                    None
                    
                Returns:
                    An array of all the pixel points in the contour
                    
                '''
                if(self.allPixelPoints is None):
                        drawing = np.zeros(self.binaryImg.shape,np.uint8) #create a zero'd drawing with same dimensions as given image
                        cv2.drawContours(drawing,[self.cnt],0,(255,255,255),-1)              
                        pixelPoints = np.nonzero(drawing)
                        self.allPixelPoints = pixelPoints
		return self.allPixelPoints
	def getTotalPixelsContained(self):
                '''Returns total number of pixel points in the contour

                Args:
                    None
                    
                Returns:
                    An array of all the pixel points in the contour
                
                '''
                if(self.totalPixelsContained is None):
                        self.getPixelPoints()     
                        rows = self.allPixelPoints[0]
                        cols = self.allPixelPoints[1]
                        count = 0
                        for x in range(0, (len(rows)-1)):
                                for y in range(0, (len(cols)-1)):
                                        count += 1
                        self.totalPixelsContained = count                
                return self.totalPixelsContained
	
	def getPixelPointColours(self):
                '''Returns an tuple of cordinates and colour arrays

                Args:
                    None
                    
                Returns:
                     An array of all the pixel points in the contour
                     
                '''
                
                if (self.allPixelPointColours is None):
                        pixelpoints = self.getPixelPoints()                 
                        colourList = list()
                        rows = self.allPixelPoints[0]
                        cols = self.allPixelPoints[1]
                        
                        for x in range(0, (len(rows)-1)):
                                for y in range(0, (len(cols)-1)):
                                        colourList.append([[rows[x],cols[y]],self.originalImg[rows[x],cols[y]]])
                                        
                        self.allPixelPointColours = colourList
                return  self.allPixelPointColours

        def getTotalColourIntensity(self):
                '''Returns the total of all three colour channels across all pixel contained in the contour

                Args:
                     None
                
                Returns:
                     Integer
                
                '''
                totalPixelValue = 0 #to keep track of the total of all colour channels added together
                if (self.totalColourIntensity is None):
                        self.getPixelPointColours()
        
                        for colours in self.allPixelPointColours:
                                for channel in colours[1]:
                                        totalPixelValue += channel
                        self.totalColourIntensity = totalPixelValue
                return self.totalColourIntensity        
        def getTotalReflectance(self):
                '''Returns the average intensity over all three channels of all the pixels in the contour

                Args:
                    None
                
                Returns:
                    Float
                
                '''
                
                #the total intensity devided by number of contained pixels
                self.totalReflectance = float(self.getTotalColourIntensity())/float(self.getTotalPixelsContained())
                        
                return self.totalReflectance

        def getTotalBlueValues(self):
                '''Returns the total of all blue channels in each pixel point accross the whole contour

                Args:
                    None
                
                Returns:
                    Integer
                
                '''
                if (self.totalBlueValues is None):
                        totalCount = 0
                        
                        self.getPixelPointColours()
                
                        for colours in self.allPixelPointColours:
                                totalCount += colours[1][0]

                        self.totalBlueValues = totalCount

                return self.totalBlueValues

        def getTotalGreenValues(self):
                '''Returns the total of all green channels in each pixel point accross the whole contour

                Args:
                    None
                
                Returns:
                    Integer
                    
                '''
                if (self.totalGreenValues is None):
                        totalCount = 0
                        
                        self.getPixelPointColours()
                
                        for colours in self.allPixelPointColours:
                                totalCount += colours[1][1]
                        self.totalGreenValues = totalCount
                        
                return self.totalGreenValues
        def getTotalRedValues(self):
                '''Returns the total of all red channels in each pixel point accross the whole contour

                Args:
                     None
                     
                Returns:
                     Integer
                     
                '''
                if (self.totalRedValues is None):
                        totalCount = 0

                        self.getPixelPointColours()
                        for colours in self.allPixelPointColours:
                                totalCount += colours[1][2]
                        self.totalRedValues = totalCount
                        
                return self.totalRedValues

        def getRedToGreenRatio(self):
                '''Returns the ratio of red to green values across the whole contour

                Args: None
                Returns: Float
                '''
                if (self.redToGreenRatio is None):
                        ratio = float()
                        ratio = float(self.getTotalGreenValues())/float(self.getTotalRedValues())
                        self.redToGreenRatio = ratio
                return self.redToGreenRatio

        def getAllColourDensities(self):
                '''Returns an array of the three BGR colour densities. Colour Density is the individual channels values added together devided by total number of pixel points in the contour

                Args:
                    None
                    
                Returns: Array of the colour densities in the openCV native order of BGR (Blue, Green, Red)

                '''
                if(self.allColourDensities is None):
                        
                        blueDensity = float(self.getTotalBlueValues())/float(self.getTotalColourIntensity())
                        greenDensity = float(self.getTotalGreenValues())/float(self.getTotalColourIntensity())
                        redDensity = float(self.getTotalRedValues())/float(self.getTotalColourIntensity())
                        self.allColourDensities = [blueDensity,greenDensity,redDensity]
                        
                return self.allColourDensities
                        
                      
                        
