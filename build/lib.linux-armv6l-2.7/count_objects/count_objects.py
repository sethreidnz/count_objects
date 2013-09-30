import cv2
import sys
import numpy as np
from Tkinter import *
import count_objects


#attributes
thresholdValue = 90
lowThreshold = 90
max_lowThreshold = 100
ratio = 3
kernel_size = 3
contourList = list()
fontFace = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX,3,2,0)

#function definitions

def show_image(windowName,img):
    if (img == None):                      ## Check for invalid input
        print "Could not open or find the image"
    else:
        cv2.namedWindow(windowName, 0)        ## create window for display
        cv.ResizeWindow(windowName, 500,500);
        cv2.imshow(windowName,img)         ## Show image in the window
       
def close_image(img,elegment,iterations):
    if (img == None or element == None):                      ## Check for invalid input
        print "Could not open or find the image"
    else:
        img = cv2.dilate(img, element, iterations=(iterations+1))
        img = cv2.erode(img, element, iterations=iterations)
      
        return img
def threshold_gray(thresholdValue):
    ret, threshold_image = cv2.threshold(gray_image,thresholdValue,255,cv2.THRESH_BINARY_INV)
    return threshold_image

def CannyThreshold(img, lowThreshold):
    detected_edges = img
    detected_edges = cv2.Canny(detected_edges,lowThreshold,lowThreshold*ratio,apertureSize = kernel_size)
    dst = cv2.bitwise_and(img,img,mask = detected_edges)  # just add some colours to edges from original image.
    return dst
    
if len(sys.argv)!=2:                  ## Check for error in usage syntax
    print "Usage : python countSeeds.py <image_file>"
    


else:#continue with the program
    
    ## Read image file
    img = cv2.imread(sys.argv[1],cv2.CV_LOAD_IMAGE_COLOR)  

    #convert to grayscale
    gray_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    

    #threshold 
    threshold_image = countObjects.threshold_gray(thresholdValue)  
    
    #close image with morph_cross element
    element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    closed_image = close_image(threshold_image,element,5)
    
    drawing = np.zeros(img.shape,np.uint8)     # Image to draw the contours
    contours,hierarchy = cv2.findContours(closed_image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    seedCount = 1
    header = "____________________________________________________________________\n| Seed number | Centroid (x,y) | Seed Area | Width | Length | Circularity"             
    print header
    for cnt in contours:
        if (cv2.contourArea(cnt) > 50):               
            c = cf.Contour(gray_image, cnt)          
            contourList.append(c)
            color = np.random.randint(0,255,(3)).tolist()  # Select a random color
            cv2.drawContours(drawing,[cnt],0,(255,255,255),-1)
            c.getBoundingBox()
            area = c.getArea()
            c.getContourLength()
            boundingBoxDims = c.getBoundingBoxDimensions()
            print '|    ' + str(seedCount) + '        |' + str(c.getCentroid()) + '      |  '+ str(area) + '    |' + str(boundingBoxDims[0]) + '  | ' + str(boundingBoxDims[1]) + '   |' + str(round(c.getCircularity(),3)) + '|'
            textX = int(c.centroid[0])
            textY = int(c.centroid[1])
            cv2.putText(drawing, str(seedCount), (textX,textY),cv2.cv.CV_FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            seedCount = seedCount + 1
           
           
            cv2.polylines(drawing, [c.getBoundingBox()], True, (255,0,0),2,)
            #ellipse = c.getBoundingEllipse()
            #cv2.ellipse(drawing, ellipse, (0,0,255,0),2)
            

    ### show original
    show_image('input',img)
    cv.MoveWindow('input',0,0)
    
    ### show grayscale
    #show_image('gray_scale', gray_image)
    #cv.MoveWindow('gray_scale',500,0)
    
    ### show thresholded image
    #show_image('threshold_image', threshold_image)
    #cv.MoveWindow('threshold_image',1000,0)
    
    ### Show closed image
    #show_image('closed_image',closed_image)
    #cv.MoveWindow('opened_image',0,400)

    #Show final image
    show_image('output',drawing)
    cv.MoveWindow('output',500,0)
    
    ## Wait for keystroke to allow user to see image displays
    cv2.waitKey(0)                       
    cv2.destroyAllWindows()
