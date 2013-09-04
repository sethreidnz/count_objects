'''
*****************
img_proc module
*****************

The im_proc module has utility function that can be used to prepare an image
for processing and analysis. The module relies on openCV (cv2). Many of the functions are simply extensions
of openCV functions make easier to implement by reducing them to simple singular functions.
Created by Seth Reid August 2013.

'''

import cv2
import cv
import sys
import numpy as np

def show_image(windowName,img):
    '''Diplay an image in an openCV named window.

    Args:
        windowName (str): The name of the window to use
        img (image): The image to be shown

    Returns:
        none
    '''
    if (img == None):                      ## Check for invalid input
        print "Could not open or find the image"
    else:
        cv2.namedWindow(windowName, cv2.CV_WINDOW_AUTOSIZE)        ## create window for display

        cv2.imshow(windowName,img)         ## Show image in the window

       
def close_image(img,element,iterations):
    '''Perform a morphological close operation (dilate followed by erode) to the image supllied and by the iterations specified.

    Args:
        img (image): The image to be operated on
        element (element): a morphological element by which to do the operation
        iterations (int): the number of iterations of the close operation

    Returns:
        the closed image
    '''
    if (img == None or element == None):## Check for invalid input
        print "Could not open or find the image"
    else:
        img = cv2.dilate(img, element, iterations=iterations)
        img = cv2.erode(img, element, iterations=iterations)
      
        return img

def open_image(img,element,iterations):
    '''Perform a morphological open operation (erode followed by dilate) to the image supllied and by the iterations specified.

    Args:
        img (image): The image to be operated on
        element (element): a morphological element by which to do the operation
        iterations (int): the number of iterations of the open operation

    Returns:
        the opned image
    '''
    
    if (img == None or element == None):## Check for invalid input
        print "Could not open or find the image"
    else:
        img = cv2.dilate(img, element, iterations=iterations)
        img = cv2.erode(img, element, iterations=iterations)

def threshold_image(img,thresholdValue):
    ''' Perform a threshold eperation on a supplied image with the thresholdValue specified.

    Args:
        img (image): The image to be operated on
        thresholdValue: a value between 0 and 255 around which the image will be thresholed. Any values bellow the given value will be black while those above will become white in the output
    Returns:
        A binary image based on the threshold value supplied
    '''
    
    ret, threshold_image = cv2.threshold(img,thresholdValue,255,cv2.THRESH_BINARY_INV)
    return threshold_image

def singleChannelHist(img):
    ''' creates single channel intensity histogram from the image supplied

    Args:
        img (image): The image to be operated on.

    Returns:
        a numpy array with the histogram data contained
    '''
    bins = np.arange(256).reshape(256,1)
    color = [(255,255,255)]
    for ch, col in enumerate(color):
        hist_item = cv2.calcHist([img],[ch],None,[256],[0,256])
        cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
        hist=np.int32(np.around(hist_item))    
    return hist

def findThreshValue(img):
    ''' Find an appropriate threshold value in an image with a distict background and foreground gray-scale intensity contrast. This function should be used on an image that has already been converted to gray scale. The function works by gathering the histrogram data of the image and working backwards through the numpy array to find the first none zero values. It then continues until it finds a zero value. This is consideredto be the point at which the darker parts of the image end and is considered the threshold value.

    Args:
        img (image): the image to be operated on

    Returns:
        An integer threshold value
    '''
    hist = singleChannelHist(img)
    for x in range(hist.size -1 , 0, -1):
        if hist[x] > 0:
            break
    for y in range(x, 0, -1):
        if hist[y] == 0:
            break
    return y  
