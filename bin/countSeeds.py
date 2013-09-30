import cv2
import sys
import numpy as np
from count_objects import im_proc
from count_objects import contour_features as cf

#attributes
lowThreshold = 90
max_lowThreshold = 100
ratio = 3
kernel_size = 3
contourList = list()
fontFace = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX,3,2,0)
    
if len(sys.argv)!=2:                  ## Check for error in usage syntax
    print "Usage : python countSeeds.py <image_file>"
    


else:#continue with the program
    
    ## Read image file
    img = cv2.imread(sys.argv[1],cv2.CV_LOAD_IMAGE_COLOR)  

    #convert to grayscale
    gray_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    

    #threshold 
    threshold_image = im_proc.threshold_image(gray_image,im_proc.findThreshValue(gray_image),)  
    #print im_proc.findThreshValue(gray_image)
    #close image with morph_cross element
    element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    closed_image = im_proc.close_image(threshold_image,element,5)
    
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
    im_proc.show_image('input',img)
    cv2.cv.MoveWindow('input',0,0)
    
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
    im_proc.show_image('output',drawing)
    cv2.cv.MoveWindow('output',500,0)
    
    ## Wait for keystroke to allow user to see image displays
    cv2.waitKey(0)                       
    cv2.destroyAllWindows()
