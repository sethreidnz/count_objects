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
import contour_features as cf

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
        thresholdValue (int Default= None): A value between 0 and 255 around which the image will be thresholed. Any values bellow the given value will be black while those above will become white in the output
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

def prepareImage(img, threshValue = None):
    ''' Prepare an image by converting to grey, thresholding and then opening it 

    Args:
        colourImg (image): the image to be operated on

    Returns:
        An array containing the prepared image and the original image [prepared image, original image]
    '''
    if (threshValue is None):
        threshValue = findThreshValue(img)
    threshold_img = threshold_image(img,threshValue)  
    element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    closed_img = close_image(threshold_img,element,1)
    return threshold_img

def getContourListFrom(originalImage, threshValue = None, initValues = False):
    ''' Gets a list of contours from a colour image. Optionally can set teh threshValue, and whether the contour objects
        have their attributes pre-populated with flag "initValues"

    Args:
        img (image): the image to be operated on
        threshValue: (boolean :optional) optional threshold value if built in auto-threshold does not work for given image.
        initValues: (boolean :optional) Boolean value to specify whether or not to calculate all the contour statistics on instantiation or not.

    Returns:
        An list of contour objects
    '''
    contourList = list()
    gray_image = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    prepared_image = prepareImage(gray_image)
    prepared_image_copy = prepared_image.copy()
    contours,hierarchy = cv2.findContours(prepared_image_copy,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    seedCount = 1
    for cnt in contours:
        if (cv2.contourArea(cnt) > 50):#if the contour is really small ignore it
            c = cf.Contour(originalImage,cnt,prepared_image,initValues)
            contourList.append(c)
    return contourList
