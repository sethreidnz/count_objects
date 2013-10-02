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
    cList = im_proc.getContourListFrom(img, initValues=True)
    output = im_proc.drawContoursFromList(cList, img.shape)
    ### show original
    im_proc.show_image('input',img)
    cv2.cv.MoveWindow('input',0,0)

    #Show final image
    im_proc.show_image('output',output)
    cv2.cv.MoveWindow('output',500,0)

    ## Wait for keystroke to allow user to see image displays
    cv2.waitKey(0)
    cv2.destroyAllWindows()
