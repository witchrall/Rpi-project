#Importing all the necessary libraries.
import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors
from PIL import Image
import numpy
import time
import picamera

#Taking a picture with the separate camera module.
with picamera.PiCamera() as camera:
   
    camera.start_preview()
    
    time.sleep(2)
    
    camera.capture('/home/pi/Desktop/imgtest.png')

#Converting the taken image to RGB-grey and turning it into a 1D array.
img = Image.open('imgtest.png').convert('LA')
img.save('greytest.png')
data = np.asarray( img, dtype='uint8' )
gray = data[:,:,0]

#Convolution of img
kernel = np.ones((5,5),np.float32)/25
dst = cv2.filter2D(gray,-1,kernel)

#Extracting the edges out of the image using then concoluded one and trying to make the edges more prominent.
#edge = ((gray.astype(int) - dst.astype(int)) *4) +128 
#edge = cv2.max(edge, 0)
#edge = cv2.min(edge, 255)

#Extracting the edges out of the image using then concoluded one.
edge = gray.astype(int) - dst.astype(int)
edge = edge - edge.min()
edge = edge/edge.max() * 255
edge = np.asarray( edge, dtype="uint8" )

#Saving the image as the 4 different pictures next to each other.
plt.subplot(141),plt.imshow(img, cmap = 'gray'),plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(142),plt.imshow(gray, cmap = 'gray'),plt.title('Gray')
plt.xticks([]), plt.yticks([])
plt.subplot(143),plt.imshow(dst, cmap = 'gray'),plt.title('Averaging')
plt.xticks([]), plt.yticks([])
plt.subplot(144),plt.imshow(edge, cmap = 'gray'),plt.title('Edges')
plt.xticks([]), plt.yticks([])
plt.show()