import StringIO
import subprocess
import os
import time
import cv
from datetime import datetime
from PIL import Image
import cv2
import numpy as np
from urllib2 import urlopen
from cStringIO import StringIO as StringIO2

# File settings
saveWidth = 1280
saveHeight = 960

# Save a full size image to disk
def saveImage(width, height):
    time = datetime.now()
    filename = "capture-%04d%02d%02d-%02d%02d%02d.jpg" % (time.year, time.month, time.day, time.hour, time.minute, time.second)
    subprocess.call("raspistill -w 1296 -h 972 -t 0 -e jpg -q 15 -o %s" % filename, shell=True)
    return filename

filename = saveImage(saveWidth, saveHeight)
src = cv.LoadImageM(filename,cv.CV_LOAD_IMAGE_COLOR)
image = cv.CreateImage(cv.GetSize(src), cv.IPL_DEPTH_8U, 1)
cv.CvtColor(src, image, cv.CV_RGB2GRAY)
laplace = cv.Laplace(src, image)
cv.NamedWindow('testImage', cv.CV_WINDOW_AUTOSIZE)
cv.ShowImage('testImage', laplace)
cv.WaitKey(0)
