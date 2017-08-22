import numpy as np
import cv2
import time
import threading
import dataTypes

from Tkinter import *
from picamera import PiCamera
from picamera.array import PiRGBArray


#this class is in chrage of processing a live stream of data
#from the raspberry pi camera. 
class imageProcessing():
    


    #camera input - raspberry pi camera 
    cam = PiCamera()
    videoStream = None
    resolution = (310, 220)

	
    debug = False    
    
    #HSV color range for blue and green LEDs used on the drone
    yellowUpper = np.array([74,255,255])
    yellowLower = np.array([10,93,93])
    
    greenUpper = np.array([179, 255, 255])
    greenLower = np.array([114, 90, 90])
    
    x = None
    y = None
    radius = None
    
    def nothing(self, x):
        pass
    #initial variables
    def __init__(self, resolution, debug):

	self.debug = debug
        self.cam.resolution = resolution
        self.cam.exposure_mode = 'backlight'
	self.cam.awb_mode = 'flash'
        self.cam.hflip = True
        self.cam.exposure_compensation = 25
        self.cam.framerate = 60
        self.videoStream = PiRGBArray(self.cam, size=self.resolution)
        
        
        
        
        if (debug):
            cv2.namedWindow('controls')
            
            cv2.createTrackbar('B-H-l', 'controls', 0,179, self.nothing)
            cv2.createTrackbar('B-S-l', 'controls', 0,255, self.nothing)
            cv2.createTrackbar('B-V-l', 'controls', 0,255, self.nothing)
            
            cv2.createTrackbar('B-H-u', 'controls', 0,179, self.nothing)
            cv2.createTrackbar('B-S-u', 'controls', 0,255, self.nothing)
            cv2.createTrackbar('B-V-u', 'controls', 0,255, self.nothing)

            """cv2.setTrackbarPos('B-H-l', 'controls', self.yellowLower[0])
	    cv2.setTrackbarPos('B-S-l', 'controls', self.yellowLower[1])
            cv2.setTrackbarPos('B-V-l', 'controls', self.yellowLower[2])
            
            cv2.setTrackbarPos('B-H-u', 'controls', self.yellowUpper[0])
            cv2.setTrackbarPos('B-S-u', 'controls', self.yellowUpper[1])
            cv2.setTrackbarPos('B-V-u', 'controls', self.yellowUpper[2])
	    """

	    cv2.setTrackbarPos('B-H-l', 'controls', self.greenLower[0])
	    cv2.setTrackbarPos('B-S-l', 'controls', self.greenLower[1])
            cv2.setTrackbarPos('B-V-l', 'controls', self.greenLower[2])
            
            cv2.setTrackbarPos('B-H-u', 'controls', self.greenUpper[0])
            cv2.setTrackbarPos('B-S-u', 'controls', self.greenUpper[1])
            cv2.setTrackbarPos('B-V-u', 'controls', self.greenUpper[2])
            

    
    
    #image processing required to get a specificColour
    def processImage(self, image, color):
        
        processedImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

	if (self.debug):
	    self.greenLower = np.array([cv2.getTrackbarPos('B-H-l','controls'), cv2.getTrackbarPos('B-S-l','controls'), cv2.getTrackbarPos('B-V-l','controls')])
            self.greenUpper = np.array([cv2.getTrackbarPos('B-H-u','controls'), cv2.getTrackbarPos('B-S-u','controls'), cv2.getTrackbarPos('B-V-u','controls')])
       
        #processing for HSV ranges
        if color=="yellow":
            processedImage = cv2.inRange(processedImage, self.yellowLower, self.yellowUpper)
        elif color=="green":
            processedImage = cv2.inRange(processedImage, self.greenLower, self.greenUpper)
	
	#futher processing for smoothing contours
	processedImage = cv2.erode(processedImage, None, iterations=3)
	processedImage = cv2.dilate(processedImage, None, iterations=3)

	processedImage = cv2.erode(processedImage, None, iterations=2)
	processedImage = cv2.dilate(processedImage, None, iterations=2)
	
	return processedImage;
    
    #calculate the position of largest contour in the image
    def calculatePosition(self, image, color):
        x = None
        y = None
        radius = None
        
         #find all countour in the image
        cnts = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        
        #print("len = " + str(len(cnts)))
        if len(cnts) > 0:
            #use only the largest contour
            c = max(cnts, key=cv2.contourArea)
            ((x,y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            #decrease the radius
            
            #if (color=="yellow"):
             #   radius = radius * 0.8
            
            if radius > 0:
                #exception handeling for devision by zero
                try:
                    x = int(M["m10"] / M["m00"])
                    y = int(M["m01"] / M["m00"])
                    radius = int(radius)                    
                
                    center = (self.x, self.y)
                    return (x,y,radius)
                
                except ZeroDivisionError, Argument:
                    print("error")
                    
        return None
        
    #read video stream from camera and return position of
    #largest contour
    def readStream(self):
        currentPos = None
        currentFrame = None
        image = None
        processedImage = None
        
        self.cam.capture(self.videoStream, format="bgr", use_video_port=True)
  
        image = self.videoStream.array
        HUD = image.copy()
        
        yellowImage = self.processImage(image, "yellow")
        yellowPos = self.calculatePosition(yellowImage, "yellow")
         
        greenImage = self.processImage(image, "green")
       	greenPos = self.calculatePosition(greenImage, "green")
        position = None
        
        if greenPos!=None and yellowPos!=None:
            
            posX = abs(yellowPos[0]-greenPos[0])
            posY = abs(yellowPos[1]-greenPos[1])
            posR = (yellowPos[2]+greenPos[2])/2
            
            if yellowPos[0] < greenPos[0]:
                posX = posX/2+yellowPos[0]
                posY = posY/2+yellowPos[1]
            elif yellowPos[0] > greenPos[0]:
                posX = posX/2+greenPos[0]
                posY = posY/2+greenPos[1]
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img=HUD, text=("x: "+str(posX)+" y: "+str(posY)), org=(posX+50,posY), fontFace=font, color=(255,255,255),fontScale=0.5, lineType=cv2.LINE_AA)
            
                
            currentPos = dataTypes.droneData(x=posX, y=posY, z=posR, direction=None, yellowX=yellowPos[0], yellowY=yellowPos[1],
                                             yellowZ=yellowPos[2], greenX=greenPos[0], greenY=greenPos[1], greenZ=greenPos[2], detected=False, inRadius=False)
            position = (posY,posX,posR)
            cv2.circle(HUD, (position[1], position[0]), position[2], (0,255,255),thickness=-10,lineType=8, shift=0)
            
 
        center = (int(self.resolution[0]/2),int(self.resolution[1]/2))
        radius = 50
        
        if currentPos != None:
            if currentPos.x < (center[0]+radius/2) and currentPos.x > (center[0]-radius/2) and currentPos.y < (center[1]+radius/2) and currentPos.y > (center[1]-radius/2):
                cv2.circle(HUD, center, radius, (55,255,125),thickness=10,lineType=8, shift=0)
                currentPos = dataTypes.droneData(x=posX, y=posY, z=posR, direction=None, yellowX=yellowPos[0], yellowY=yellowPos[1],
                                             yellowZ=yellowPos[2], greenX=greenPos[0], greenY=greenPos[1], greenZ=greenPos[2], detected=True, inRadius=True)
            else:
                cv2.circle(HUD, center, radius, (255,255,255),thickness=10,lineType=8, shift=0)
                currentPos = dataTypes.droneData(x=posX, y=posY, z=posR, direction=None, yellowX=yellowPos[0], yellowY=yellowPos[1],
                                             yellowZ=yellowPos[2], greenX=greenPos[0], greenY=greenPos[1], greenZ=greenPos[2], detected=True, inRadius=False)
        else:
            cv2.circle(HUD, center, radius, (3,225,225),thickness=10,lineType=8, shift=0)
        
        cv2.imshow("yellow Processing", yellowImage)
        cv2.imshow("Green Processing", greenImage)
        cv2.imshow("HUD", HUD)
        
        
        cv2.imshow("Original", image)
        key = cv2.waitKey(1) & 0xFF

        self.videoStream.truncate()
        self.videoStream.seek(0)
            
        return currentPos
        


