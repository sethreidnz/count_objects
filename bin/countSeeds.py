import cv2
import sys
import numpy as np
from Tkinter import *
from count_objects import im_proc
from count_objects import contour_features as cf
import pprint
 
#attributes
fontFace = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX,3,2,0)
     
if len(sys.argv)!=2:                  ## Check for error in usage syntax
    print "Usage : python countSeeds.py <image_file>"
 
else:#continue with the program
 
    ## Read image file in colour
    img = cv2.imread(sys.argv[1],cv2.CV_LOAD_IMAGE_COLOR)
    cList = im_proc.getContourListFrom(img, initValues=True)
    drawing = np.zeros(img.shape,np.uint8)#Image to draw the contours
    seedCount = 1
    header = "____________________________________________________________________\n| Seed number | Centroid (x,y) | Seed Area | Width | Length | Circularity|"            
    print header
    for c in cList:
        if (c.area > 50):
            #color = np.random.randint(0,255,(3)).tolist()  # Select a random color
            cv2.drawContours(drawing,[c.cnt],0,(255,255,255),-1)
            c.getContourLength()
            boundingBoxDims = c.getMinBoundingBoxDimensions()
            print '|    ' + str(seedCount) + '        |' + str(c.getCentroid()) + '      |  '+ str(c.area) + '    |' + str(boundingBoxDims[0]) + '  | ' + str(boundingBoxDims[1]) + '   |' + str(round(c.circularity,3)) + '|'
            textX = int(c.centroid[0])
            textY = int(c.centroid[1])
            cv2.putText(drawing, str(seedCount), (textX,textY),cv2.cv.CV_FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            seedCount = seedCount + 1
            cv2.polylines(drawing, [c.getBoundingBox()], True, (255,0,0),2,)
 
    ### show original
    im_proc.show_image('input',img)
    cv2.cv.MoveWindow('input',0,0)
 
    #Show final image
    im_proc.show_image('output',drawing)
    cv2.cv.MoveWindow('output',500,0)
 
    ## Wait for keystroke to allow user to see image displays
    cv2.waitKey(0)
    cv2.destroyAllWindows()