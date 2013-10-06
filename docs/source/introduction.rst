========================================
Introduction to Count Objects Package
========================================

This package has been created with the purpose of being used as toolkit for the building of
object detecting and classifying application. The package can be used to analyse images of 
objects of interest in a high contrast foreground to background situation where the objects
of interest and the background are distinct in colour/intensity for thresholding purposes. The
toolbox also does not currently deal with overlapping objects of interest and as a result the 
objects must be separate for accurate identification of singular objects.
Given these conditions the combination of the im_proc module and the contour_features module
allows an application to identify and gather statistics about the objects in an image.

The im_proc module has functions for preparing the image through thresholding, opening,
closing and other operations. It also has some functions to identify objects (referred to from
now on as contours) in the image and create 'contour objects' made available through the contour_features
module.

The contour_features module contains the Contour Class which is used to store contour data as well
as calculate various statistics about the contour. The class has the option of both initialising values
on instantiation as well as writing until the appropriate 'get' method is called. This was done to 
help with performance on slower systems as some of the calculations are quite memory intensive.
The statistics available are:

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
    The length of the minor axis of the bounding ellipse in pixels

height: (double):
    The length (longest side) of the bounding box which can be considered a proxy for length

width: (double):
    The width (longest side) of the bounding box which can be considered a proxy for width

ellipse (array):
    An array of the points in the smallest bounding ellipse

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
    The ratio of red to blue channel values across the whole contour
                        
allColourDensities (Array of floats):
    Three values that represent the total value of each colour channel divided by the total intensity. In openCV native channel order of BGR. IE redTotal/totalColourIntensity.
