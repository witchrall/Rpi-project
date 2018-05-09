#Importing all the necessary libraries.
import numpy as np
import sys
sys.path.append("/home/pi/pylepton")
from pylepton import Lepton
import cv2
from PIL import Image
import picamera
import RPi.GPIO as GPIO

#Taking a picture with the separate camera module.
with picamera.PiCamera() as camera:
   # camera.resolution(800, 480)
    camera.capture('/home/pi/Desktop/Sak/imgtest.png')

#Takes an IR-image with the lepton module
with Lepton() as l:
    a,_ = l.capture()
cv2.normalize(a, a, 0, 65535, cv2.NORM_MINMAX) # extend contrast
np.right_shift(a, 8, a) # fit data into 8 bits
cv2.imwrite("output.png", np.uint8(a)) # write it!


#Converting the taken image to RGB-grey and turning it into a 1D array.
img = Image.open('imgtest.png').convert('LA')
data = np.asarray( img, dtype='uint8' )
gray = data[:,:,0]

#Convolution of img
kernel = np.ones((5,5),np.float32)/25
dst = cv2.filter2D(gray,-1,kernel)

#Extracting the edges out of the image using then concoluded one.
edge = gray.astype(int) - dst.astype(int)
edge = edge - edge.min()
edge = edge/edge.max() * 255
edge = np.asarray( edge, dtype="uint8" )

#Saves the array as an image for later use
edge2 = Image.fromarray(edge)
edge3 = cv2.resize(edge, (1920,1080))
edge4 = Image.fromarray(edge3)
edge4.save("test.png")
cropped = edge3[40:1040, 250:1670]
cropped2 = cv2.resize(cropped, (1920,1080))
edge5 = Image.fromarray(cropped2)

#edge4.crop(30, 30)
#edge5 = cv2.resize(edge4, (1920, 1080))
#edge6 = Image.fromarray(edge5)
#Resizing output image
img = cv2.imread('output.png')
F = cv2.resize(img, (1920, 1080), fx=0, fy=0, interpolation = cv2.INTER_CUBIC)
#F = cv2.applyColorMap(F,cv2.COLORMAP_JET)

img2 = Image.fromarray(F)

#Rotates image 180 degrees
#img3 = img2.rotate(180, expand=1)
img2.save('refernceimage.png')

#Makes output transparrent
img2.putalpha(80)

#Blends the background with the foreground where the foreground is transparrent
edge5.paste(img2, (0,20),img2)
edge5.save('blendtest.png')