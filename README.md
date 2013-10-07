=============
Count Objects
=============

Warning: This is very much in a development stage V: 0.0.2

This is a framework that can be used to design futher applications with the purpose
of counting objects of interest in a high contrast background to foreground context.
If lighting conditions are correct (even backlit image with white background) the
functions in this tool box should be able to acurately count and measure statistics 
of the objects. It is suggested to use an LED backlit lightbox.The package uses OpenCV 
and python (cv2 bindings).

The package is depended on python numPY and openCV version 2.3 or higher with python cv2
bindings.

**Statistics available on contours found** 

* area
* centroid
* boundingBox
* minBoundingBox_Points
* boundingEllipse
* majorAxis
* minorAxis
* height
* width
* ellipse
* ellipse_MinorAxisLength          
* ellipse_MajorAxisLength
* contourLengthToWidth
* convexHull
* convexHullArea
* convexAreaDivCntArea
* allPixelPoints
* totalPixelsContained
* allPixelPointColours
* totalColourIntensity
* totalReflectance
* totalBlueValues                       
* totalGreenValues                       
* totalRedValuess                      
* redToGreenRatio
* allColourDensities

Included is a script contour_class.py which I used to make my contour_features.py and Contour class. This is a script made by abidrahmank
on GitHub and all his code can be found here: 

 https://github.com/abidrahmank/

He is responsible for the bulk of this work and many thanks to him.


## Install ##

Ensure you have python (with numPY included) and openCV (with cv2 Bindings) installed on your system.

Clone repositry, cd to directory and run:
python setup.py install

## Developer ##

Seth Reid, Oct 2013, Lincoln University, New Zealand

