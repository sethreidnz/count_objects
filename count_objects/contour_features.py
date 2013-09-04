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

class Contour:
        '''Contour class used to create and store statists about the obejcts found in an image using cv2.findContours function. The attributes are not calculated on instantiation but are popluated when the corresponding function is called on the contour.

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
        '''
        def __init__(self,img,cnt):
                '''The constructor for a contour object

                Args:
                    img (image): The image that the contour moments were detected from
                    cnt (moment): An openCV contour moment structure that is returned using cv2.findContours()

                Returns:
                    None

                '''
                self.img = img
                self.cnt = cnt
                self.size = len(cnt)

        #get contour area
        def getArea(self):
                '''Finds the area of the contour in pixels

                Args:
                     none

                Returns:
                     The area in pixels
                '''
                self.area = cv2.contourArea(self.cnt)

                return self.area
            

        #get average position (centroid) of the contour relative to top left 0px,0px
        def getCentroid(self):
                '''

                Args:
                         

                Returns:
                      
                '''    
                self.moments = cv2.moments(self.cnt)
                if self.moments['m00'] != 0.0:       
                        self.cx = self.moments['m10']/self.moments['m00']
                        self.cy = self.moments['m01']/self.moments['m00']
                        self.centroid = (int(round(self.cx,0)),int(round(self.cy)))
                        return self.centroid            
                else:
                        return "Region has zero area"

        def getBoundingBox(self):
                '''Get the minimal bounding box for the countour
                Args:
                   None
                   
                Returns:
                   An array containing the x,y values of the four corners of the bounding box
                '''
                rect = cv2.minAreaRect(self.cnt)
                
                points = cv2.cv.BoxPoints(rect)
                points = np.int0(np.around(points))
                

                self.boundingBox_points = points
                self.boundingBox_top = points[0]
                self.boundingBox_right = points[1]
                self.boundingBox_bottom = points[2]
                self.boundingBox_right = points[3]
                
                return self.boundingBox_points

        def getBoundingEllipse(self):
                '''Get the smallest bounding ellipse for the contour

                Args:
                    None

                Returns:
                    An array of the points in the bounding ellipse
                ''' 
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
                if (self.ellipse is None):
                        self.getBoundingEllipse()
                
                self.ellispse_MinorAxisLength = min(self.ellipse_axes)  
                return self.ellispse_MinorAxisLength

        def getBoundingBoxDimensions(self):
                '''Find the length and width of the bounding box of the contour. This can be used as  proxy for the length and width of the contour itself

                Args:
                    None 

                Returns:
                    An array containing the width and the height in that order [width,height]
                ''' 
                if (self.boundingBox_points is None):
                        self.getBoundingBox()

                #for dimention 1 using the top corner and the right corner
               
                a = (self.boundingBox_right[0] - self.boundingBox_top[0])            
                b = (self.boundingBox_right[1] - self.boundingBox_top[1])
                dimension1 = math.sqrt(a**2 + b**2)

                #for dimension 2 using the bottom corner and the left corner

                c = (self.boundingBox_right[0] - self.boundingBox_bottom[0])
                d = (self.boundingBox_right[1] - self.boundingBox_bottom[1])
                    
                                    
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
                self.contourLength = cv2.arcLength(self.cnt,True)
                return self.contourLength
        
        def getCircularity(self):
                '''Calculate the circularity of the the contour using the Haywood Circularity Factor formula. The function returns the inverse of the result of the Haywoord formula

                Args:
                    None

                Returns:
                    A double that represents the circularity of the contour with a value between 0 and 1 where a value of 1 represents a perfect circle.
                ''' 
                if (self.area is None):
                        self.getArea()
                if (self.contourLength is None):
                        self.ContourLength()
                               
                self.circularity = 1/((self.contourLength/(2*math.sqrt(math.pi*self.area))))
                return self.circularity

        def getContourLengthToWidth(self):
                '''Returns the ratio of  to width (hieght/width)

                Args:
                    None

                Returns:
                    The ratio of length to width as a double
                '''
                if self.width == None or self.height == None:
                        self.getBoundingBoxDimensions()
                
                self.contourLengthToWidth = self.height/self.width
                return self.contourLengthToWidth
