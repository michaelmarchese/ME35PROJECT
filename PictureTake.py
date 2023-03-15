

#Takes an image using a raspberry pi camera & finds the percentage of pixels in the image that are red
#by Maddie Pero

#import libraries 
from picamera2 import Picamera2 
import cv2 as cv 
import numpy as np
from libcamera import controls
import time

picam2 = Picamera2()

#configure the picamera
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous}) #sets auto focus mode


picam2.start() #must start the camera before taking any images
time.sleep(1)



for x in range(25):
    y = input("S")

    if(y=="S"):
        for i in range(10):
            picam2.capture_file('/home/tuftsrobot/ME35PROJECT/KIWI/image%s%s.jpg' % (x, i))
    #!change the size of the image or turn off auto focus


picam2.stop() #stop the picam 
