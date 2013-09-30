Introduction to the Count Objects Toolbox
=========================================

This toolbox is built using Python and OpenCV (cv2 bindings) for the purpose
of speeding up the devleopment of an objects counting and categorising application.
The toolbox requires OpenCV, Python and pythons Numpy package to be installed. The 
package allows for the development of an application that can take an image, with clear 
foreground/background contrast, prepare and then analyse the image for objects of interest
for certain statistics important in identifying the type of object deteted.


It is split into two modules. The first of which is im_proc which has many functions that
can be used to process an image into a form that can then have the openCV function findContours()
find all the objects of interest in the image. The second is contour_features which takes
a contour found by findContours() and creates a Contour object. This object is capable of 
calculating many different statistics about the contour that can be used to identify the object.