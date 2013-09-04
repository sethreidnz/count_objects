=============
Count Objects
=============

Warning: This is very much in a development stage V: 0.0.1

This is a framework that can be used to design futher applications with the purpose
of counting objects of interest in a high contrast background to foreground context.
If lighting conditions are correct (even backlit image with white background the
functions in this tool box should be able to acurately count and measure statistics 
of the objects. The package uses OpenCV and python (cv2 bindings).

Such statistics include:

Width (px)
Circularity
Area (px)
Major and Minor Axis
Smallest bounding rectangle
Width and Height (px)
Total number of objects in the image

Included is a script contour_class.py which I used to make my contour_features.py and Contour class. This is a script made by abidrahmank
on GitHub and all his code can be found here: 

 https://github.com/abidrahmank/

He is responsible for the bulk of this work and many thanks to him.

============
Install
============

Clone repositry, cd to directory and run:

python setup.py install

============
Developer
============

JustSayNo
Sept 2013
Lincoln University
New Zealand

